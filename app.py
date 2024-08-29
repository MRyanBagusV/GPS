import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from streamlit_option_menu import option_menu

# Data sample untuk kendaraan
data_kendaraan = {
    'ID': [1, 2, 3],
    'Nama Kendaraan': ['Scoopy Prestige', 'Honda Brio', 'Kendaraan C'],
    'Latitude': [-6.200, -6.300, -6.400],
    'Longitude': [106.800, 106.900, 107.000],
    'Status': ['Aktif', 'Tidak Aktif', 'Aktif']
}

# Mengonversi data kendaraan ke DataFrame
df_kendaraan = pd.DataFrame(data_kendaraan)

# Konversi ke GeoDataFrame untuk visualisasi peta
gdf_kendaraan = gpd.GeoDataFrame(
    df_kendaraan, 
    geometry=gpd.points_from_xy(df_kendaraan.Longitude, df_kendaraan.Latitude),
    crs="EPSG:4326"
)

# Inisialisasi geocoder
geolocator = Nominatim(user_agent="gps_tracker_app")

def get_location_description(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language='id', timeout=10)
        if location:
            return location.address
        else:
            return "Deskripsi tidak tersedia"
    except GeocoderTimedOut:
        return "Waktu koneksi habis, coba lagi nanti"

# Judul aplikasi
st.title('Aplikasi GPS Tracker')

# Menu navigasi dengan ikon
selected_option = option_menu(
    menu_title=None,  # Tidak menampilkan judul menu
    options=["Pelacakan", "Profil", "Data Kendaraan"],  # Opsi menu
    icons=["geo-alt", "person", "car"],  # Ikon untuk setiap opsi
    menu_icon="cast",  # Ikon menu utama (opsional)
    default_index=0,  # Indeks default yang dipilih
    orientation="horizontal"  # Menampilkan menu secara horizontal
)

# Konten berdasarkan menu yang dipilih
if selected_option == "Pelacakan":
    st.header('Pelacakan Kendaraan')
    st.write("Pilih kendaraan untuk melihat lokasi saat ini.")
    
    kendaraan = st.selectbox('Pilih Kendaraan', df_kendaraan['Nama Kendaraan'])
    lokasi_kendaraan = df_kendaraan[df_kendaraan['Nama Kendaraan'] == kendaraan].iloc[0]
    
    st.write(f"Lokasi {kendaraan}:")
    st.write(f"Latitude: {lokasi_kendaraan['Latitude']}")
    st.write(f"Longitude: {lokasi_kendaraan['Longitude']}")
    
    # Mendapatkan deskripsi lokasi
    deskripsi_lokasi = get_location_description(lokasi_kendaraan['Latitude'], lokasi_kendaraan['Longitude'])
    st.write(f"Deskripsi Lokasi: {deskripsi_lokasi}")
    
    # Tampilkan peta
    map_data = pd.DataFrame({
        'lat': [lokasi_kendaraan['Latitude']],
        'lon': [lokasi_kendaraan['Longitude']]
    })
    st.map(map_data)

elif selected_option == "Profil":
    st.header('Profil Kendaraan')
    st.write("Masukkan ID kendaraan untuk melihat profil.")
    
    id_kendaraan = st.number_input('ID Kendaraan', min_value=1, max_value=len(df_kendaraan))
    if id_kendaraan:
        profil_kendaraan = df_kendaraan[df_kendaraan['ID'] == id_kendaraan].iloc[0]
        st.write(f"Nama Kendaraan: {profil_kendaraan['Nama Kendaraan']}")
        st.write(f"Status: {profil_kendaraan['Status']}")
        st.write(f"Latitude: {profil_kendaraan['Latitude']}")
        st.write(f"Longitude: {profil_kendaraan['Longitude']}")
        
        # Mendapatkan deskripsi lokasi
        deskripsi_lokasi = get_location_description(profil_kendaraan['Latitude'], profil_kendaraan['Longitude'])
        st.write(f"Deskripsi Lokasi: {deskripsi_lokasi}")

elif selected_option == "Data Kendaraan":
    st.header('Data Kendaraan')
    st.write(df_kendaraan)
