import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

@st.cache_data
def load_data():
    try:
        return pd.read_csv(os.getcwd() + '/dashboard/all_data.csv')
    except FileNotFoundError as e:
        st.error(f"File tidak ditemukan: {e}")
    except pd.errors.ParserError as e:
        st.error(f"Error parsing CSV: {e}")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

data = load_data()
product_df = data[['product_id', 'product_category_name']].drop_duplicates() 
order_items_df = data[['order_id', 'product_id', 'price', 'freight_value']]
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'], errors='coerce')

st.title("Dashboard Analisis Data E-commerce")

st.sidebar.title("Menu")
available_years = data['order_purchase_timestamp'].dt.year.dropna().astype(int).unique().tolist()
available_years.sort(reverse=True)  # Sortir dari yang terbaru

selected_year = st.sidebar.selectbox("Pilih Tahun:", available_years)

filtered_data_by_year = data[data['order_purchase_timestamp'].dt.year == selected_year]

selected_state = st.sidebar.multiselect(
    "Pilih Negara Bagian:", 
    options=data['customer_state'].dropna().unique(),
    default=data['customer_state'].dropna().unique()
)

filtered_data = data[data['customer_state'].isin(selected_state)]

# Analisis jumlah transaksi per bulan
monthly_transactions = filtered_data_by_year.groupby(filtered_data_by_year['order_purchase_timestamp'].dt.month).size()
monthly_transactions = monthly_transactions.reindex(range(1, 13), fill_value=0)

# Menampilkan total transaksi
total_transaksi = filtered_data_by_year['order_id'].nunique()
st.subheader(f"Total Transaksi pada Tahun {selected_year} : {total_transaksi}")

bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

# Visualisasi data total transaksi perbulan pada setiap tahunnya(tahun terakhir)
fig, ax = plt.subplots()
sns.lineplot(x=monthly_transactions.index, y=monthly_transactions.values, marker='o', ax=ax)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(bulan, rotation=45)
ax.set_title(f'Jumlah Transaksi per Bulan pada Tahun {selected_year}')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Transaksi')

# Visualisasi data distribusi pelanggan berdasarkan negara bagian
st.pyplot(fig)
st.subheader("Distribusi Pelanggan Berdasarkan Negara Bagian")
state_counts = filtered_data['customer_state'].value_counts()
st.bar_chart(state_counts)
