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


def show_original_data(place_df, recommend_df):
    st.subheader("장소정보 시트")
    st.dataframe(place_df)

    st.subheader("추천정보 시트")
    st.dataframe(recommend_df)


def show_joined_data(df):
    st.subheader("조인된 데이터")
    st.dataframe(df)


def search_recommendations(df):
    st.subheader("추천 장소 검색")

    selected_region = st.selectbox("지역 선택", df["지역"].unique())
    selected_purpose = st.selectbox("추천목적 선택", df["추천목적"].unique())
    selected_situation = st.selectbox("추천상황 선택", df["추천상황"].unique())
    selected_target = st.selectbox("추천대상 선택", df["추천대상"].unique())

    selected_budget = st.number_input(
        "최대 예산",
        min_value=0,
        value=10000,
        step=1000
    )

    min_rating = st.number_input(
        "최소 평점 선택",
        min_value=0.0,
        max_value=5.0,
        value=0.0,
        step=0.1
    )

    need_reservation = st.selectbox(
        "예약 필요 여부",
        ["전체"] + list(df["예약필요"].dropna().unique())
    )

    max_time = st.number_input(
        "최대 소요 시간 (분)",
        min_value=0,
        value=180,
        step=10
    )

    condition = (
        (df["지역"] == selected_region) &
        (df["추천목적"] == selected_purpose) &
        (df["추천상황"] == selected_situation) &
        (df["추천대상"] == selected_target) &
        (df["예산"] <= selected_budget)
    )

    if "평점" in df.columns:
        condition = condition & (df["평점"] >= min_rating)

    time_col = None
    for col in df.columns:
        if "소요시간" in col:
            time_col = col
            break

    if time_col:
        condition = condition & (df[time_col] <= max_time)

    if need_reservation != "전체":
        condition = condition & (df["예약필요"] == need_reservation)

    result = df[condition]

    st.subheader("검색 결과")

    if len(result) > 0:
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 추천 장소가 없습니다.")


def show_chart(df):
    st.subheader("데이터 시각화")

    chart_option = st.selectbox(
        "시각화 기준 선택",
        ["지역", "유형", "추천목적", "추천상황", "추천대상", "예약필요"]
    )

    chart_data = df[chart_option].value_counts()

    st.bar_chart(chart_data)


def show_summary_dashboard(df):
    st.subheader("장소 등록 현황")
    
    name_col = "장소명" if "장소명" in df.columns else ("장소이름" if "장소이름" in df.columns else "place_id")
    unique_places = df.drop_duplicates(subset=[name_col])
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"등록된 총 장소 수: {len(unique_places)}곳")
    with col2:
        st.success(f"예약이 필요한 장소 수: {len(unique_places[unique_places['예약필요'] == 'Y'])}곳")
        
    st.markdown("---")
    st.subheader("등록된 장소 전체 요약 정보")
    available_cols = [col for col in [name_col, "지역", "유형", "예약필요", "한줄소개"] if col in df.columns]
    st.dataframe(unique_places[available_cols])


uploaded_file = st.file_uploader(
    "엑셀 파일을 업로드하세요",
    type=["xlsx"]
)

if uploaded_file is not None:
    place_df, recommend_df = load_data(uploaded_file)
    merged_df = join_data(place_df, recommend_df)

    menu = st.sidebar.radio(
        "메뉴 선택",
        [
            "등록 현황 대시보드", 
            "원본 데이터 보기", 
            "조인 데이터 보기", 
            "추천 검색", 
            "데이터 시각화"
        ]
    )

    if menu == "등록 현황 대시보드":
        show_summary_dashboard(merged_df)

    elif menu == "원본 데이터 보기":
        show_original_data(place_df, recommend_df)

    elif menu == "조인 데이터 보기":
        show_joined_data(merged_df)

    elif menu == "추천 검색":
        search_recommendations(merged_df)

    elif menu == "데이터 시각화":
        show_chart(merged_df)
