import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Data sample untuk kendaraan
data_kendaraan = {
    'ID': [1, 2, 3],
    'Nama Kendaraan': ['Kendaraan A', 'Kendaraan B', 'Kendaraan C'],
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

# Judul aplikasi
st.title('Aplikasi GPS Tracker')

# Sidebar untuk navigasi
st.sidebar.title('Navigasi')
option = st.sidebar.selectbox('Pilih Menu', ['Pelacakan', 'Profil', 'Data Kendaraan'])

# Menu Pelacakan
if option == 'Pelacakan':
    st.header('Pelacakan Kendaraan')
    st.write("Pilih kendaraan untuk melihat lokasi saat ini.")
    
    kendaraan = st.selectbox('Pilih Kendaraan', df_kendaraan['Nama Kendaraan'])
    lokasi_kendaraan = df_kendaraan[df_kendaraan['Nama Kendaraan'] == kendaraan].iloc[0]
    
    st.write(f"Lokasi {kendaraan}:")
    st.write(f"Latitude: {lokasi_kendaraan['Latitude']}")
    st.write(f"Longitude: {lokasi_kendaraan['Longitude']}")
    
    # Tampilkan peta
    map_data = pd.DataFrame({
        'lat': [lokasi_kendaraan['Latitude']],
        'lon': [lokasi_kendaraan['Longitude']]
    })
    st.map(map_data)

# Menu Profil
elif option == 'Profil':
    st.header('Profil Kendaraan')
    st.write("Masukkan ID kendaraan untuk melihat profil.")
    
    id_kendaraan = st.number_input('ID Kendaraan', min_value=1, max_value=len(df_kendaraan))
    if id_kendaraan:
        profil_kendaraan = df_kendaraan[df_kendaraan['ID'] == id_kendaraan].iloc[0]
        st.write(f"Nama Kendaraan: {profil_kendaraan['Nama Kendaraan']}")
        st.write(f"Status: {profil_kendaraan['Status']}")
        st.write(f"Latitude: {profil_kendaraan['Latitude']}")
        st.write(f"Longitude: {profil_kendaraan['Longitude']}")

# Menu Data Kendaraan
elif option == 'Data Kendaraan':
    st.header('Data Kendaraan')
    st.write(df_kendaraan)

# Menjalankan aplikasi Streamlit
if __name__ == "__main__":
    st.write("Aplikasi GPS Tracker berjalan...")
