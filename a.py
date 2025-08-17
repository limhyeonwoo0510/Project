import streamlit as st
import pandas as pd
import random
import requests

# 서버 IP 기반 URL
SERVER_URL = "http://192.168.55.245:5000"  # 여기 서버 IP로 바꿔

# 세션 초기화
if "username" not in st.session_state:
    st.session_state.username = ""
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_word" not in st.session_state:
    st.session_state.current_word = None
if "asked_words" not in st.session_state:
    st.session_state.asked_words = []

# 사용자 이름 입력
if st.session_state.username == "":
    name = st.text_input("이름을 입력하세요:")
    if name:
        st.session_state.username = name
        # 서버에 유저 등록
        requests.post(f"{SERVER_URL}/register", json={"username": name})
else:
    st.write(f"안녕하세요, **{st.session_state.username}** 님!")

    # CSV 불러오기 (탭 구분)
    df = pd.read_csv("words.csv", sep="\t", encoding="utf-8")
    
    # 퀴즈 진행
    remaining = df[~df["English"].isin(st.session_state.asked_words)]
    if not remaining.empty:
        if st.session_state.current_word is None:
            st.session_state.current_word = remaining.sample(1).iloc[0]

        word = st.session_state.current_word["English"]
        answer = st.session_state.current_word["Korean"]

        st.subheader(f"단어: {word}")
        user_input = st.text_input("뜻을 입력하세요", key=word)

        if st.button("제출"):
            if user_input.strip() == answer.strip():
                st.success("정답!")
                st.session_state.score += 10  # 10점
                st.session_state.asked_words.append(word)
                
                # 서버에 점수 업데이트
                requests.post(f"{SERVER_URL}/update_score", json={
                    "username": st.session_state.username,
                    "score": st.session_state.score
                })
            else:
                st.error(f"틀렸습니다! 정답: {answer}")

            st.session_state.current_word = None  # 다음 문제로 넘어가도록

    else:
        st.write("모든 문제를 다 풀었습니다!")

    # 현재 점수 표시
    st.write(f"현재 점수: {st.session_state.score}")

    # 랭킹 보기
    if st.button("🏆 랭킹 보기"):
        res = requests.get(f"{SERVER_URL}/ranking")
        if res.status_code == 200:
            ranking = res.json()
            st.write("### 상위 10명 랭킹")
            for i, r in enumerate(ranking, 1):
                st.write(f"{i}. {r['username']} - {r['score']}점")
