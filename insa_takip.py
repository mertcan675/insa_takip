import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime

# --- GÜVENLİK VE ŞİFRELEME ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- VERİ TABANI AYARLARI ---
DB_FILE = "insa_takip_db.csv"
USER_DB = "users_db.csv"

if not os.path.exists(USER_DB):
    pd.DataFrame(columns=['username', 'password', 'role']).to_csv(USER_DB, index=False)

def veriyi_getir():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).to_dict('records')
   
    # 🏗️ KABA VE İNCE İNŞAAT BİRLEŞİK SIRALAMA
    return [
        {"id": 1, "is": "K1. Hafriyat ve Temel Kazısı", "durum": "Bekliyor", "etap": "Kaba", "tarih": "-", "kanit": "-"},
        {"id": 2, "is": "K2. Temel Donatı ve Beton", "durum": "Bekliyor", "etap": "Kaba", "tarih": "-", "kanit": "-"},
        {"id": 3, "is": "K3. Kolon ve Perde Betonlar", "durum": "Bekliyor", "etap": "Kaba", "tarih": "-", "kanit": "-"},
        {"id": 4, "is": "K4. Kat Tabliye Betonu", "dur_": "Bekliyor", "etap": "Kaba", "tarih": "-", "kanit": "-"},
        {"id": 5, "is": "K5. Dış ve İç Tuğla Duvarlar", "durum": "Bekliyor", "etap": "Kaba", "tarih": "-", "kanit": "-"},
        {"id": 6, "is": "K6. Çatı Çelik/Ahşap Karkas", "durum": "Bekliyor", "etap": "Kaba", "tarih": "-", "kanit": "-"},
        {"id": 7, "is": "İ1. Elektrik-Su Kaba Tesisat", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"},
        {"id": 8, "is": "İ2. Kapı ve Pencere Doğramaları", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"},
        {"id": 9, "is": "İ3. Dış Cephe Mantolama", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"},
        {"id": 10, "is": "İ4. Kaba Sıva (İç Cephe)", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"},
        {"id": 11, "is": "İ5. Yerden Isıtma / Tesisat Döşeme", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"},
        {"id": 12, "is": "İ6. Şap Dökümü", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"},
        {"id": 13, "is": "İ7. Alçı Sıva ve Asma Tavan", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"},
        {"id": 14, "is": "İ8. Banyo İzolasyonu", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"},
        {"id": 15, "is": "İ9. Seramik ve Fayans Döşeme", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"},
        {"id": 16, "is": "İ10. Parke ve Süpürgelik", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"},
        {"id": 17, "is": "İ11. İç Kapı Montajı", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"},
        {"id": 18, "is": "İ12. Mutfak ve Banyo Dolapları", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"},
        {"id": 19, "is": "İ13. Vitrifiye (Musluk, Lavabo)", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"},
        {"id": 20, "is": "İ14. Son Kat Boya ve Temizlik", "durum": "Bekliyor", "etap": "İnce", "tarih": "-", "kanit": "-"}
    ]

def veriyi_kaydet(liste):
    pd.DataFrame(liste).to_csv(DB_FILE, index=False)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'db' not in st.session_state:
    st.session_state.db = veriyi_getir()

st.set_page_config(page_title="Pro-Build Full", layout="wide", page_icon="🏗️")

# --- LOGIN / SIGNUP (Öncekiyle aynı yapı) ---
if not st.session_state.logged_in:
    st.title("🏗️ Pro-Build Giriş Paneli")
    tab1, tab2 = st.tabs(["Giriş", "Kayıt"])
    with tab1:
        u = st.text_input("E-posta")
        p = st.text_input("Şifre", type='password')
        if st.button("Giriş"):
            users = pd.read_csv(USER_DB)
            if not users[(users['username'] == u) & (users['password'] == make_hashes(p))].empty:
                st.session_state.logged_in = True
                st.session_state.user_role = users[users['username'] == u].iloc[0]['role']
                st.session_state.username = u
                st.rerun()
            else: st.error("Hata!")
    with tab2:
        nu = st.text_input("Yeni E-posta")
        np = st.text_input("Yeni Şifre", type='password')
        nr = st.selectbox("Rol", ["Patron / Mühendis", "Usta Paneli"])
        if st.button("Kayıt"):
            new_data = pd.DataFrame([[nu, make_hashes(np), nr]], columns=['username', 'password', 'role'])
            new_data.to_csv(USER_DB, mode='a', header=False, index=False)
            st.success("Tamamdır!")

# --- ANA PANEL ---
else:
    st.sidebar.title("PRO-BUILD FULL")
    st.sidebar.write(f"**{st.session_state.username}**")
    if st.sidebar.button("Çıkış"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.user_role == "Usta Paneli":
        st.header("👷 Saha İş Bildirimi")
        yapilacak = [i["is"] for i in st.session_state.db if i["durum"] in ["Bekliyor", "Reddedildi"]]
        if yapilacak:
            s = st.selectbox("Bitirdiğiniz İş:", yapilacak)
            f = st.file_uploader("📷 Fotoğraf Yükle", type=['jpg','png','jpeg'])
            if st.button("Onaya Gönder") and f:
                for i in st.session_state.db:
                    if i["is"] == s:
                        i["durum"] = "Onay Bekliyor"
                        i["tarih"] = datetime.now().strftime("%d/%m %H:%M")
                veriyi_kaydet(st.session_state.db)
                st.success("Gönderildi!")
        else: st.info("Bekleyen iş yok.")

    else:
        st.header("📊 Şantiye Durum Özeti")
        df = pd.DataFrame(st.session_state.db)
       
        # Kaba ve İnce ilerleme çubukları
        kaba_biten = len(df[(df['etap'] == 'Kaba') & (df['durum'] == 'Tamamlandı')])
        ince_biten = len(df[(df['etap'] == 'İnce') & (df['durum'] == 'Tamamlandı')])
       
        st.write(f"**Kaba İnşaat İlerleme:** %{int(kaba_biten/6*100)}")
        st.progress(kaba_biten/6)
        st.write(f"**İnce İnşaat İlerleme:** %{int(ince_biten/14*100)}")
        st.progress(ince_biten/14)

        st.divider()
        st.dataframe(df, use_container_width=True)

        # Onay Merkezi
        onay_bekleyen = [i for i in st.session_state.db if i["durum"] == "Onay Bekliyor"]
        for ob in onay_bekleyen:
            with st.expander(f"ONAY BEKLİYOR: {ob['is']}"):
                c1, c2 = st.columns(2)
                if c1.button(f"ONAYLA - {ob['id']}", type="primary"):
                    ob["durum"] = "Tamamlandı"
                    veriyi_kaydet(st.session_state.db)
                    st.rerun()
                if c2.button(f"REDDET - {ob['id']}"):
                    ob["durum"] = "Reddedildi"
                    veriyi_kaydet(st.session_state.db)
                    st.rerun()




