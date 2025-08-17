import streamlit as st
import pandas as pd
import random
import requests

# 서버 주소
SERVER_URL = "http://localhost:5000"

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_word" not in st.session_state:
    st.session_state.current_word = None
if "asked_words" not in st.session_state:
    st.session_state.asked_words = []
if "username" not in st.session_state:
    st.session_state.username = ""

# 사용자 이름 입력
if st.session_state.username == "":
    username = st.text_input("이름을 입력하세요:")
    if username:
        st.session_state.username = username
        # 서버에 유저 등록
        requests.post(f"{SERVER_URL}/register", json={"username": username})
else:
    st.write(f"안녕하세요, **{st.session_state.username}** 님!")

    # 단어 데이터 불러오기 (탭 구분!)
    df = pd.read_csv("words.csv", sep="\t", encoding="utf-8")

    # 새로운 문제 불러오기
    if st.session_state.current_word is None and len(st.session_state.asked_words) < len(df):
        remaining = df[~df["English"].isin(st.session_state.asked_words)]
        if not remaining.empty:
            st.session_state.current_word = remaining.sample(1).iloc[0]

    if st.session_state.current_word is not None:
        word = st.session_state.current_word["English"]
        answer = st.session_state.current_word["Korean"]

        st.write(f"다음 단어의 뜻은 무엇일까요? **{word}**")

        user_answer = st.text_input("뜻을 입력하세요:")

        if st.button("제출"):
            if user_answer.strip() == answer.strip():
                st.success("정답입니다!")
                st.session_state.score += 1
                # 서버에 점수 업데이트
                requests.post(f"{SERVER_URL}/update_score", json={
                    "username": st.session_state.username,
                    "score": st.session_state.score
                })
            else:
                st.error(f"틀렸습니다! 정답은 {answer}")

            st.session_state.asked_words.append(word)
            st.session_state.current_word = None  # 다음 문제로 넘어가도록 리셋

    else:
        st.write("모든 문제를 다 푸셨습니다!")

    # 점수 표시
    st.write(f"현재 점수: {st.session_state.score}")

    # 랭킹 조회
    if st.button("랭킹 보기"):
        res = requests.get(f"{SERVER_URL}/ranking")
        if res.status_code == 200:
            ranking = res.json()
            st.write("### 🏆 랭킹")
            for i, r in enumerate(ranking, 1):
                st.write(f"{i}. {r['username']} - {r['score']}점")
