import streamlit as st
import pandas as pd

st.title("강원생활도우미앱 3.0")


def load_data(uploaded_file):
    place_df = pd.read_excel(uploaded_file, sheet_name="장소정보")
    recommend_df = pd.read_excel(uploaded_file, sheet_name="추천정보")
    return place_df, recommend_df


def join_data(place_df, recommend_df):
    merged_df = pd.merge(
        recommend_df,
        place_df,
        on="place_id",
        how="left"
    )

    return merged_df


def show_joined_data(df):
    st.subheader("조인된 데이터")
    st.dataframe(df)

def search_recommendations(df):
    st.subheader("추천 장소 검색")

    selected_region = st.selectbox(
        "지역 선택",
        df["지역"].unique()
    )

    selected_purpose = st.selectbox(
        "추천목적 선택",
        df["추천목적"].unique()
    )

    selected_situation = st.selectbox(
        "추천상황 선택",
        df["추천상황"].unique()
    )

    selected_target = st.selectbox(
        "추천대상 선택",
        df["추천대상"].unique()
    )

    selected_budget = st.number_input(
        "최대 예산",
        min_value=0,
        value=10000,
        step=1000
    )

    result = df[
        (df["지역"] == selected_region) &
        (df["추천목적"] == selected_purpose) &
        (df["추천상황"] == selected_situation) &
        (df["추천대상"] == selected_target) &
        (df["예산"] <= selected_budget)
    ]

    st.subheader("검색 결과")

    if len(result) > 0:
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 추천 장소가 없습니다.")

uploaded_file = st.file_uploader(
    "엑셀 파일을 업로드하세요",
    type=["xlsx"]
)

if uploaded_file is not None:
    place_df, recommend_df = load_data(uploaded_file)
    merged_df = join_data(place_df, recommend_df)
    show_joined_data(merged_df)
