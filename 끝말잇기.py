import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="끝말잇기 치트키", page_icon="🤫", layout="centered")

st.title("🤫 끝말잇기 한방단어 검색기")
st.caption("한 글자만 입력하면 상대를 한방에 보내는 단어를 추천합니다.")

# 강력한 한방단어 데이터베이스
HANBANG_DICT = {
    "기": ["기쁨", "기름", "기륨"],
    "나": ["나트륨", "나이오븀"],
    "다": ["다이뮴", "다이아몬드"],
    "라": ["라듐", "라돈"],
    "마": ["마그네슘", "마이크로필름"],
    "바": ["바륨", "바나듐"],
    "사": ["사마륨", "사이클로트론"],
    "아": ["아르곤", "아인슈타이늄"],
    "자": ["자석", "자이로스코프"],
    "차": ["차륨"],
    "카": ["카드뮴", "칼슘", "칼리포늄"],
    "타": ["타이타늄", "탄탈럼"],
    "파": ["파라듐", "프로메튬"],
    "하": ["하프늄", "하이드로늄"]
}

# 검색창 구현 (글자 수가 바뀔 때마다 즉시 반영)
user_input = st.text_input("시작하는 글자를 입력하세요 (딱 한 글자만!):", max_chars=1)

if user_input:
    # 입력한 글자로 시작하는 한방단어 찾기
    recommendations = HANBANG_DICT.get(user_input, [])
    
    if recommendations:
        st.success(f"**'{user_input}'**(으)로 시작하는 강력한 방어/공격 단어 발견!")
        
        # 보기 좋게 카드 형태로 출력
        for word in recommendations:
            st.info(f"💡 **{word}** (끝 단어 공격 유효)")
    else:
        st.warning(f"앗, '{user_input}'로 시작하는 등록된 한방단어가 없습니다. 단어를 추가해보세요!")
