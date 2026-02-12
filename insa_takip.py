import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- VERİ TABANI AYARI (CSV ÜZERİNDEN KALICI DEPOLAMA) ---
DB_FILE = "insa_takip_db.csv"

def veriyi_getir():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).to_dict('records')
    return [
        {"id": 1, "is": "Temel Kazısı", "durum": "Bekliyor", "usta": "Hafriyatçı Ali", "tarih": "-", "kanit": "-"},
        {"id": 2, "is": "Demir Bağlama", "durum": "Bekliyor", "usta": "Demirci Veli", "tarih": "-", "kanit": "-"},
        {"id": 3, "is": "Beton Dökümü", "durum": "Bekliyor", "usta": "Betoncu Hasan", "tarih": "-", "kanit": "-"},
        {"id": 4, "is": "Duvar Örümü", "durum": "Bekliyor", "usta": "Duvarcı Selim", "tarih": "-", "kanit": "-"}
    ]

def veriyi_kaydet(liste):
    pd.DataFrame(liste).to_csv(DB_FILE, index=False)

# Session State başlatma
if 'db' not in st.session_state:
    st.session_state.db = veriyi_getir()

# --- ARAYÜZ TASARIMI ---
st.set_page_config(page_title="Pro-Build V1", layout="wide")

st.sidebar.title("🏗️ PRO-BUILD SİSTEMİ")
mod = st.sidebar.radio("Giriş Yetkisi:", ["Patron / Mühendis", "Usta Paneli"])

# --- USTA PANELİ ---
if mod == "Usta Paneli":
    st.header("👷 Saha İş Teslim Ekranı")
    yapilacak_isler = [i["is"] for i in st.session_state.db if i["durum"] in ["Bekliyor", "Reddedildi"]]
   
    if yapilacak_isler:
        secilen = st.selectbox("Tamamladığınız İş:", yapilacak_isler)
        foto = st.file_uploader("İşin Fotoğrafını Yükle (Kanıt)", type=['jpg', 'png', 'jpeg'])
        notlar = st.text_input("Notunuz:")
       
        if st.button("Onaya Gönder"):
            if foto:
                for is_kalemi in st.session_state.db:
                    if is_kalemi["is"] == secilen:
                        is_kalemi["durum"] = "Onay Bekliyor"
                        is_kalemi["tarih"] = datetime.now().strftime("%d-%m-%Y %H:%M")
                        is_kalemi["kanit"] = "Fotoğraf Yüklendi"
                veriyi_kaydet(st.session_state.db)
                st.success(f"✅ {secilen} işi başarıyla gönderildi. Patron onayı bekleniyor.")
                st.rerun()
            else:
                st.error("❌ Fotoğraf yüklemeden işi bitiremezsiniz!")
    else:
        st.info("Şu an üzerinizde bekleyen bir iş yok.")

# --- PATRON PANELİ ---
else:
    st.header("📊 Şantiye Genel Denetim")
   
    # Özet Sayacı
    c1, c2, c3 = st.columns(3)
    biten = len([i for i in st.session_state.db if i["durum"] == "Tamamlandı"])
    bekleyen = len([i for i in st.session_state.db if i["durum"] == "Onay Bekliyor"])
   
    c1.metric("Toplam İş", len(st.session_state.db))
    c2.metric("Tamamlanan", biten)
    c3.metric("Onay Bekleyen", bekleyen)

    st.divider()

    # İş Akış Tablosu
    st.subheader("📋 Güncel İş Akışı")
    df = pd.DataFrame(st.session_state.db)
    st.dataframe(df, use_container_width=True)

    # Onay Merkezi
    st.subheader("🔔 Onay Bekleyen Kanıtlar")
    onay_listesi = [i for i in st.session_state.db if i["durum"] == "Onay Bekliyor"]
   
    if onay_listesi:
        for is_kalemi in onay_listesi:
            with st.expander(f"İncele: {is_kalemi['is']} ({is_kalemi['usta']})"):
                st.write(f"Tarih: {is_kalemi['tarih']}")
                st.write("📷 [Görsel Kanıt Mevcut]") # Gerçek uygulamada burada foto görünür
               
                col_onay, col_red = st.columns(2)
                if col_onay.button(f"ONAYLA - {is_kalemi['id']}", type="primary"):
                    is_kalemi["durum"] = "Tamamlandı"
                    veriyi_kaydet(st.session_state.db)
                    st.rerun()
                if col_red.button(f"REDDET - {is_kalemi['id']}"):
                    is_kalemi["durum"] = "Reddedildi"
                    veriyi_kaydet(st.session_state.db)
                    st.rerun()
    else:
        st.write("Yeni bildirim yok.")