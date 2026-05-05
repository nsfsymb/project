import streamlit as st
import pandas as pd

st.title("강원생활도우미앱 2.0")
st.write("엑셀 파일을 업로드하면 장소 데이터를 확인할 수 있습니다.")

uploaded_file = st.file_uploader(
    "장소 데이터 엑셀 파일을 업로드하세요",
    type=["xlsx"]
)

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("업로드한 장소 데이터")
    st.dataframe(df)
else:
    st.info("엑셀 파일을 업로드하면 데이터가 표시됩니다.")
