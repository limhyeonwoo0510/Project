import streamlit as st
import pandas as pd
import random
import requests

# 서버 IP와 포트
SERVER_URL = "http://192.168.0.100:5000"  # 실제 서버 IP로 변경

# 세션 상태 초기화
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
    with st.form("name_form"):
        name = st.text_input("이름을 입력하세요")
        submitted = st.form_submit_button("시작")
        if submitted and name.strip() != "":
            st.session_state.username = name.strip()
            # 서버에 등록
            try:
                requests.post(f"{SERVER_URL}/register", json={"username": st.session_state.username})
            except requests.exceptions.RequestException:
                st.error("서버 연결 실패! 서버가 실행 중인지 확인하세요.")
            st.experimental_rerun()  # 화면 갱신

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
                st.session_state.score += 10  # 점수 10점
                st.session_state.asked_words.append(word)
                
                # 서버에 점수 업데이트
                try:
                    requests.post(f"{SERVER_URL}/update_score", json={
                        "username": st.session_state.username,
                        "score": st.session_state.score
                    })
                except requests.exceptions.RequestException:
                    st.error("서버 연결 실패! 점수가 저장되지 않았습니다.")
            else:
                st.error(f"틀렸습니다! 정답: {answer}")

            st.session_state.current_word = None  # 다음 문제로 넘어가도록

    else:
        st.write("모든 문제를 다 풀었습니다!")

    # 현재 점수 표시
    st.write(f"현재 점수: {st.session_state.score}")

    # 랭킹 보기
    if st.button("🏆 랭킹 보기"):
        try:
            res = requests.get(f"{SERVER_URL}/ranking")
            if res.status_code == 200:
                ranking = res.json()
                st.write("### 상위 10명 랭킹")
                for i, r in enumerate(ranking, 1):
                    st.write(f"{i}. {r['username']} - {r['score']}점")
            else:
                st.error("랭킹을 불러오는데 실패했습니다.")
        except requests.exceptions.RequestException:
            st.error("서버 연결 실패! 랭킹을 불러올 수 없습니다.")
