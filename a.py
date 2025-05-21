import streamlit as st
import pygame
import numpy as np

# 초기화
pygame.init()

# 화면 크기 및 공 속도 설정
WIDTH, HEIGHT = 600, 400
FPS = 60

# 공의 초기 속도 설정
speed = st.slider("공의 속도", min_value=1, max_value=10, value=5, step=1)

# 공의 초기 위치와 속도
ball_pos = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)
ball_vel = np.array([speed, speed], dtype=float)  # 속도는 사용자가 설정

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (255, 0, 0)

# 화면 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("충돌하는 공")

# 공의 반지름
ball_radius = 15

# 게임 루프
def move_ball():
    global ball_pos, ball_vel

    # 벽에 충돌하면 반사
    if ball_pos[0] - ball_radius <= 0 or ball_pos[0] + ball_radius >= WIDTH:
        ball_vel[0] = -ball_vel[0]
    if ball_pos[1] - ball_radius <= 0 or ball_pos[1] + ball_radius >= HEIGHT:
        ball_vel[1] = -ball_vel[1]

    # 공의 위치 업데이트
    ball_pos += ball_vel

# Streamlit에서 게임 화면을 실시간으로 업데이트
def run_game():
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 화면 배경을 검정색으로 설정
        screen.fill(BLACK)

        # 공을 그리기
        pygame.draw.circle(screen, BALL_COLOR, ball_pos.astype(int), ball_radius)

        # 공의 움직임 처리
        move_ball()

        # 화면 업데이트
        pygame.display.flip()

        # FPS 설정
        clock.tick(FPS)

# Streamlit에서 pygame을 실행할 수 없으므로,
# Streamlit에서 pygame 화면을 열어놓고, 공 속도를 사용자 입력에 따라 업데이트 하는 방식으로 접근
if __name__ == "__main__":
    run_game()
