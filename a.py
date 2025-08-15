import streamlit as st
import pandas as pd
import random

# CSV 읽기 (같은 폴더에 있는 경우)
@st.cache_data
def load_words():
    df = pd.read_csv("words.csv")  # words.csv 파일이 같은 폴더에 있어야 함
    return df

# 점수와 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_word' not in st.session_state:
    st.session_state.quiz_word = None

st.title("📚 영어 단어 학습 프로그램")

# 데이터 불러오기
df = load_words()

# 모드 선택
mode = st.radio("모드 선택", ["학습 모드", "퀴즈 모드"])

# -------------------
# 학습 모드
# -------------------
if mode == "학습 모드":
    st.subheader("📖 영어 단어와 뜻")
    st.dataframe(df)

# -------------------
# 퀴즈 모드
# -------------------
elif mode == "퀴즈 모드":
    st.subheader("❓ 영어 뜻 맞추기")

    # 새 문제 버튼
    if st.button("새 문제"):
        st.session_state.quiz_word = df.sample(1).iloc[0]

    # 문제 출력
    if st.session_state.quiz_word is not None:
        eng_word = st.session_state.quiz_word['English']
        correct_meaning = st.session_state.quiz_word['Korean']

        st.write(f"**영어 단어:** {eng_word}")
        answer = st.text_input("뜻을 입력하세요", key="answer_input")

        if st.button("정답 확인"):
            if answer.strip() == correct_meaning.strip():
                st.success("정답입니다! +10점")
                st.session_state.score += 10
            else:
                st.error(f"틀렸습니다. 정답: {correct_meaning}")

    st.write(f"현재 점수: **{st.session_state.score}점**")
