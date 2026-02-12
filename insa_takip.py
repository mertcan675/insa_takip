import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- VERİ TABANI AYARI (KALICI DEPOLAMA) ---
DB_FILE = "insa_takip_db.csv"

def veriyi_getir():
    """Veritabanı dosyasını okur, yoksa yeni sıralı listeyi oluşturur."""
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).to_dict('records')
   
    # SENİN İSTEDİĞİN KRİTİK İNCE İŞ SIRALAMASI:
    return [
        {"id": 1, "is": "1. Kaba Tesisat (Elektrik-Su)", "durum": "Bekliyor", "usta": "Tesisat Ekibi", "tarih": "-", "kanit": "-"},
        {"id": 2, "is": "2. Dış Cephe Mantolama", "durum": "Bekliyor", "usta": "Dış Cephe Ekibi", "tarih": "-", "kanit": "-"},
        {"id": 3, "is": "3. Kaba Sıva", "durum": "Bekliyor", "usta": "Sıva Ekibi", "tarih": "-", "kanit": "-"},
        {"id": 4, "is": "4. Kapı ve Pencere Doğramaları", "durum": "Bekliyor", "usta": "Doğrama Ekibi", "tarih": "-", "kanit": "-"},
        {"id": 5, "is": "5. Şap Dökümü", "durum": "Bekliyor", "usta": "Şap Ekibi", "tarih": "-", "kanit": "-"},
        {"id": 6, "is": "6. Alçı Sıva ve Saten", "durum": "Bekliyor", "usta": "Alçıcı", "tarih": "-", "kanit": "-"},
        {"id": 7, "is": "7. Islak Hacim İzolasyonu", "durum": "Bekliyor", "usta": "İzolasyon Ekibi", "tarih": "-", "kanit": "-"},
        {"id": 8, "is": "8. Seramik ve Fayans", "durum": "Bekliyor", "usta": "Fayansçı", "tarih": "-", "kanit": "-"},
        {"id": 9, "is": "9. Mutfak Dolabı ve Kapılar", "durum": "Bekliyor", "usta": "Mobilyacı", "tarih": "-", "kanit": "-"},
        {"id": 10, "is": "10. Parke ve Süpürgelik", "durum": "Bekliyor", "usta": "Parkeci", "tarih": "-", "kanit": "-"},
        {"id": 11, "is": "11. Son Kat Boya ve Aksesuarlar", "durum": "Bekliyor", "usta": "Boya Ekibi", "tarih": "-", "kanit": "-"}
    ]

def veriyi_kaydet(liste):
    """Verileri CSV dosyasına yazar."""
    pd.DataFrame(liste).to_csv(DB_FILE, index=False)

# Session State (Uygulama belleği) başlatma
if 'db' not in st.session_state:
    st.session_state.db = veriyi_getir()

# --- ARAYÜZ TASARIMI ---
st.set_page_config(page_title="Pro-Build V1.0", layout="wide", page_icon="🏗️")

# Kenar Çubuğu Giriş Ayarı
st.sidebar.title("🏗️ PRO-BUILD")
st.sidebar.subheader("Yönetim Paneli")
mod = st.sidebar.radio("Yetki Girişi:", ["Patron / Mühendis", "Usta Paneli"])

# --- USTA PANELİ ---
if mod == "Usta Paneli":
    st.header("👷 Saha İş Teslim Ekranı")
    st.write("Lütfen bitirdiğiniz işi seçin ve fotoğrafını yükleyin.")
   
    # Reddedilen veya Bekleyen işleri göster
    yapilacak_isler = [i["is"] for i in st.session_state.db if i["durum"] in ["Bekliyor", "Reddedildi"]]
   
    if yapilacak_isler:
        with st.container():
            secilen = st.selectbox("İş Listesi:", yapilacak_isler)
            foto = st.file_uploader("📷 İşin Fotoğrafını Yükle (Zorunlu Kanıt)", type=['jpg', 'png', 'jpeg'])
            notlar = st.text_area("Varsa Ek Notunuz:")
           
            if st.button("İşi Onaya Gönder", use_container_width=True):
                if foto:
                    for is_kalemi in st.session_state.db:
                        if is_kalemi["is"] == secilen:
                            is_kalemi["durum"] = "Onay Bekliyor"
                            is_kalemi["tarih"] = datetime.now().strftime("%d-%m-%Y %H:%M")
                            is_kalemi["kanit"] = "Görsel Yüklendi"
                    veriyi_kaydet(st.session_state.db)
                    st.success(f"✅ {secilen} gönderildi! Patron onayı bekleniyor.")
                    st.balloons()
                else:
                    st.error("❌ HATA: Fotoğraf yüklemeden işi tamamlayamazsınız!")
    else:
        st.info("Harika! Üzerinizde bekleyen bir iş bulunmuyor.")

# --- PATRON PANELİ ---
else:
    st.header("📊 Şantiye Genel Denetim")
   
    # Sayaç Kartları
    c1, c2, c3 = st.columns(3)
    biten = len([i for i in st.session_state.db if i["durum"] == "Tamamlandı"])
    bekleyen = len([i for i in st.session_state.db if i["durum"] == "Onay Bekliyor"])
   
    c1.metric("Toplam Adım", len(st.session_state.db))
    c2.metric("Tamamlanan ✅", biten)
    c3.metric("Onay Bekleyen ⏳", bekleyen)

    st.divider()
   
    # Genel Tablo
    st.subheader("📋 Güncel İş Akış Durumu")
    df = pd.DataFrame(st.session_state.db)
   
    # Renk paleti fonksiyonu
    def color_df(val):
        if val == "Tamamlandı": return 'background-color: #d4edda'
        if val == "Onay Bekliyor": return 'background-color: #fff3cd'
        if val == "Reddedildi": return 'background-color: #f8d7da'
        return ''

    st.dataframe(df.style.applymap(color_df, subset=['durum']), use_container_width=True)

    st.divider()

    # Onay Merkezi
    st.subheader("🔔 Gelen İş Onay Talepleri")
    onay_listesi = [i for i in st.session_state.db if i["durum"] == "Onay Bekliyor"]
   
    if onay_listesi:
        for is_kalemi in onay_listesi:
            with st.expander(f"İncele: {is_kalemi['is']}"):
                st.write(f"**Usta/Ekip:** {is_kalemi['usta']}")
                st.write(f"**Gönderim Saati:** {is_kalemi['tarih']}")
                st.info("📷 Görsel Kanıt Sisteme Yüklendi. Lütfen sahayı kontrol edin.")
               
                col_onay, col_red = st.columns(2)
                if col_onay.button(f"ONAYLA - {is_kalemi['id']}", key=f"on_{is_kalemi['id']}", type="primary"):
                    is_kalemi["durum"] = "Tamamlandı"
                    veriyi_kaydet(st.session_state.db)
                    st.rerun()
                if col_red.button(f"REDDET - {is_kalemi['id']}", key=f"red_{is_kalemi['id']}"):
                    is_kalemi["durum"] = "Reddedildi"
                    veriyi_kaydet(st.session_state.db)
                    st.rerun()
    else:
        st.write("Şu an onay bekleyen bir iş kanıtı yok.")

st.sidebar.divider()
if st.sidebar.button("Sistemi Sıfırla (Test İçin)"):
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        st.rerun()
