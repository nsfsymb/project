import streamlit as st
import pandas as pd

# 페이지 기본 설정 및 와이드 모드 적용
st.set_page_config(
    page_title="강원생활도우미앱 3.0",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ 강원생활도우미앱 3.0 (통합 검색 지원 버전)")
st.markdown("---")

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
    tab1, tab2 = st.tabs(["📊 장소정보 시트", "📋 추천정보 시트"])
    with tab1:
        st.dataframe(place_df, use_container_width=True)
    with tab2:
        st.dataframe(recommend_df, use_container_width=True)


def show_joined_data(df):
    st.subheader("🔗 조인 완료된 통합 데이터")
    st.dataframe(df, use_container_width=True)


# ==========================================
# [기능 개선 및 확장 코드] - '전체' 선택 로직 반영
# ==========================================

def search_recommendations(df):
    st.subheader("🔍 맞춤형 추천 장소 검색 (조건에 '전체' 선택 가능)")

    # [개선] 각 선택 항목의 고유 값 리스트 앞에 "전체"를 추가합니다.
    regions = ["전체"] + list(df["지역"].dropna().unique())
    purposes = ["전체"] + list(df["추천목적"].dropna().unique())
    situations = ["전체"] + list(df["추천상황"].dropna().unique())
    targets = ["전체"] + list(df["추천대상"].dropna().unique())

    # 화면 구성 개선: 2열 레이아웃 배치
    col1, col2 = st.columns(2)
    with col1:
        selected_region = st.selectbox("📍 지역 선택", regions)
        selected_purpose = st.selectbox("🎯 추천목적 선택", purposes)
    with col2:
        selected_situation = st.selectbox("🎬 추천상황 선택", situations)
        selected_target = st.selectbox("👥 추천대상 선택", targets)

    selected_budget = st.number_input(
        "💰 최대 가용 예산 (원)",
        min_value=0,
        value=10000,
        step=1000
    )

    # [핵심 확장] '전체'를 선택했을 때의 필터링 우회 로직 설계
    # 기본적으로 예산 조건을 먼저 만족하는 데이터를 복사해온 뒤, 각 조건이 '전체'가 아닐 때만 필터를 누적 적용합니다.
    result = df[df["예산"] <= selected_budget]

    if selected_region != "전체":
        result = result[result["지역"] == selected_region]
        
    if selected_purpose != "전체":
        result = result[result["추천목적"] == selected_purpose]
        
    if selected_situation != "전체":
        result = result[result["추천상황"] == selected_situation]
        
    if selected_target != "전체":
        result = result[result["추천대상"] == selected_target]

    st.markdown("### 📋 검색 결과")

    if len(result) > 0:
        st.info(f"💡 조건에 맞는 장소를 총 {len(result)}개 찾았습니다. 정렬 기준을 선택해보세요.")
        
        # 정렬 옵션 위젯
        sort_option = st.radio(
            "🔽 원하는 정렬 방식을 선택하세요",
            ["기본 순서", "평점 높은 순 ⭐", "예산 낮은 순 💵"],
            horizontal=True
        )
        
        # 정렬 확장 함수 호출 및 결과 출력
        sorted_result = sort_places_data(result, sort_option)
        st.dataframe(sorted_result, use_container_width=True)
        
    else:
        st.warning("⚠️ 지정하신 조건에 맞는 추천 장소가 없습니다. 조건을 변경해 보세요.")


def show_chart(df):
    st.subheader("📈 데이터 시각화 분석")

    chart_option = st.selectbox(
        "📊 시각화 기준 열(Column) 선택",
        ["지역", "유형", "추천목적", "추천상황", "추천대상", "예약필요"]
    )

    chart_data = df[chart_option].value_counts()
    
    ccol1, ccol2 = st.columns([2, 1])
    with ccol1:
        st.bar_chart(chart_data)
    with ccol2:
        st.write("📋 **데이터 분포 요약**")
        st.dataframe(chart_data)


def sort_places_data(result_df, option):
    """
    [확장 기능] 사용자가 선택한 조건에 맞춰 결과를 정렬하여 반환하는 함수
    """
    sorted_df = result_df.copy()
    
    if option == "평점 높은 순 ⭐":
        if "평점" in sorted_df.columns:
            return sorted_df.sort_values(by="평점", ascending=False)
        else:
            st.error("데이터에 '평점' 열이 존재하지 않습니다.")
            
    elif option == "예산 낮은 순 💵":
        if "예산" in sorted_df.columns:
            return sorted_df.sort_values(by="예산", ascending=True)
        else:
            st.error("데이터에 '예산' 열이 존재하지 않습니다.")
            
    return sorted_df


# ==========================================
# [메인 실행 흐름 및 사이드바 레이아웃]
# ==========================================

with st.sidebar:
    st.title("메뉴 컨트롤러")
    uploaded_file = st.file_uploader(
        "📂 데이터베이스 엑셀 파일(.xlsx)",
        type=["xlsx"]
    )
    
    st.markdown("---")
    if uploaded_file is not None:
        menu = st.sidebar.radio(
            "🧭 바로가기 메뉴",
            ["🏠 원본 데이터 보기", "🔗 조인 데이터 보기", "🔍 추천 검색", "📊 데이터 시각화"]
        )

if uploaded_file is not None:
    place_df, recommend_df = load_data(uploaded_file)
    merged_df = join_data(place_df, recommend_df)

    if "🏠 원본 데이터 보기" in menu:
        show_original_data(place_df, recommend_df)

    elif "🔗 조인 데이터 보기" in menu:
        show_joined_data(merged_df)

    elif "🔍 추천 검색" in menu:
        search_recommendations(merged_df)

    elif "📊 데이터 시각화" in menu:
        show_chart(merged_df)
else:
    st.info("👋 시작하려면 왼쪽 사이드바에서 강원생활도우미 데이터가 들어있는 엑셀 파일(.xlsx)을 업로드해 주세요.")
