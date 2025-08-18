import streamlit as st
import csv
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

def send_to_server(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(message.encode())
            data = s.recv(1024).decode()
        return data
    except Exception as e:
        return f"Error: {e}"

def load_words():
    words = []
    with open("words.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                words.append((row[0], row[1]))
    return words

words = load_words()

if "page" not in st.session_state:
    st.session_state.page = "menu"
if "name" not in st.session_state:
    st.session_state.name = ""
if "score" not in st.session_state:
    st.session_state.score = 0
if "index" not in st.session_state:
    st.session_state.index = 0
if "selected" not in st.session_state:
    st.session_state.selected = None  # 선택 답안 저장
if "answered" not in st.session_state:
    st.session_state.answered = False  # 제출 여부

st.title("영어 단어 학습 프로그램 (TCP 통신)")

if st.session_state.page == "menu":
    st.subheader("메뉴")
    name = st.text_input("이름 입력", st.session_state.name)
    if st.button("시작"):
        st.session_state.name = name
        st.session_state.page = "quiz"

elif st.session_state.page == "quiz":
    if st.session_state.index >= len(words):
        st.success(f"퀴즈 종료! 최종 점수: {st.session_state.score}")
        send_to_server(f"SAVE,{st.session_state.name},{st.session_state.score}")
        st.session_state.page = "menu"
    else:
        eng, kor = words[st.session_state.index]
        st.subheader(f"문제 {st.session_state.index+1}: {eng}")

        # 답 선택
        st.session_state.selected = st.radio(
            "정답을 선택하세요:",
            [kor, "틀린 뜻 예시 1", "틀린 뜻 예시 2"],
            index=None,   # 처음엔 아무 것도 선택되지 않게
            key=f"q{st.session_state.index}"
        )

        # 제출 버튼
        if st.button("제출"):
            if st.session_state.selected == kor:
                st.success("정답입니다!")
                st.session_state.score += 1
            else:
                st.error(f"오답입니다! 정답은 {kor}")
            st.session_state.index += 1
            st.session_state.selected = None  # 선택 초기화
            st.rerun()
