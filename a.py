import streamlit as st
import random
import csv
import socket

# 서버 정보
SERVER_IP = "127.0.0.1"   # 서버 IP
SERVER_PORT = 5000

# CSV 단어 불러오기
def load_words(csv_file="words.csv"):
    words = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 2:
                words.append((row[0], row[1]))
    return words

# 서버에 데이터 전송
def send_to_server(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        s.sendall(message.encode())
        return s.recv(4096).decode()

# 단어 불러오기
words = load_words()

# Streamlit UI
st.title("📘 영어 단어 학습 프로그램")

if "page" not in st.session_state:
    st.session_state.page = "login"
if "score" not in st.session_state:
    st.session_state.score = 0
if "name" not in st.session_state:
    st.session_state.name = ""

# 로그인 페이지
if st.session_state.page == "login":
    st.session_state.name = st.text_input("이름을 입력하세요")
    if st.button("시작하기"):
        if st.session_state.name.strip():
            st.session_state.page = "menu"

# 메뉴 페이지
elif st.session_state.page == "menu":
    st.header(f"안녕하세요, {st.session_state.name}님!")
    if st.button("단어 학습하기"):
        st.session_state.page = "study"
    if st.button("퀴즈 풀기"):
        st.session_state.page = "quiz"
    if st.button("점수 랭킹 보기"):
        st.session_state.page = "rank"

# 단어 학습 페이지
elif st.session_state.page == "study":
    st.header("📖 단어 학습")
    for eng, kor in words[:20]:  # 20개만 예시
        st.write(f"{eng} → {kor}")
    if st.button("뒤로가기"):
        st.session_state.page = "menu"

# 퀴즈 페이지
elif st.session_state.page == "quiz":
    st.header("📝 단어 퀴즈")
    if "quiz_word" not in st.session_state:
        st.session_state.quiz_word = random.choice(words)

    eng, kor = st.session_state.quiz_word
    answer = st.text_input(f"{eng} 의 뜻은 무엇일까요?")

    if st.button("제출"):
        if answer.strip() == kor:
            st.success("정답입니다! +10점")
            st.session_state.score += 10
        else:
            st.error(f"틀렸습니다. 정답: {kor}")
        st.session_state.quiz_word = random.choice(words)

    if st.button("뒤로가기"):
        # 점수 서버 저장
        send_to_server(f"SAVE,{st.session_state.name},{st.session_state.score}")
        st.session_state.page = "menu"

# 랭킹 페이지
elif st.session_state.page == "rank":
    st.header("🏆 점수 랭킹")
    data = send_to_server("RANK")
    st.text(data)
    if st.button("뒤로가기"):
        st.session_state.page = "menu"
