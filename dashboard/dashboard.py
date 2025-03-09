import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("PRSA_Data_Cleaned.csv")

# Cleaning: Menghilangkan data NaN
df_cleaned = df.dropna()

# Menambahkan kolom kategori musim berdasarkan bulan
def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"

df_cleaned["Season"] = df_cleaned["month"].apply(get_season)

# Menambahkan kolom kategori untuk PM2.5 berdasarkan EPA standard
def categorize_pm25(value):
    if value <= 12:
        return "Baik"
    elif value <= 35:
        return "Sedang"
    elif value <= 55:
        return "Tidak Sehat (Sensitif)"
    elif value <= 150:
        return "Tidak Sehat"
    elif value <= 250:
        return "Sangat Tidak Sehat"
    else:
        return "Berbahaya"

df_cleaned["PM2.5 Category"] = df_cleaned["PM2.5"].apply(categorize_pm25)

# Menambahkan kolom kategori untuk PM10 berdasarkan EPA standard
def categorize_pm10(value):
    if value <= 54:
        return "Baik"
    elif value <= 154:
        return "Sedang"
    elif value <= 254:
        return "Tidak Sehat (Sensitif)"
    elif value <= 354:
        return "Tidak Sehat"
    elif value <= 424:
        return "Sangat Tidak Sehat"
    else:
        return "Berbahaya"

df_cleaned["PM10 Category"] = df_cleaned["PM10"].apply(categorize_pm10)

# Convert datetime

# Sidebar
st.sidebar.title("📌 Dashboard Analisis PM2.5 & PM10")
st.sidebar.write("Gunakan menu di bawah untuk menavigasi:")
menu = st.sidebar.selectbox("Pilih Analisis", ["Tren Waktu", "Pengaruh Curah Hujan", "Klasifikasi PM2.5 & PM10", "Pengaruh Faktor Meteorologi Berdasarkan Musim"])

#  Tren Waktu 
if menu == "Tren Waktu":
    st.title("Tren PM2.5 & PM10 Berdasarkan Waktu")

    # Tren Harian PM2.5 & PM10
    st.subheader("Rata-rata PM2.5 & PM10 per Jam")
    pm_hourly = df_cleaned.groupby("hour")[["PM2.5", "PM10"]].mean()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(x=pm_hourly.index, y=pm_hourly["PM2.5"], marker="o", color="purple", label="PM2.5", ax=ax)
    sns.lineplot(x=pm_hourly.index, y=pm_hourly["PM10"], marker="s", color="orange", label="PM10", ax=ax)
    ax.set_xlabel("Jam dalam Sehari")
    ax.set_ylabel("Konsentrasi (µg/m³)")
    ax.set_title("Rata-rata PM2.5 & PM10 per Jam")
    ax.grid(True)
    st.pyplot(fig)

    st.info("""
    ✅ **Insight**:  
    - **PM2.5 dan PM10 lebih tinggi pada pagi dan malam hari.**
    - Ini menunjukkan bahwa aktivitas manusia seperti transportasi dan industri berkontribusi terhadap kedua jenis polutan ini.
    """)

    # Tren Bulanan PM2.5 & PM10
    st.subheader("Rata-rata PM2.5 & PM10 per Bulan")
    pm_monthly = df_cleaned.groupby("month")[["PM2.5", "PM10"]].mean()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(x=pm_monthly.index, y=pm_monthly["PM2.5"], marker="o", color="red", label="PM2.5", ax=ax)
    sns.lineplot(x=pm_monthly.index, y=pm_monthly["PM10"], marker="s", color="blue", label="PM10", ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Konsentrasi (µg/m³)")
    ax.set_title("Rata-rata PM2.5 & PM10 per Bulan")
    ax.grid(True)
    st.pyplot(fig)

    st.info("""
    ✅ **Insight**:  
    - **Kedua polutan lebih tinggi selama musim dingin (Desember - Februari).**  
    - Ini kemungkinan disebabkan oleh pemanas ruangan dan kondisi cuaca yang memperangkap polutan.
    """)
    
    st.title("📈 Tren Tahunan PM2.5 & PM10")

    # Mengelompokkan data berdasarkan tahun dan menghitung rata-rata PM2.5 & PM10
    pm_yearly = df_cleaned.groupby("year")[["PM2.5", "PM10"]].mean()

    # Membuat Line Chart Tren Tahunan
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(x=pm_yearly.index, y=pm_yearly["PM2.5"], marker="o", color="purple", label="PM2.5", ax=ax)
    sns.lineplot(x=pm_yearly.index, y=pm_yearly["PM10"], marker="s", color="orange", label="PM10", ax=ax)

    # Customisasi Plot
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Konsentrasi (µg/m³)")
    ax.set_title("Tren Tahunan PM2.5 & PM10")
    ax.grid(True)
    ax.legend()

    # Tampilkan di Streamlit
    st.pyplot(fig)

    # Insight
    st.info("""
    ✅ **Insight:**  
    - Tren tahunan PM2.5 & PM10 menunjukkan fluktuasi dengan kecenderungan tertentu.  
    - Penurunan kadar PM2.5 dan PM10 dapat mencerminkan keberhasilan kebijakan lingkungan atau perubahan aktivitas manusia.  
    - Lonjakan pada tahun tertentu bisa disebabkan oleh cuaca ekstrem, kebakaran hutan, atau peningkatan aktivitas industri.  
    """)

#  Pengaruh Curah Hujan terhadap PM2.5 & PM10 
elif menu == "Pengaruh Curah Hujan":
    st.title("Pengaruh Curah Hujan terhadap PM2.5 & PM10")

    # Scatter plot PM2.5 vs Curah Hujan
    st.subheader("Hubungan Curah Hujan dengan PM2.5 & PM10")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=df_cleaned["RAIN"], y=df_cleaned["PM2.5"], alpha=0.5, color="blue", label="PM2.5", ax=ax)
    sns.scatterplot(x=df_cleaned["RAIN"], y=df_cleaned["PM10"], alpha=0.5, color="red", label="PM10", ax=ax)
    ax.set_xlabel("Curah Hujan (mm)")
    ax.set_ylabel("Konsentrasi (µg/m³)")
    ax.set_title("Hubungan antara Curah Hujan, PM2.5 & PM10")
    ax.grid(True)
    st.pyplot(fig)

    st.info("""
    ✅ **Insight**:  
    - **Saat curah hujan tinggi, kadar PM2.5 dan PM10 cenderung lebih rendah.**  
    - Ini menunjukkan bahwa hujan membantu membersihkan udara dari partikel polusi.
    """)

#  Klasifikasi PM2.5 & PM10 
elif menu == "Klasifikasi PM2.5 & PM10":
    st.title("📊 Klasifikasi Kualitas Udara")

    # Distribusi PM2.5
    st.subheader("🟢 Distribusi Kategori PM2.5")
    pm25_category_counts = df_cleaned["PM2.5 Category"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=pm25_category_counts.index, y=pm25_category_counts.values, palette="viridis", ax=ax)
    ax.set_xlabel("Kategori PM2.5")
    ax.set_ylabel("Jumlah Observasi")
    ax.set_title("Distribusi Kategori PM2.5")
    ax.set_xticklabels(pm25_category_counts.index, rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    # Distribusi PM10
    st.subheader("🔴 Distribusi Kategori PM10")
    pm10_category_counts = df_cleaned["PM10 Category"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=pm10_category_counts.index, y=pm10_category_counts.values, palette="magma", ax=ax)
    ax.set_xlabel("Kategori PM10")
    ax.set_ylabel("Jumlah Observasi")
    ax.set_title("Distribusi Kategori PM10")
    ax.set_xticklabels(pm10_category_counts.index, rotation=45)
    ax.grid(True)
    st.pyplot(fig)
    
    st.info("""
    ✅ **Insight**:  
    - Sebagian besar waktu, udara berada dalam kategori "Tidak Sehat" hingga "Sangat Tidak Sehat".
    - Hanya sedikit waktu di mana udara benar-benar "Baik" (PM2.5 < 12 µg/m³).
    - Menunjukkan bahwa tingkat polusi udara di Beijing sangat mengkhawatirkan.
    """)

elif menu == "Pengaruh Faktor Meteorologi Berdasarkan Musim":
    st.title("Pengaruh Faktor Meteorologi terhadap PM2.5 & PM10 Berdasarkan Musim")

    # Pilih Musim
    selected_season = st.selectbox("Pilih Musim:", ["Winter", "Spring", "Summer", "Autumn"])
    df_season = df_cleaned[df_cleaned["Season"] == selected_season]

    # Scatter Plot TEMP vs PM2.5 & PM10
    st.subheader(f"Suhu (TEMP) vs PM2.5 & PM10 - {selected_season}")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=df_season["TEMP"], y=df_season["PM2.5"], alpha=0.5, color="blue", label="PM2.5", ax=ax)
    sns.scatterplot(x=df_season["TEMP"], y=df_season["PM10"], alpha=0.5, color="red", label="PM10", ax=ax)
    ax.set_xlabel("Suhu (°C)")
    ax.set_ylabel("Konsentrasi (µg/m³)")
    ax.set_title(f"Hubungan Suhu terhadap PM2.5 & PM10 - {selected_season}")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Scatter Plot PRES vs PM2.5 & PM10
    st.subheader(f"Tekanan Udara (PRES) vs PM2.5 & PM10 - {selected_season}")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=df_season["PRES"], y=df_season["PM2.5"], alpha=0.5, color="blue", label="PM2.5", ax=ax)
    sns.scatterplot(x=df_season["PRES"], y=df_season["PM10"], alpha=0.5, color="red", label="PM10", ax=ax)
    ax.set_xlabel("Tekanan Udara (hPa)")
    ax.set_ylabel("Konsentrasi (µg/m³)")
    ax.set_title(f"Hubungan Tekanan Udara terhadap PM2.5 & PM10 - {selected_season}")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Scatter Plot WSPM vs PM2.5 & PM10
    st.subheader(f"Kecepatan Angin (WSPM) vs PM2.5 & PM10 - {selected_season}")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=df_season["WSPM"], y=df_season["PM2.5"], alpha=0.5, color="blue", label="PM2.5", ax=ax)
    sns.scatterplot(x=df_season["WSPM"], y=df_season["PM10"], alpha=0.5, color="red", label="PM10", ax=ax)
    ax.set_xlabel("Kecepatan Angin (m/s)")
    ax.set_ylabel("Konsentrasi (µg/m³)")
    ax.set_title(f"Hubungan Kecepatan Angin terhadap PM2.5 & PM10 - {selected_season}")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Korelasi Faktor Meteorologi Berdasarkan Musim
    st.subheader(f"Korelasi antara Faktor Meteorologi dan Polusi Udara - {selected_season}")
    fig, ax = plt.subplots(figsize=(8, 5))
    correlation = df_season[["PM2.5", "PM10", "TEMP", "PRES", "WSPM"]].corr()
    sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title(f"Heatmap Korelasi - {selected_season}")
    st.pyplot(fig)

    st.info(f"""
    ✅ **Insight Musim {selected_season}**:  
    - **Winter** → PM2.5 dan PM10 cenderung lebih tinggi karena efek inversi suhu.  
    - **Summer** → Polusi lebih rendah karena suhu tinggi dan kecepatan angin lebih tinggi.  
    - **Spring & Autumn** → Pola polusi sedang, dipengaruhi oleh transisi musim.  
    """)