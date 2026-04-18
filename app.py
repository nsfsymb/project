import streamlit as st

places = [
    {"이름": "강릉 시립도서관", "지역": "강릉", "실내여부": "실내", "예산": 0, "한줄설명": "조용히 공부하기 좋은 공간"},
    {"이름": "강릉 중앙시장", "지역": "강릉", "실내여부": "실내", "예산": 10000, "한줄설명": "저렴하게 식사할 수 있는 시장"},
    {"이름": "속초해변", "지역": "속초", "실내여부": "실외", "예산": 0, "한줄설명": "바다를 보며 쉬기 좋은 장소"},
    {"이름": "춘천 시립도서관", "지역": "춘천", "실내여부": "실내", "예산": 0, "한줄설명": "학습과 독서에 적합한 공간"}
]

def get_recommendations(data, region, indoor, budget):
    result = []
    for place in data:
        if place["지역"] == region and place["실내여부"] == indoor and place["예산"] <= budget:
            result.append(place)
    return result

st.title("강원 청소년 생활 도우미")
selected_region = st.selectbox("지역을 선택하세요", ["강릉", "속초", "춘천"])
selected_indoor = st.radio("실내 여부를 선택하세요", ["실내", "실외"])
selected_budget = st.number_input("예산을 입력하세요", min_value=0)
if st.button("추천 보기"):
    recommendations = get_recommendations(places, selected_region, selected_indoor, selected_budget)

    if len(recommendations) == 0:
        st.write("조건에 맞는 장소가 없습니다")

    for place in recommendations:
        st.write(place["이름"])
        st.write(place["지역"])
        st.write(place["예산"])
        st.write(place["한줄설명"])
        st.write("---")
