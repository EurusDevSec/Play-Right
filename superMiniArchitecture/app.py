import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Crawl du lieu VnExpress")

df = pd.read_csv('vnexpress_data.csv')
st.subheader(f"hien thi {len(df)} bai viet da crawl: ")
for index, row in df.iterrows():
    with st.container(border=True):
        st.image(row['HinhAnh'])
        st.subheader(row['TieuDe'])
        st.write(f"[Doc bai viet]({row['DuongDan']})")