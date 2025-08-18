import streamlit as st
import pandas as pd
import requests
import random

SERVER_URL = "http://192.168.55.245:5000"  # 서버 실행 주소 맞게 바꿔야 함

# CSV에서 단어 불러오기
@st.cache_data
def load_words():
    df = pd.read_csv("words.csv")  # "english","korean" 형식
    return df

df = load_words()

# 세션 상태 초기화
if "name" not in st.session_state:
    st.session_state.name = ""
if "score" not in st.session_state:
    st.session_state.score = 0

st.title("영단어 학습 & 퀴즈 앱")

# 사용자 이름 입력
if st.session_state.name == "":
    st.session_state.name = st.text_input("이름을 입력하세요")
    if st.button("시작하기"):
        # 서버에서 기존 점수 불러오기
        res = requests.get(f"{SERVER_URL}/load/{st.session_state.name}")
        if res.status_code == 200:
            st.session_state.score = res.json()["score"]
            st.success(f"환영합니다 {st.session_state.name}! 현재 점수: {st.session_state.score}")
else:
    st.subheader(f"안녕하세요 {st.session_state.name}님, 현재 점수: {st.session_state.score}")

    menu = st.radio("메뉴 선택", ["단어 보기", "퀴즈 풀기", "랭킹 보기"])

    if menu == "단어 보기":
        st.dataframe(df)

    elif menu == "퀴즈 풀기":
        word = df.sample(1).iloc[0]
        st.write(f"다음 영어 단어의 뜻은? 👉 **{word['english']}**")

        options = [word["korean"]]
        options += random.sample(list(df["korean"]), 3)
        random.shuffle(options)

        answer = st.radio("정답을 고르세요", options)

        if st.button("제출"):
            if answer == word["korean"]:
                st.session_state.score += 10
                st.success("정답입니다! +10점")
            else:
                st.session_state.score -= 5
                st.error(f"오답입니다! 정답: {word['korean']} (-5점)")

            # 서버에 점수 저장
            requests.post(f"{SERVER_URL}/save", json={
                "name": st.session_state.name,
                "score": st.session_state.score
            })

    elif menu == "랭킹 보기":
        res = requests.get(f"{SERVER_URL}/ranking")
        if res.status_code == 200:
            ranking = res.json()["ranking"]
            st.table(ranking)
