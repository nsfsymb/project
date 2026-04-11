st.title("강원 청소년 생활 도우미")
st.write("강원도에서 공부, 식사, 휴식에 도움이 되는 장소를 추천합니다")

region = st.selectbox("지역을 선택하세요", ["강릉", "속초", "춘천"])

if st.button("추천 보기"):
    st.write(region, "지역의 추천 장소를 보여 줍니다")
