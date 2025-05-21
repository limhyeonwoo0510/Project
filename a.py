import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# 당구 테이블 크기
table_width = 10
table_height = 5

# 당구 공 설정
ball_radius = 0.3
ball_color = 'red'
ball_position = [5, 2.5]  # 공의 초기 위치 (중앙)

# Streamlit UI
st.title('당구 게임')
st.sidebar.header('게임 설정')

# 공의 위치 이동
dx = st.sidebar.slider('X축 이동 거리', -1.0, 1.0, 0.0)
dy = st.sidebar.slider('Y축 이동 거리', -1.0, 1.0, 0.0)

# 공의 새로운 위치 계산
ball_position[0] += dx
ball_position[1] += dy

# 공이 테이블을 벗어나지 않도록 경계 설정
ball_position[0] = np.clip(ball_position[0], ball_radius, table_width - ball_radius)
ball_position[1] = np.clip(ball_position[1], ball_radius, table_height - ball_radius)

# 당구 테이블 그리기
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(0, table_width)
ax.set_ylim(0, table_height)

# 테이블 그리기
ax.set_facecolor('green')

# 공 그리기
ball = Ellipse((ball_position[0], ball_position[1]), 2 * ball_radius, 2 * ball_radius, color=ball_color)
ax.add_patch(ball)

# 축 숨기기
ax.axis('off')

# 테이블 표시
st.pyplot(fig)

