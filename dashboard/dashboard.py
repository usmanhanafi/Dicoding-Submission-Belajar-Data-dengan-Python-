import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    return pd.read_csv('all_data.csv')

data = load_data()

st.title("Dashboard Analisis Data E-commerce")

# st.subheader("Data yang Digabungkan")
# st.dataframe(data)

st.subheader("Total Transaksi dalam Bulan Terakhir")

total_transactions = data['order_id'].nunique()
st.write(f"Total transaksi: {total_transactions}")

st.subheader("Distribusi Pelanggan Berdasarkan Negara Bagian")
state_counts = data['customer_state'].value_counts()
st.bar_chart(state_counts)

st.subheader("Pendapatan Tertinggi per Produk")
data['total_revenue'] = data['price'] * data['freight_value']
revenue_per_product = data.groupby('product_id')['total_revenue'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='total_revenue', y='product_id', data=revenue_per_product.sort_values('total_revenue', ascending=False).head(10), palette='viridis')
plt.title('Produk dengan Pendapatan Tertinggi')
plt.xlabel('Total Pendapatan')
plt.ylabel('ID Produk')
st.pyplot(plt)

if __name__ == "__main__":
    st.sidebar.title("Menu")
    st.sidebar.write("Selamat datang di dashboard analisis data e-commerce!")
