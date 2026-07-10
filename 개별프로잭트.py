import streamlit as st
import pandas as pd

# 페이지 기본 설정 및 와이드 모드 적용 (화면 구성 개선)
st.set_page_config(
    page_title="강원생활도우미앱",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ 강원생활도우미앱 3.0 (개별 프로젝트)")
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
    # 화면 구성 개선: 탭(Tab)을 활용하여 화면을 깔끔하게 분할
    tab1, tab2 = st.tabs(["📊 장소정보 시트", "📋 추천정보 시트"])
    with tab1:
        st.dataframe(place_df, use_container_width=True)
    with tab2:
        st.dataframe(recommend_df, use_container_width=True)


def show_joined_data(df):
    st.subheader("🔗 조인 완료된 통합 데이터")
    st.dataframe(df, use_container_width=True)


def search_recommendations(df):
    st.subheader("🔍 맞춤형 추천 장소 검색")

    # 화면 구성 개선: selectbox들을 한눈에 들어오도록 2열(Columns) 레이아웃으로 배치
    col1, col2 = st.columns(2)
    with col1:
        selected_region = st.selectbox("📍 지역 선택", df["지역"].unique())
        selected_purpose = st.selectbox("🎯 추천목적 선택", df["추천목적"].unique())
    with col2:
        selected_situation = st.selectbox("🎬 추천상황 선택", df["추천상황"].unique())
        selected_target = st.selectbox("👥 추천대상 선택", df["추천대상"].unique())

    selected_budget = st.number_input(
        "💰 최대 가용 예산 (원)",
        min_value=0,
        value=10000,
        step=1000
    )

    # 1차 필터링 수행
    result = df[
        (df["지역"] == selected_region) &
        (df["추천목적"] == selected_purpose) &
        (df["추천상황"] == selected_situation) &
        (df["추천대상"] == selected_target) &
        (df["예산"] <= selected_budget)
    ]

    st.markdown("### 📋 검색 결과")

    if len(result) > 0:
        # ----------------------------------------------------
        # [접점 / 인터페이스 연결] 
        # 기존 코드를 깨뜨리지 않고, 검색 결과가 있을 때 새 확장 함수를 자연스럽게 결합
        # ----------------------------------------------------
        st.info(f"💡 조건에 맞는 장소를 총 {len(result)}개 찾았습니다. 정렬 기준을 선택해보세요.")
        
        # 신규 확장 기능인 '정렬 옵션 위젯' 배치
        sort_option = st.radio(
            "🔽 원하는 정렬 방식을 선택하세요",
            ["기본 순서", "평점 높은 순 ⭐", "예산 낮은 순 💵"],
            horizontal=True
        )
        
        # 신규 확장 함수 호출 및 결과 출력
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
    
    # 화면 구성 개선: 차트와 요약 수치를 좌우 배치로 깔끔하게 정돈
    ccol1, ccol2 = st.columns([2, 1])
    with ccol1:
        st.bar_chart(chart_data)
    with ccol2:
        st.write("📋 **데이터 분포 요약**")
        st.dataframe(chart_data)


# ==========================================
# [신규 확장 코드] - 정렬 및 품질 보증을 위한 독립 함수
# ==========================================

def sort_places_data(result_df, option):
    """
    [확장 기능] 사용자가 선택한 조건에 맞춰 결과를 정렬하여 반환하는 함수
    - 제약조건: 원본 데이터프레임을 안전하게 유지하기 위해 .copy() 사용
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

# 사이드바 화면 구성 개선
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1621259182978-f09e5e24d90d?q=80&w=200", width=100) # 가상의 강원 지도/여가 이미지 플레이스홀더
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

# 파일 업로드 성공 후 처리
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
    # 파일을 아직 올리지 않았을 때 안내 화면 디자인 개선
    st.info("👋 시작하려면 왼쪽 사이드바에서 강원생활도우미 데이터가 들어있는 엑셀 파일(.xlsx)을 업로드해 주세요.")
