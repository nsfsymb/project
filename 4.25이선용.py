import streamlit as st

if "placelist" not in st.session_state:
    st.session_state.placelist = [
    {"이름": "강릉 시립도서관", "지역": "강릉", "실내여부": "실내", "예산": 0, "한줄설명": "조용히 공부하기 좋은 공간"},
    {"이름": "강릉 중앙시장", "지역": "강릉", "실내여부": "실내", "예산": 10000, "한줄설명": "저렴하게 식사할 수 있는 시장"},
    {"이름": "속초해변", "지역": "속초", "실내여부": "실외", "예산": 0, "한줄설명": "바다를 보며 쉬기 좋은 장소"},
    {"이름": "춘천 시립도서관", "지역": "춘천", "실내여부": "실내", "예산": 0, "한줄설명": "공부와 독서에 적합한 공간"}
]

def show_all_places(place_list):
    st.subheader("전체 장소 보기")
    for place in place_list:
        # 아래 빈칸을 완성하세요
        st.write("장소 이름:", place["이름"])
        st.write("지역:", place["지역"])
        st.write("실내/실외:", place["실내여부"])
        st.write("예산:", place["예산"], "원")
        st.write("설명:", place["한줄설명"])
        st.write("---")


def find_places(place_list, region, place_type, budget):
    result = []
    for place in place_list:
        # 아래 조건문을 완성하세요
        if place["지역"] == region and place["실내여부"] == place_type and place["예산"] <= budget:
            result.append(place)
    return result


def add_place(place_list, name, region, place_type, budget, description):
    new_place = {
        "이름": name,
        "지역": region,
        "실내여부": place_type,
        "예산": budget,
        "한줄설명": description
    }
    place_list.append(new_place)


st.markdown("# 🏔️ :blue[강원] 생활 도우미")
st.divider()

menu = st.selectbox("기능을 선택하세요", ["전체 보기", "추천 받기", "장소 추가"])

if menu == "전체 보기":
    show_all_places(placelist)

elif menu == "추천 받기":
    region = st.selectbox("지역을 선택하세요", ["강릉", "속초", "춘천"])
    place_type = st.selectbox("실내/실외를 선택하세요", ["실내", "실외"])
    is_free = st.checkbox("무료 장소만 찾고 싶어요")

    if is_free:
        budget = 0
        st.write("무료 장소를 검색합니다.")
    else:
        budget = st.number_input("사용 가능한 예산을 입력하세요", min_value=0, step=1000, value=5000)

    result_places = find_places(placelist, region, place_type, budget)

    st.subheader("추천 결과")

    # 아래 빈칸을 완성하세요
    if len(result_places) > 0:
        for place in result_places:
            st.write("장소 이름:", place["이름"])
            st.write("설명:", place["한줄설명"])
            st.write("예산:", place["예산"], "원")
            st.write("---")
    else:
        st.write("조건에 맞는 장소가 없습니다")

elif menu == "장소 추가":
    name = st.text_input("장소 이름을 입력하세요")
    region = st.selectbox("지역을 선택하세요", ["강릉", "속초", "춘천"])
    place_type = st.selectbox("실내/실외를 선택하세요", ["실내", "실외"])
    budget = st.number_input("예산을 입력하세요", min_value=0, step=1000)
    description = st.text_input("한줄 설명을 입력하세요")

    if st.button("장소 추가"):
        # 아래 함수 호출을 완성하세요
        add_place(placelist, name, region, place_type, budget, description)
        st.success("새 장소가 추가되었습니다")
