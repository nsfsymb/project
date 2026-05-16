import streamlit as st
import pandas as pd

def load_data(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df

def show_data(df):
    st.subheader("업로드된 장소 목록")
    st.dataframe(df)

st.title("강원생활도우미 앱 2.0")
st.write("엑셀 파일을 업로드 할 수 있습니다.")

uploaded_file = st.file_uploader(
    "장소 데이터 엑셀 파일을 업로드해주세요.",
    type=["xlsx"]
)

if uploaded_file is not None:
    df = load_data(uploaded_file)
    show_data(df)
