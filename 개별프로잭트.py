import streamlit as st
import pandas as pd

# 웹브라우저 탭 설정하고 화면 넓게 쓰게 지정함
st.set_page_config(
    page_title="강원생활도우미앱 3.0",
    layout="wide"
)

# 메인 제목 출력하는 코드임
st.title("강원생활도우미앱 3.0")
st.markdown("---")

# 기존 코드 - 수정 안 하고 그대로 보존한 영역

def load_data(uploaded_file):
    # 장소정보 시트랑 추천정보 시트를 각각 읽어옴
    place_df = pd.read_excel(uploaded_file, sheet_name="장소정보")
    recommend_df = pd.read_excel(uploaded_file, sheet_name="추천정보")
    # 읽어온 데이터 두 개를 반환함
    return place_df, recommend_df


def join_data(place_df, recommend_df):
    # place_id 열을 기준으로 두 테이블을 하나로 합쳐줌
    merged_df = pd.merge(
        recommend_df,
        place_df,
        on="place_id",
        how="left"
    )
    # 결합된 데이터프레임을 반환함
    return merged_df


def show_original_data(place_df, recommend_df):
    # 화면 분할용 탭 두 개를 만듦
    tab1, tab2 = st.tabs(["장소정보 시트", "추천정보 시트"])
    # 첫 번째 탭에 장소 정보 표를 띄워줌
    with tab1:
        st.dataframe(place_df, use_container_width=True)
    # 두 번째 탭에 추천 조건 표를 띄워줌
    with tab2:
        st.dataframe(recommend_df, use_container_width=True)


def show_joined_data(df):
    # 조인 완료된 전체 데이터를 표로 보여줌
    st.subheader("조인 완료된 통합 데이터")
    st.dataframe(df, use_container_width=True)


def show_chart(df):
    # 통계 기준을 고르는 상자를 만듦
    st.subheader("데이터 시각화 분석")
    chart_option = st.selectbox(
        "시각화 기준 열 선택",
        ["지역", "유형", "추천목적", "추천상황", "추천대상", "예약필요"]
    )
    # 선택한 열의 값 개수를 종류별로 세어줌
    chart_data = df[chart_option].value_counts()
    
    # 화면을 좌우 2:1 비율로 나눔
    ccol1, ccol2 = st.columns([2, 1])
    # 왼쪽에 막대그래프를 그려줌
    with ccol1:
        st.bar_chart(chart_data)
    # 오른쪽에 수치 요약 표를 보여줌
    with ccol2:
        st.write("데이터 분포 요약")
        st.dataframe(chart_data)

# 신규 기능 및 접점 코드 - 전체 검색이랑 정렬 기능 영역임

def search_recommendations(df):
    st.subheader("맞춤형 추천 장소 검색")

    # 각 항목 고유 값 목록 맨 앞에 "전체" 텍스트를 붙여줌
    regions = ["전체"] + list(df["지역"].dropna().unique())
    purposes = ["전체"] + list(df["추천목적"].dropna().unique())
    situations = ["전체"] + list(df["추천상황"].dropna().unique())
    targets = ["전체"] + list(df["추천대상"].dropna().unique())

    # 화면을 좌우 2열로 배치함
    col1, col2 = st.columns(2)
    # 왼쪽에 지역이랑 목적 선택 상자를 띄움
    with col1:
        selected_region = st.selectbox("지역 선택", regions)
        selected_purpose = st.selectbox("추천목적 선택", purposes)
    # 오른쪽에 상황이랑 대상 선택 상자를 띄움
    with col2:
        selected_situation = st.selectbox("추천상황 선택", situations)
        selected_target = st.selectbox("추천대상 선택", targets)

    # 가용 예산을 입력받는 칸을 만듦
    selected_budget = st.number_input(
        "최대 가용 예산 (원)",
        min_value=0,
        value=10000,
        step=1000
    )

    # 입력한 예산 이하인 데이터를 1차로 걸러냄
    result = df[df["예산"] <= selected_budget]

    # "전체"가 아닐 때만 해당 조건으로 필터링을 적용함
    if selected_region != "전체":
        result = result[result["지역"] == selected_region]
    if selected_purpose != "전체":
        result = result[result["추천목적"] == selected_purpose]
    if selected_situation != "전체":
        result = result[result["추천상황"] == selected_situation]
    if selected_target != "전체":
        result = result[result["추천대상"] == selected_target]

    st.markdown("### 검색 결과")

    # 걸러진 데이터가 존재하는지 확인함
    if len(result) > 0:
        # 데이터 개수를 안내창으로 띄움
        st.info(f"조건에 맞는 장소를 총 {len(result)}개 찾았습니다.")
        
        # 정렬 기준을 고르는 라디오 버튼을 만듦
        sort_option = st.radio(
            "원하는 정렬 방식을 선택하세요",
            ["기본 순서", "평점 높은 순", "예산 낮은 순"],
            horizontal=True
        )
        
        # 결과 데이터랑 정렬 옵션을 신규 정렬 함수로 넘겨줌
        sorted_result = sort_places_data(result, sort_option)
        # 정렬된 최종 데이터를 표로 띄움
        st.dataframe(sorted_result, use_container_width=True)
    else:
        # 데이터가 없으면 경고창을 띄움
        st.warning("지정하신 조건에 맞는 추천 장소가 없습니다. 조건을 변경해 보세요.")


def sort_places_data(result_df, option):
    # 원본 데이터 손상을 막기 위해 복사본을 만듦
    sorted_df = result_df.copy()
    
    # 평점 높은 순을 골랐을 때 작동함
    if option == "평점 높은 순":
        if "평점" in sorted_df.columns:
            # 평점 기준으로 내림차순 정렬해서 반환함
            return sorted_df.sort_values(by="평점", ascending=False)
            
    # 예산 낮은 순을 골랐을 때 작동함
    elif option == "예산 낮은 순":
        if "예산" in sorted_df.columns:
            # 예산 기준으로 오름차순 정렬해서 반환함
            return sorted_df.sort_values(by="예산", ascending=True)
            
    # 아무것도 해당 안 되면 그대로 돌려줌
    return sorted_df


# ==========================================
# [메인 실행 흐름] - 전체 실행을 제어하는 영역임
# ==========================================

# 사이드바 영역을 정의함
with st.sidebar:
    st.title("메뉴 컨트롤러")
    # 엑셀 파일을 올리는 칸을 만듦
    uploaded_file = st.file_uploader("데이터베이스 엑셀 파일(.xlsx)", type=["xlsx"])
    st.markdown("---")
    # 파일이 들어왔을 때만 메뉴를 보여줌
    if uploaded_file is not None:
        menu = st.sidebar.radio(
            "바로가기 메뉴",
            ["원본 데이터 보기", "조인 데이터 보기", "추천 검색", "데이터 시각화"]
        )

# 파일이 업로드되었을 때 실행함
if uploaded_file is not None:
    # 데이터 로드 함수를 실행해서 시트 두 개를 가져옴
    place_df, recommend_df = load_data(uploaded_file)
    # 두 시트 데이터를 하나로 합쳐줌
    merged_df = join_data(place_df, recommend_df)

    # 누른 메뉴에 따라 함수를 실행함
    if menu == "원본 데이터 보기":
        show_original_data(place_df, recommend_df)
    elif menu == "조인 데이터 보기":
        show_joined_data(merged_df)
    elif menu == "추천 검색":
        search_recommendations(merged_df)
    elif menu == "데이터 시각화":
        show_chart(merged_df)
else:
    # 파일이 없으면 안내창을 띄움
    st.info("시작하려면 왼쪽 사이드바에서 엑셀 파일을 업로드해 주세요.")
