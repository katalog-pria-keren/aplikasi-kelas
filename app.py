import streamlit as st
from st_gsheets_connection import GSheetsConnection
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Sistem Kelas Pak Cecep", layout="wide")

st.title("🏫 Sistem Informasi Kelas Online")
st.subheader("Wali Kelas: Cecep Purkon, S.Pd.I")

# --- KONEKSI KE GOOGLE SHEETS ---
# Pastikan Bapak nanti memasukkan link Google Sheets di "Secrets" Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

# Fungsi ambil data dari Google Sheets
def ambil_data():
    try:
        # Mengambil data dari tab bernama 'Data_Siswa'
        return conn.read(worksheet="Data_Siswa", ttl="0")
    except:
        st.error("Gagal terhubung ke Google Sheets. Pastikan Nama Sheet benar dan Link sudah dimasukkan di Secrets.")
        return pd.DataFrame(columns=["Nama", "Hadir", "Sakit", "Izin"])

df_siswa = ambil_data()

# --- SIDEBAR MENU ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3449/3449692.png", width=100)
menu = st.sidebar.selectbox("Pilih Menu", ["Beranda", "Absensi Siswa", "Cek Nilai & Absensi", "Panel Guru (Admin)"])

# --- LOGIKA MENU ---
if menu == "Beranda":
    st.markdown("""
    ### Selamat Datang di Aplikasi Kelas!
    Aplikasi ini digunakan untuk:
    *   **Siswa:** Mengisi daftar hadir harian secara mandiri.
    *   **Siswa:** Memantau nilai dan persentase kehadiran.
    *   **Guru:** Mengelola data induk kelas secara terpusat.
    """)
    st.info("Siswa silakan pilih menu 'Absensi Siswa' untuk mengisi kehadiran hari ini.")

elif menu == "Absensi Siswa":
    st.header("📝 Form Absensi Mandiri")
    if not df_siswa.empty:
        nama = st.selectbox("Pilih Nama Anda", df_siswa["Nama"].tolist())
        status = st.radio("Keterangan", ["Hadir", "Izin", "Sakit"])
        
        if st.button("Kirim Laporan"):
            st.success(f"Terima kasih {nama}, laporan {status} Anda sudah masuk ke sistem Pak Cecep.")
            st.balloons()
    else:
        st.warning("Data siswa tidak ditemukan di Google Sheets.")

elif menu == "Cek Nilai & Absensi":
    st.header("📊 Pantau Nilai Mandiri")
    if not df_siswa.empty:
        cari_nama = st.selectbox("Masukkan Nama Anda", df_siswa["Nama"].tolist())
        data_pribadi = df_siswa[df_siswa["Nama"] == cari_nama]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Kehadiran", f"{data_pribadi['Hadir'].values[0]} Hari")
        with col2:
            st.write("**Detail Data:**")
            st.table(data_pribadi)
    else:
        st.warning("Data tidak tersedia.")

elif menu == "Panel Guru (Admin)":
    st.header("🔐 Area Wali Kelas")
    password = st.text_input("Masukkan Password Guru", type="password")
    if password == "admin123": # Silakan Bapak ganti passwordnya di sini
        st.success("Akses Diterima, Pak Cecep.")
        st.write("Berikut adalah data seluruh siswa:")
        st.dataframe(df_siswa)
        st.download_button("Download Data ke Excel", df_siswa.to_csv(), "data_kelas.csv")
    elif password != "":
        st.error("Password Salah!")
