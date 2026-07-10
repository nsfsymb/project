import streamlit as st
import pandas as pd

st.title("강원생활도우미앱 (개별 프로젝트)")

# ==========================================
# [기존 레거시 코드] - 안전하게 보존
# ==========================================

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
        
        # ----------------------------------------------------
        # [접점 / 인터페이스 연결] 
        # 기존 코드를 수정하지 않고, 검색 결과가 존재할 때 확장 기능을 하단에 호출.
        st.markdown("---")
        st.subheader("가성비 기반 TOP 추천")
        
        # 가성비 추천을 받을 개수 선택 위젯
        top_n = st.slider("상위 몇 개의 가성비 장소를 볼까요?", min_value=1, max_value=max(1, len(result)), value=3)
        
        # 신규 확장 함수 호출
        enhanced_result = calculate_cost_effectiveness(result, top_n)
        st.dataframe(enhanced_result)
        
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


# ==========================================
# [신규 확장 코드] - SDD에 기반한 새 함수 정의

def calculate_cost_effectiveness(result_df, top_n):
    """
    [확장 기능] 가성비 점수를 계산하고 상위 N개를 정렬하여 반환하는 함수
    - 제약조건: 기존 result_df 원본을 훼손하지 않기 위해 .copy() 사용
    - 제약조건: 예산이 0인 경우 나눗셈 에러 방지 (예산 + 1)
    """
# 원본 데이터 보호를 위한 카피
    extended_df = result_df.copy()
    
    # 데이터 개수 확인
    available_count = len(extended_df)
    
    if "평점" in extended_df.columns and "예산" in extended_df.columns:
        # 가성비 점수 산출 (예산 0원 나눗셈 방지 처리)
        extended_df["가성비_점수"] = round(
            extended_df["평점"] / (extended_df["예산"] + 1) * 1000, 2
        )
        # 가성비 점수 기준 내림차순 정렬
        extended_df = extended_df.sort_values(by="가성비_점수", ascending=False)
        
        # 만약 실제 결과 개수가 사용자가 원하는 개수보다 적다면 안내하기
        if available_count < top_n:
            st.info(f"💡 해당 조건을 만족하는 장소가 총 {available_count}개뿐이므로, 검색된 모든 장소를 가성비 순으로 표시합니다.")
            return extended_df
        else:
            return extended_df.head(top_n)
    else:
        st.error("데이터에 '평점' 또는 '예산' 열이 존재하지 않아 가성비를 계산할 수 없습니다.")
        return extended_df


# ==========================================
# [메인 실행 흐름]

uploaded_file = st.file_uploader(
    "엑셀 파일을 업로드하세요",
    type=["xlsx"]
)

if uploaded_file is not None:
    place_df, recommend_df = load_data(uploaded_file)
    merged_df = join_data(place_df, recommend_df)

    menu = st.sidebar.radio(
        "메뉴 선택",
        ["원본 데이터 보기", "조인 데이터 보기", "추천 검색", "데이터 시각화"]
    )

    if menu == "원본 데이터 보기":
        show_original_data(place_df, recommend_df)

    elif menu == "조인 데이터 보기":
        show_joined_data(merged_df)

    elif menu == "추천 검색":
        search_recommendations(merged_df)

    elif menu == "데이터 시각화":
        show_chart(merged_df)
