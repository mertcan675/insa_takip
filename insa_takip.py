import streamlit as st

import pandas as pd

import os

import hashlib

from datetime import datetime

# --- GÜVENLİK VE ŞİFRELEME ---

def make_hashes(password):

    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):

    if make_hashes(password) == hashed_text:

        return hashed_text

    return False

# --- VERİ TABANI AYARLARI ---

DB_FILE = "insa_takip_db.csv"

USER_DB = "users_db.csv"

# Veritabanı dosyalarını kontrol et ve oluştur

if not os.path.exists(USER_DB):

    pd.DataFrame(columns=['username', 'password', 'role']).to_csv(USER_DB, index=False)

def veriyi_getir():

    if os.path.exists(DB_FILE):

        return pd.read_csv(DB_FILE).to_dict('records')

    return [

        {"id": 1, "is": "1. Kaba Tesisat (Elektrik-Su)", "durum": "Bekliyor", "usta": "Tesisat Ekibi", "tarih": "-", "kanit": "-"},

        {"id": 2, "is": "2. Dış Cephe Mantolama", "durum": "Bekliyor", "usta": "Dış Cephe Ekibi", "tarih": "-", "kanit": "-"},

        {"id": 3, "is": "3. Kapı ve Pencere Doğramaları", "durum": "Bekliyor", "usta": "Doğrama Ekibi", "tarih": "-", "kanit": "-"},

        {"id": 4, "is": "4. Kaba Sıva", "durum": "Bekliyor", "usta": "Sıva Ekibi", "tarih": "-", "kanit": "-"},

        {"id": 5, "is": "5. Şap Dökümü", "durum": "Bekliyor", "usta": "Şap Ekibi", "tarih": "-", "kanit": "-"},

        {"id": 6, "is": "6. Alçı Sıva ve Saten", "durum": "Bekliyor", "usta": "Alçıcı", "tarih": "-", "kanit": "-"},

        {"id": 7, "is": "7. Islak Hacim İzolasyonu", "durum": "Bekliyor", "usta": "İzolasyon Ekibi", "tarih": "-", "kanit": "-"},

        {"id": 8, "is": "8. Seramik ve Fayans", "durum": "Bekliyor", "usta": "Fayansçı", "tarih": "-", "kanit": "-"},

        {"id": 9, "is": "9. Parke ve Süpürgelik", "durum": "Bekliyor", "usta": "Parkeci", "tarih": "-", "kanit": "-"},

        {"id": 10, "is": "10. Kapı Kasaları ve Mutfak Dolapları", "durum": "Bekliyor", "usta": "Mobilyacı", "tarih": "-", "kanit": "-"},

        {"id": 11, "is": "11. Son Kat Boya ve Aksesuarlar", "durum": "Bekliyor", "usta": "Boya Ekibi", "tarih": "-", "kanit": "-"}

    ]

def veriyi_kaydet(liste):

    pd.DataFrame(liste).to_csv(DB_FILE, index=False)

# --- OTURUM YÖNETİMİ ---

if 'logged_in' not in st.session_state:

    st.session_state.logged_in = False

if 'db' not in st.session_state:

    st.session_state.db = veriyi_getir()

# --- ARAYÜZ AYARLARI ---

st.set_page_config(page_title="Pro-Build Enterprise", layout="wide", page_icon="🏗️")

# --- GİRİŞ / KAYIT EKRANI ---

if not st.session_state.logged_in:

    st.title("🏗️ Pro-Build Giriş Sistemi")

    auth_mode = st.tabs(["Giriş Yap", "Kayıt Ol"])

   

    with auth_mode[0]: # GİRİŞ

        user = st.text_input("E-posta / Kullanıcı Adı")

        pw = st.text_input("Şifre", type='password')

        if st.button("Giriş Yap", use_container_width=True):

            users = pd.read_csv(USER_DB)

            hashed_pw = make_hashes(pw)

            result = users[(users['username'] == user) & (users['password'] == hashed_pw)]

            if not result.empty:

                st.session_state.logged_in = True

                st.session_state.user_role = result.iloc[0]['role']

                st.session_state.username = user

                st.rerun()

            else:

                st.error("Hatalı bilgiler!")

    with auth_mode[1]: # KAYIT

        new_user = st.text_input("E-posta Seçin")

        new_pw = st.text_input("Şifre Belirleyin", type='password')

        role = st.selectbox("Rolünüz", ["Patron / Mühendis", "Usta Paneli"])

        if st.button("Kayıt Ol", use_container_width=True):

            users = pd.read_csv(USER_DB)

            if new_user in users['username'].values:

                st.warning("Bu kullanıcı zaten mevcut.")

            else:

                new_data = pd.DataFrame([[new_user, make_hashes(new_pw), role]], columns=['username', 'password', 'role'])

                new_data.to_csv(USER_DB, mode='a', header=False, index=False)

                st.success("Kayıt başarılı! Giriş yapabilirsiniz.")

# --- ANA UYGULAMA PANELİ ---

else:

    # Sidebar

    st.sidebar.title("🏗️ PRO-BUILD")

    st.sidebar.write(f"Kullanıcı: **{st.session_state.username}**")

    st.sidebar.write(f"Yetki: **{st.session_state.user_role}**")

    if st.sidebar.button("Çıkış Yap"):

        st.session_state.logged_in = False

        st.rerun()

    # --- USTA PANELİ ---

    if st.session_state.user_role == "Usta Paneli":

        st.header("👷 Saha İş Teslim Ekranı")

        yapilacak_isler = [i["is"] for i in st.session_state.db if i["durum"] in ["Bekliyor", "Reddedildi"]]

       

        if yapilacak_isler:

            secilen = st.selectbox("Bitirdiğiniz İş:", yapilacak_isler)

            foto = st.file_uploader("📷 Fotoğraf Yükle (Zorunlu)", type=['jpg', 'png', 'jpeg'])

            if st.button("Onaya Gönder", use_container_width=True):

                if foto:

                    for is_kalemi in st.session_state.db:

                        if is_kalemi["is"] == secilen:

                            is_kalemi["durum"] = "Onay Bekliyor"

                            is_kalemi["tarih"] = datetime.now().strftime("%d-%m-%Y %H:%M")

                    veriyi_kaydet(st.session_state.db)

                    st.success("İş onaya gönderildi!")

                    st.balloons()

                else:

                    st.error("Fotoğraf yüklemeden devam edemezsiniz!")

        else:

            st.info("Bekleyen işiniz bulunmuyor.")

    # --- PATRON PANELİ ---

    else:

        st.header("📊 Şantiye Genel Denetim")

        c1, c2, c3 = st.columns(3)

        biten = len([i for i in st.session_state.db if i["durum"] == "Tamamlandı"])

        bekleyen = len([i for i in st.session_state.db if i["durum"] == "Onay Bekliyor"])

       

        c1.metric("Toplam Adım", len(st.session_state.db))

        c2.metric("Tamamlanan", biten)

        c3.metric("Onay Bekleyen", bekleyen)

        st.divider()

        st.subheader("📋 İş Akış Tablosu")

        df = pd.DataFrame(st.session_state.db)

        st.dataframe(df, use_container_width=True)

        st.subheader("🔔 Onay Bekleyen Kanıtlar")

        onay_listesi = [i for i in st.session_state.db if i["durum"] == "Onay Bekliyor"]

        if onay_listesi:

            for is_kalemi in onay_listesi:

                with st.expander(f"İncele: {is_kalemi['is']}"):

                    st.write(f"Tarih: {is_kalemi['tarih']}")

                    c_onay, c_red = st.columns(2)

                    if c_onay.button(f"ONAYLA - {is_kalemi['id']}", type="primary"):

                        is_kalemi["durum"] = "Tamamlandı"

                        veriyi_kaydet(st.session_state.db)

                        st.rerun()

                    if c_red.button(f"REDDET - {is_kalemi['id']}"):

                        is_kalemi["durum"] = "Reddedildi"

                        veriyi_kaydet(st.session_state.db)

                        st.rerun()

        else:

            st.write("Onay bekleyen bildirim yok.")


