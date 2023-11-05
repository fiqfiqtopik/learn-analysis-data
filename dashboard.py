import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import geodatasets
import folium
import streamlit as st
sns.set(style='dark')

def create_customers_abt_geolocation(df):
    customers_abt_geolocation = df.groupby(by="geolocation_city").agg({
        "customer_id": "nunique",
        "geolocation_lat": "mean",
        "geolocation_lng": "mean"
    }).reset_index()

    return customers_abt_geolocation

def create_total_orders_df(df):
    total_orders_df = df.groupby(by="product_category_name_english").order_item_id.nunique().sort_values(ascending=False).reset_index()
    total_orders_df.columns = ["product_category", "total_orders"]

    return total_orders_df

def create_ratings_df(df):
    ratings_df = df.groupby(by="review_score").order_id.count().sort_values(ascending=False).reset_index()
    ratings_df.columns = ["rating", "total_rate"]

    return ratings_df

customers_geolocation = pd.read_csv('D:\DataScience\MyProject(Ngulang)\E-CommercePublicDataset\dashboard\customers_geolocation_dataset.csv')
order_product_items_translated_df = pd.read_csv('D:\DataScience\MyProject(Ngulang)\E-CommercePublicDataset\dashboard\order_product_items_translated_df.csv')
order_reviews_df = pd.read_csv('D:\DataScience\MyProject(Ngulang)\E-CommercePublicDataset\data\order_reviews_dataset.csv')

customers_abt_geolocation = create_customers_abt_geolocation(customers_geolocation)
total_orders_df = create_total_orders_df(order_product_items_translated_df)
ratings_df = create_ratings_df(order_reviews_df)

st.header('Analisis E-Commerce Public Dataset')

st.subheader('Persebaran Customer Berdasarkan Kota')
m = folium.Map(location=[-14.2350, -51.9253], zoom_start=9)

for index, row in customers_abt_geolocation.iterrows():
    folium.Marker(
        location=[row["geolocation_lat"], row["geolocation_lng"]],
        popup=f"Kota: {row['geolocation_city']}<br>Jumlah Customer: {row['customer_id']}",
        icon=folium.Icon(icon="user")
    ).add_to(m)

m


st.subheader('Best & Worst Performing Product by Number of Sales')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

sns.barplot(data=total_orders_df.head(5), x="total_orders", y="product_category", hue="product_category", palette=["#72BCD4" if x == total_orders_df.total_orders.max() else "#D3D3D3" for x in total_orders_df.total_orders], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Category Product", loc="center", fontsize=15)
ax[0].tick_params(axis='y', labelsize=14)

sns.barplot(data=total_orders_df.sort_values(by="total_orders" ,ascending=True).head(5), x="total_orders", y="product_category", hue="product_category", palette=["#72BCD4" if x == total_orders_df.total_orders.max() else "#D3D3D3" for x in total_orders_df.total_orders], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Category Product", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=14)

st.pyplot(fig)


st.subheader('Sales Rating Product')
fig, ax = plt.subplots(figsize=(12, 6), subplot_kw=dict(aspect="equal"))

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return f"{pct:.1f}%\n({absolute:d} rate)"

wedges, texts, autotexts = ax.pie(ratings_df.total_rate, autopct=lambda pct: func(pct, ratings_df.total_rate),
                                  textprops=dict(color="w"))

ax.legend(wedges, ratings_df.rating,
          title="Rating",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")
st.pyplot(fig)

st.caption('Copyright (c) Dicoding 2023')