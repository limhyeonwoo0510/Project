import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# 초기 설정
box_width = 10  # 상자의 가로 길이
box_height = 5  # 상자의 세로 길이
ball_radius = 0.3  # 공의 반지름

# Streamlit UI 설정
st.title('상자 안에서 충돌하는 공')
st.sidebar.header('게임 설정')

# 속도 설정 (단위: 0 ~ 1)
speed = st.sidebar.slider('공의 속도', 0.1, 1.0, 0.5)
angle = st.sidebar.slider('공의 이동 각도 (degree)', 0, 360, 45)

# 각도를 라디안으로 변환
angle_rad = np.radians(angle)

# 초기 속도 계산
initial_speed = speed * 2  # 속도는 단순히 가속도로 계산 (최대 2)

# 공의 초기 위치와 속도
ball_position = [box_width / 2, box_height / 2]  # 공의 초기 위치 (중앙)
ball_velocity = [initial_speed * np.cos(angle_rad), initial_speed * np.sin(angle_rad)]  # 초기 속도

# 물리 엔진: 매 프레임마다 공의 위치 업데이트
def update_ball_position(position, velocity, dt=0.1):
    new_position = [position[0] + velocity[0] * dt, position[1] + velocity[1] * dt]
    
    # 상자 경계를 넘지 않도록 반사 로직 추가
    if new_position[0] - ball_radius <= 0 or new_position[0] + ball_radius >= box_width:
        velocity[0] = -velocity[0]  # X축 반사
    if new_position[1] - ball_radius <= 0 or new_position[1] + ball_radius >= box_height:
        velocity[1] = -velocity[1]  # Y축 반사
    
    # 공의 새로운 위치
    new_position[0] = np.clip(new_position[0], ball_radius, box_width - ball_radius)
    new_position[1] = np.clip(new_position[1], ball_radius, box_height - ball_radius)
    
    return new_position, velocity

# 게임 업데이트: 공의 위치와 속도 계산
ball_position, ball_velocity = update_ball_position(ball_position, ball_velocity)

# 테이블 그리기
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(0, box_width)
ax.set_ylim(0, box_height)

# 상자 그리기
ax.set_facecolor('lightblue')

# 공 그리기
ball = Ellipse((ball_position[0], ball_position[1]), 2 * ball_radius, 2 * ball_radius, color='red')
ax.add_patch(ball)

# 축 숨기기
ax.axis('off')

# 테이블 표시
st.pyplot(fig)
