import streamlit as st
import pandas as pd

def load_file():
    uploaded_file = st.file_uploader("장소 데이터 엑셀 파일을 업로드하세요", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        return df
    else:
        st.info("엑셀 파일을 업로드하면 데이터가 표시됩니다")
        return None

def print_table(table, table_name):
    st.subheader(table_name)
    if table is not None and len(table) > 0:
        st.dataframe(table)
    else:
        st.warning("출력할 장소가 없습니다")

def get_user_input(df):
    selected_region = st.selectbox("지역을 선택하세요", df["지역"].unique())
    selected_budget = st.number_input("사용 가능한 예산을 입력하세요", min_value=0, value=10000, step=1000)
    result = df[
        (df["지역"] == selected_region) &
        (df["예산"] <= selected_budget)
    ]
    return result

def show_filter_places(result, df):
    if len(result) > 0:
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 장소가 없습니다.")

def count_chart(df, key):
    key_count = df[key].value_counts()
    st.subheader(key + "별 장소 개수")
    st.bar_chart(key_count)

def average_chart(df, group, num):
    avg_score = df.groupby(group)[num].mean()
    st.subheader(group + "별 평균 " + num)
    st.bar_chart(avg_score)

def add_region_ui():
    st.subheader("새로운 장소 및 지역 추가")
    
    new_region = st.text_input("지역 이름")
    new_place = st.text_input("장소 이름")
    new_budget = st.number_input("예산", min_value=0, value=0, step=1000)
    new_type = st.text_input("유형")
    new_score = st.number_input("평점", min_value=0.0, max_value=5.0, value=4.5, step=0.1)
    
    if st.button("데이터 등록하기"):
        if new_region.strip() == "" or new_place.strip() == "":
            st.error("지역 이름과 장소 이름은 필수 항목입니다.")
        else:
            new_data = {
                "지역": new_region,
                "장소명": new_place,
                "예산": new_budget,
                "유형": new_type,
                "평점": new_score
            }
            
            new_row = pd.DataFrame([new_data])
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.success("새로운 데이터가 성공적으로 추가되었습니다! 전체 데이터 보기 또는 조건별 검색에서 확인해보세요.")

st.title("강생도 2.0")
st.write("엑셀 파일을 업로드하면 장소 데이터를 확인할 수 있습니다.")

df = load_file()

if df is not None:
    if "df" not in st.session_state:
        st.session_state.df = df

    st.sidebar.markdown("---")
    st.sidebar.header("기능 메뉴")
    menu = st.sidebar.radio(
        "원하는 기능을 선택하세요",
        ["전체 데이터 보기", "조건별 장소 검색", "지역 추가"]
    )
    st.sidebar.markdown("---")
    
    if menu == "전체 데이터 보기":
        print_table(st.session_state.df, "업로드한 장소 데이터 전체 목록")
        
    elif menu == "조건별 장소 검색":
        result = get_user_input(st.session_state.df)
        show_filter_places(result, st.session_state.df)

    elif menu == "지역 추가":
        add_region_ui()
