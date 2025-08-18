import streamlit as st
import socket
import csv
import random

SERVER_IP = "127.0.0.1"   # 서버 IP
SERVER_PORT = 12345       # 서버 포트

def send_to_server(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(message.encode())
            data = s.recv(4096).decode()
            return data
    except Exception as e:
        return f"서버 연결 실패: {e}"

# CSV 단어 로드
def load_words():
    words = []
    with open("words.csv", newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 2:
                words.append((row[0], row[1]))
    return words

words = load_words()

if "page" not in st.session_state:
    st.session_state.page = "home"
if "name" not in st.session_state:
    st.session_state.name = ""
if "score" not in st.session_state:
    st.session_state.score = 0
if "quiz_word" not in st.session_state:
    st.session_state.quiz_word = None

# 홈 화면
if st.session_state.page == "home":
    st.title("영어 단어 학습 프로그램")
    st.session_state.name = st.text_input("이름을 입력하세요")
    if st.button("시작"):
        if st.session_state.name.strip() != "":
            st.session_state.page = "menu"

# 메뉴 화면
elif st.session_state.page == "menu":
    st.header(f"안녕하세요, {st.session_state.name}님!")
    if st.button("단어 보기"):
        st.session_state.page = "words"
    if st.button("퀴즈 풀기"):
        st.session_state.page = "quiz"
    if st.button("랭킹 보기"):
        st.session_state.page = "rank"

# 단어 보기
elif st.session_state.page == "words":
    st.header("단어장")
    for eng, kor in words:
        st.write(f"{eng} - {kor}")
    if st.button("뒤로"):
        st.session_state.page = "menu"

# 퀴즈
elif st.session_state.page == "quiz":
    st.header("단어 퀴즈")
    if st.session_state.quiz_word is None:
        st.session_state.quiz_word = random.choice(words)

    eng, kor = st.session_state.quiz_word
    options = [kor] + [w[1] for w in random.sample(words, 3)]
    random.shuffle(options)

    answer = st.radio(f"{eng} 뜻은 무엇일까요?", options, index=None)

    if st.button("제출"):
        if answer == kor:
            st.success("정답!")
            st.session_state.score += 10
        else:
            st.error(f"오답! 정답은 {kor}")
        st.session_state.quiz_word = None

    st.write(f"현재 점수: {st.session_state.score}")
    if st.button("뒤로 가기"):
        send_to_server(f"SAVE,{st.session_state.name},{st.session_state.score}")
        st.session_state.page = "menu"

# 랭킹 보기
elif st.session_state.page == "rank":
    st.header("랭킹")
    response = send_to_server("RANK")
    st.text(response)
    if st.button("뒤로"):
        st.session_state.page = "menu"
