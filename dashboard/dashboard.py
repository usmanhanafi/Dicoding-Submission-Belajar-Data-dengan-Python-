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

st.title("Dashboard Analisis Data E-commerce")

st.sidebar.title("Menu")
selected_state = st.sidebar.multiselect("Pilih Negara Bagian:", options=data['customer_state'].unique(), default=data['customer_state'].unique())

product_categories = product_df['product_category_name'].unique().tolist()
product_categories.insert(0, 'Pilih Semua') 

selected_category = st.sidebar.selectbox("Pilih Kategori Produk:", options=product_categories)

revenue_range = st.sidebar.slider("Pilih Rentang Pendapatan:", min_value=0.0, max_value=order_items_df['price'].sum() + order_items_df['freight_value'].sum(), value=(0.0, order_items_df['price'].sum() + order_items_df['freight_value'].sum()))

filtered_data = data[data['customer_state'].isin(selected_state)]

if selected_category == 'Pilih Semua':
    filtered_order_items = order_items_df[(order_items_df['price'] + order_items_df['freight_value'] >= revenue_range[0]) & (order_items_df['price'] + order_items_df['freight_value'] <= revenue_range[1])]
else:
    filtered_order_items = order_items_df[(order_items_df['product_id'].isin(product_df[product_df['product_category_name'] == selected_category]['product_id'])) & (order_items_df['price'] + order_items_df['freight_value'] >= revenue_range[0]) & (order_items_df['price'] + order_items_df['freight_value'] <= revenue_range[1])]

st.subheader("Total Transaksi dalam Bulan Terakhir")

total_transactions = filtered_order_items['order_id'].nunique()
st.write(f"Total transaksi: {total_transactions}")

st.subheader("Distribusi Pelanggan Berdasarkan Negara Bagian")
state_counts = filtered_data['customer_state'].value_counts()
st.bar_chart(state_counts)

st.subheader("Pendapatan Tertinggi per Produk")

filtered_order_items['total_revenue'] = filtered_order_items['price'] + filtered_order_items['freight_value'] 
revenue_per_product = filtered_order_items.groupby('product_id')['total_revenue'].sum().reset_index()

merged_data = pd.merge(revenue_per_product, product_df, on='product_id', how='left')

def format_currency(value):
    return f"${value:,.2f}" 

merged_data['formatted_revenue'] = merged_data['total_revenue'].apply(format_currency)

plt.figure(figsize=(10, 6))
top_products = merged_data.sort_values('total_revenue', ascending=False).head(10)

sns.barplot(x='total_revenue', y='product_category_name', data=top_products, palette='viridis')
plt.title('Produk dengan Pendapatan Tertinggi')
plt.xlabel('Total Pendapatan (dollar)')
plt.ylabel('Nama Kategori Produk') 
st.pyplot(plt)


if __name__ == "__main__":
    st.sidebar.write("Selamat datang di dashboard analisis data e-commerce!")
