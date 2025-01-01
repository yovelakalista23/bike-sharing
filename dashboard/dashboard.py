import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Bike Sharing Dashboard</h1>", unsafe_allow_html=True)
st.write("""
         Dashboard interaktif untuk menganalisis penggunaan sepeda berdasarkan beberapa kategori.
         Terdapat beberapa visualisasi, seperti:
         1. tren penggunaan sepeda berdasarkan musim 
         2. proporsi pengguna terdaftar dan kasual
         3. dan analisis penggunaan sepeda berdasarkan jam
         4. Rata-rata pengguna berdasarkan tahun
         5. Pola penggunaan terdaftar dan kasual berdasarkan musim
         """)

# Memuat Dataset
day_df = pd.read_csv("https://raw.githubusercontent.com/yovelakalista23/bike-sharing/refs/heads/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/yovelakalista23/bike-sharing/refs/heads/main/data/hour.csv")

# 1. jam pengguna tertinggi
# Kelompokkan data berdasarkan jam dan hitung total pengguna
hourly_usage = hour_df.groupby("hr")["cnt"].sum().reset_index()

# Cari jam dengan penggunaan tertinggi
peak_hour = hourly_usage.loc[hourly_usage["cnt"].idxmax()]

# Visualisasi bar chart
st.subheader("Penggunaan Sepeda Berdasarkan Jam")
plt.figure(figsize=(10, 6))
sns.barplot(x=hourly_usage["hr"], y=hourly_usage["cnt"], palette="viridis")
plt.xlabel("Jam", fontsize=12)
plt.ylabel("Jumlah Pengguna", fontsize=12)
plt.xticks(rotation=45)
plt.axhline(y=peak_hour["cnt"], color="red", linestyle="--", label=f"Peak Hour: {peak_hour['hr']}")
plt.legend()
st.pyplot(plt)

# membuat baris ke-2 dengan 2 kolom
col1, col2 = st.columns(2)

with col1:
    # 2. Apakah ada perbedaan penggunaan sepeda di tahun yang berbeda?
    # Kelompokkan data berdasarkan kolom 'yr' dan hitung rata-rata jumlah pengguna
    yearly = day_df.groupby("yr")["cnt"].mean().reset_index()
    yearly.columns = ["yr", "avg_cnt"]

    # Visualisasi bar chart
    st.subheader("Rata-Rata Penggunaan Sepeda Berdasarkan Tahun")
    plt.figure(figsize=(8, 5))
    plt.bar(yearly["yr"].astype(str), yearly["avg_cnt"], color=["skyblue", "orange"])
    plt.xlabel("Tahun", fontsize=12)
    plt.ylabel("Rata-Rata Pengguna", fontsize=12)
    plt.xticks(ticks=[0, 1], labels=["2011", "2012"], fontsize=10)
    st.pyplot(plt)


with col2:
    # 3. Apakah tren penggunaan berbeda berdasarkan musim?
    season = day_df.groupby("season")["cnt"].mean().round().reset_index()
    season.columns = ["season", "avg_cnt"]

    # Visualisasi rata-rata penggunaan sepeda berdasarkan musim
    st.subheader("Rata-rata Penggunaan Sepeda Berdasarkan Musim")
    plt.figure(figsize=(8, 6))
    sns.barplot(x="season", y="avg_cnt", data=season, palette=["skyblue", "pink", "yellow", "orange"])
    plt.xlabel("Musim", fontsize=12)
    plt.ylabel("Rata-rata Penggunaan Sepeda", fontsize=12)
    plt.xticks(ticks=[0, 1, 2, 3], labels=["Winter", "Spring", "Summer", "Fall"], fontsize=10)
    st.pyplot(plt)


# membuat baris ke-3 dengan 2 kolom
col3, col4 = st.columns(2)

with col3:
    # 4. Berapa proporsi pengguna terdaftar dibandingkan dengan pengguna kasual?
    # Total jumlah pengguna berdasarkan kategori
    total_registered = day_df["registered"].sum()
    total_casual = day_df["casual"].sum()

    # Hitung proporsi
    total_users = total_registered + total_casual
    registered_prop = (total_registered / total_users) * 100
    casual_prop = (total_casual / total_users) * 100

    # Data untuk pie chart
    labels = ['Registered', 'Casual']
    sizes = [registered_prop, casual_prop]
    colors = ['skyblue', 'lightcoral']
    explode = (0.1, 0)  # Membuat potongan untuk highlight

    # Pie chart
    st.subheader("Proporsi Pengguna Terdaftar vs Kasual")
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Memastikan pie chart berbentuk lingkaran
    st.pyplot(plt)


with col4:
    # Filter untuk memilih jenis pengguna
    user_type = st.selectbox("Pilih Jenis Pengguna", ["Registered", "Casual"])

    # Buat DataFrame untuk proporsi pengguna
    prop_df = pd.DataFrame({
    "category": ["registered", "casual"],
    "total": [total_registered, total_casual],
    "proportion": [registered_prop, casual_prop]
    })
    # Menyaring data sesuai dengan jenis pengguna yang dipilih
    if user_type == "Registered":
        user_data = day_df[['season', 'registered']]
        user_data['cnt'] = user_data['registered']
    else:
        user_data = day_df[['season', 'casual']]
        user_data['cnt'] = user_data['casual']
        # 5. Bagaimana pola penggunaan pengguna kasual dan terdaftar berdasarkan musim atau cuaca?
        # Kelompokkan data berdasarkan musim dan hitung rata-rata jumlah pengguna
        season_usage = day_df.groupby("season")[["casual", "registered"]].mean().reset_index()
        season_usage.columns = ["season", "avg_casual", "avg_registered"]

    # Menampilkan visualisasi berdasarkan pilihan jenis pengguna
    st.subheader(f"Total Penggunaan Sepeda oleh Pengguna {user_type}")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season', y='cnt', data=user_data, palette="coolwarm", ax=ax)
    ax.set_title(f"Penggunaan Sepeda oleh Pengguna {user_type} per Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penggunaan Sepeda")
    st.pyplot(fig)
    
# Footer
st.caption('Copyright (c) Yovela Kalista 2025')
    