import pygame
import random
import sys

# 초기화
pygame.init()

# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# 색상
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)

# 플레이어 설정
player = pygame.Rect(400, 500, 50, 50)
gravity = 1.5  # 중력 값 설정    
jump_velocity = 0  # 수직 속도
is_jumping = False
is_holding = False
jump_start_time = None  # 스페이스바 누른 시간 기록

# 점프 관련 변수
min_jump_power = 10  # 최소 점프 힘
max_jump_power = 30  # 최대 점프 힘
jump_power = min_jump_power  # 기본 점프 힘

# 이동 속도
move_speed = 5  # 좌우 이동 속도

# 발판
paddle_width = 70
paddle_height = 10
paddle_list = []

def generate_paddles():
    paddle_list.clear()
    for _ in range(5):  # 발판을 5개 생성
        while True:
            p_random_x = random.randint(0, screen_width - paddle_width)
            p_random_y = random.randint(100, screen_height - paddle_height - 50)
            paddle_rect = pygame.Rect(p_random_x, p_random_y, paddle_width, paddle_height)
            if paddle_rect.collidelist(paddle_list) == -1:
                paddle_list.append(paddle_rect)
                break  # 발판이 겹치지 않으면 리스트에 추가하고 루프 탈출

# 발판 생성
generate_paddles()

while True:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_holding = True
                jump_start_time = pygame.time.get_ticks()  # 점프 시작 시간 기록

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and is_holding:
                hold_time = (pygame.time.get_ticks() - jump_start_time) / 1000.0  # 누른 시간 계산
                hold_time = min(hold_time, 1.0)  # 최대 1초까지만 계산
                jump_power = min_jump_power + (max_jump_power - min_jump_power) * hold_time
                jump_velocity = -jump_power  # 점프 힘 설정
                is_jumping = True
                is_holding = False  # 점프 후 홀드 상태 해제

    # 키보드 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= move_speed
    if keys[pygame.K_RIGHT]: 
        player.x += move_speed

    # 중력 적용 및 플레이어 이동
    if is_jumping:
        jump_velocity += gravity
        player.y += jump_velocity

    # 바닥 충돌 처리
    if player.y > 500:
        player.y = 500
        jump_velocity = 0
        is_jumping = False  # 바닥에 닿으면 점프 상태 해제

    # 발판 충돌 처리
    for paddle_rect in paddle_list:
        if player.colliderect(paddle_rect) and jump_velocity > 0:
            player.y = paddle_rect.top - player.height  # 발판 위로 플레이어 위치 조정
            jump_velocity = 0  # 점프 속도를 0으로 설정하여 멈춤
            is_jumping = False  # 발판에 닿으면 점프 상태 해제

    # 플레이어 그리기
    pygame.draw.rect(screen, BLUE, player)
    for paddle in paddle_list:
        pygame.draw.rect(screen, PINK, paddle)
    
    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)
 