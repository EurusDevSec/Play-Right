import streamlit as st
import pandas as pd # import cac thu vien streamlit, pandas

st.set_page_config(layout="wide")
st.title("Crawl du lieu VnExpress")

df = pd.read_csv('vnexpress_advanced.csv')
st.subheader(f"hien thi {len(df)} bai viet da crawl: ")
N_COLS=3
cols = st.columns(N_COLS)
# duyet qua tung dong va cot
for index, row in df.iterrows():
# duyet qua tung dong 
    col_index = index % N_COLS
    with cols[col_index]:
# tao card cho tung bai
        with st.container(border=True): 
            if pd.notna(row['HinhAnh']) and row['HinhAnh'] != "":
                st.image(row['HinhAnh'], use_container_width=True) 
            
          
            st.markdown(f"**{row['TieuDe']}**") 
            st.write(f"[Đọc bài viết]({row['DuongDan']})")