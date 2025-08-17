import streamlit as st
import pandas as pd
import requests
import random

SERVER_URL = "http://localhost:5000"  # Flask 서버 주소

# CSV 불러오기
df = pd.read_csv("words.csv")  # "english,korean" 구조
words = df.to_dict(orient="records")

# 사용자 이름 입력
if "username" not in st.session_state:
    st.session_state.username = ""

st.session_state.username = st.text_input("이름을 입력하세요", st.session_state.username)

if st.session_state.username:
    menu = st.sidebar.radio("메뉴 선택", ["단어 보기", "퀴즈", "랭킹"])

    if menu == "단어 보기":
        st.write(df)

    elif menu == "퀴즈":
        if "used" not in st.session_state:
            st.session_state.used = set()
        if "current_word" not in st.session_state:
            st.session_state.current_word = None

        if len(st.session_state.used) == len(words):
            st.success("모든 문제를 다 풀었어!")
        else:
            if st.session_state.current_word is None:
                st.session_state.current_word = random.choice(words)
                while st.session_state.current_word["english"] in st.session_state.used:
                    st.session_state.current_word = random.choice(words)

            q = st.session_state.current_word
            st.subheader(f"단어: {q['english']}")
            answer = st.text_input("뜻을 입력하세요", key="answer")

            if st.button("제출"):
                if answer.strip() == q["korean"]:
                    st.success("정답!")
                    st.session_state.used.add(q["english"])

                    # 서버에 점수 저장
                    requests.post(f"{SERVER_URL}/add_points", json={
                        "username": st.session_state.username,
                        "points": 10
                    })

                    st.session_state.current_word = None  # 다음 문제로 넘어가도록 초기화
                else:
                    st.error(f"틀렸습니다! 정답: {q['korean']}")

    elif menu == "랭킹":
        res = requests.get(f"{SERVER_URL}/ranking")
        if res.status_code == 200:
            ranking = res.json()
            st.write("### 랭킹")
            for i, row in enumerate(ranking, start=1):
                st.write(f"{i}. {row['username']} - {row['points']}점")
