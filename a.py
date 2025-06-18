from streamlit_drawable_canvas import st_canvas
import streamlit as st
import numpy as np

st.title("🖌 그림 그리기 체험")

# 캔버스 설정
canvas_result = st_canvas(
    fill_color="rgba(0, 0, 255, 0.3)",  # 채우기 색
    stroke_width=10,
    stroke_color="#000000",
    background_color="#ffffff",
    height=280,
    width=280,
    drawing_mode="freedraw",  # "freedraw" 또는 "rect", "circle" 등
    key="canvas",
)

# 그린 그림 결과 확인 (넘파이 배열)
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data, caption="그림 결과")
