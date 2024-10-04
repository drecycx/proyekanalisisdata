import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

def load_data(filename):
    script_dir = os.path.dirname(__file__)  
    file_path = os.path.join(script_dir, filename)
    return pd.read_csv(file_path)

# Load both datasets
day_df = load_data('day_data.csv')
hour_df = load_data('hour_data.csv')

# Load data hasil cleaning di ipynb
def load_hour_data():
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    hour_df['yr'] = hour_df['yr'].map({0: 2011, 1: 2012})  #di sini terdapat perubahan karena yr merupakan kategori 0 = 2011 dan 1 = 2012
    return hour_df

def load_day_data():
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    day_df['yr'] = day_df['yr'].map({0: 2011, 1: 2012})  #di sini terdapat perubahan karena yr merupakan kategori 0 = 2011 dan 1 = 2012
    return day_df

# Sidebar untuk pilihan dataset
st.sidebar.header('Dataset')
data_type = st.sidebar.radio('Pilih Jenis Data', ('Hour Data', 'Day Data'))

# Pilihan untuk menampilkan jenis data
if data_type == 'Hour Data':
    df = load_hour_data()
else:
    df = load_day_data()

st.title(f'Dashboard Dataset Bike Sharing - {data_type}')
st.subheader('Marsella - m271b4kx2414@bangkit.academy')

# Sidebar untuk filtering
st.sidebar.header('Filters')
filteryear = st.sidebar.selectbox('Select Year', df['yr'].unique())
filterseason = st.sidebar.multiselect('Select Season', df['season'].unique(), default=df['season'].unique())

# Filter data
filtered_df = df[(df['yr'] == filteryear) & (df['season'].isin(filterseason))]

# Visualisasi jumlah sewa berdasarkan cuaca
st.header('Pengaruh Cuaca pada Penyewaan Sepeda')
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='weathersit', y='cnt', data=filtered_df, ax=ax)
ax.set_xlabel('Cuaca')
ax.set_ylabel('Total Penyewaan')
st.pyplot(fig)

# Seasonal trend
st.header('Pengaruh Musim pada Penyewaan Sepeda')
seasonal_rentals = filtered_df.groupby('season')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=seasonal_rentals, ax=ax)
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Total Penyewaan')
st.pyplot(fig)

# Korelasi Heatmap untuk atribut numerik
correlation_matrix = filtered_df[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
plt.figure(figsize=(5, 4))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='Purples', square=True)
plt.title('Korelasi Heatmap antar Atribut Numerik')
st.pyplot(plt)

# Time Series untuk melihat Peak Hour hanya untuk hour_data
if data_type == 'Hour Data':
    st.header('Rata-rata Penyewaan Sepeda berdasarkan Jam')
    rental_per_jam = filtered_df.groupby('hr')['cnt'].mean().reset_index()
    plt.figure(figsize=(10, 5))
    plt.plot(rental_per_jam['hr'], rental_per_jam['cnt'])
    plt.xlabel('Jam')
    plt.ylabel('Rata-rata')
    plt.xticks(range(0, 24))
    plt.grid(True, linestyle='--')
    st.pyplot(plt)
