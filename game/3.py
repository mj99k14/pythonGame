import pygame
import random
import math
import time

# 파이게임 초기화
pygame.init()

# 화면 크기 설정
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Basketball Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 게임 속도 설정
clock = pygame.time.Clock()
FPS = 60

# 플레이어 설정
player_x = 100
player_y = screen_height - 100
player_width = 50
player_height = 100

# 농구 골대 설정
hoop_width = 100
hoop_height = 20
hoop_x = screen_width - 150
hoop_y = random.randint(100, screen_height - 200)

# 공 설정
ball_radius = 15
ball_x = player_x + player_width
ball_y = player_y - ball_radius
ball_angle = 45  # 초기 각도
ball_fired = False  # 공이 발사되었는지 여부
ball_power = 0  # 공의 발사 파워
max_power = 40  # 최대 파워

# 중력 및 속도
gravity = 0.5
ball_velocity_x = 0
ball_velocity_y = 0

# 점수
score = 0

# 공 발사 후 초기화 타이머
ball_fired_time = None

# 게임 시간 제한
start_time = time.time()
time_limit = 60  # 제한 시간 1분 (60초)

# 게임 루프
running = True
power_charging = False  # 파워 충전 여부

while running:
    current_time = time.time()
    elapsed_time = current_time - start_time
    remaining_time = max(0, time_limit - elapsed_time)  # 남은 시간 계산

    if remaining_time <= 0:
        running = False  # 시간이 다 되면 게임 종료
        continue  # 남은 코드를 실행하지 않도록 루프를 건너뜀

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball_fired:
                power_charging = True  # 파워 충전 시작
            elif event.key == pygame.K_UP:
                ball_angle = min(90, ball_angle + 5)  # 각도를 위로 조정 (최대 90도)
            elif event.key == pygame.K_DOWN:
                ball_angle = max(0, ball_angle - 5)   # 각도를 아래로 조정 (최소 0도)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and not ball_fired:
                power_charging = False  # 파워 충전 종료
                ball_fired = True
                ball_fired_time = time.time()  # 공이 발사된 시간 기록
                # 공의 속도 설정 (발사)
                ball_velocity_x = ball_power * math.cos(math.radians(ball_angle))
                ball_velocity_y = -ball_power * math.sin(math.radians(ball_angle))
                ball_power = 0  # 파워 초기화

    # 파워 충전
    if power_charging and not ball_fired:
        ball_power = min(max_power, ball_power + 0.5)  # 파워 증가

    # 공 이동
    if ball_fired:
        ball_x += ball_velocity_x
        ball_y += ball_velocity_y
        ball_velocity_y += gravity  # 중력 적용

        # 벽에 부딪혔을 때 튕기기
        if ball_x <= 0 or ball_x >= screen_width - ball_radius * 2:
            ball_velocity_x *= -1  # x축 반전
        if ball_y <= 0 or ball_y >= screen_height - ball_radius * 2:
            ball_velocity_y *= -1  # y축 반전

        # 농구 골대 통과 시 점수 증가
        if hoop_x < ball_x < hoop_x + hoop_width and hoop_y < ball_y < hoop_y + hoop_height:
            score += 1
            ball_fired = False
            ball_x = player_x + player_width
            ball_y = player_y - ball_radius
            hoop_y = random.randint(100, screen_height - 200)  # 농구 골대의 위치를 랜덤하게 변경
            ball_fired_time = None  # 발사 시간 초기화

        # 공이 농구 골대에 들어가지 않았을 때 3초 후 초기화
        if ball_fired_time and time.time() - ball_fired_time > 3:
            ball_fired = False
            ball_x = player_x + player_width
            ball_y = player_y - ball_radius
            ball_velocity_x = 0
            ball_velocity_y = 0
            ball_fired_time = None  # 발사 시간 초기화
            hoop_y = random.randint(100, screen_height - 200)  # 농구 골대의 위치를 랜덤하게 변경

    # 화면 그리기
    screen.fill(WHITE)

    # 발사 각도를 나타내는 선 그리기
    if not ball_fired:
        angle_line_length = 100  # 각도를 나타내는 선의 길이
        angle_line_x = ball_x + angle_line_length * math.cos(math.radians(ball_angle))
        angle_line_y = ball_y - angle_line_length * math.sin(math.radians(ball_angle))
        pygame.draw.line(screen, GREEN, (ball_x, ball_y), (angle_line_x, angle_line_y), 5)

    # 플레이어 그리기
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

    # 농구 골대 그리기
    pygame.draw.rect(screen, RED, (hoop_x, hoop_y, hoop_width, hoop_height))

    # 공 그리기
    pygame.draw.circle(screen, BLACK, (int(ball_x), int(ball_y)), ball_radius)

    # 텍스트로 각도, 파워, 점수, 남은 시간 표시
    font = pygame.font.SysFont(None, 36)
    angle_text = font.render(f"Angle: {ball_angle}°", True, BLACK)
    screen.blit(angle_text, (10, 10))
    power_text = font.render(f"Power: {int(ball_power)}", True, BLACK)
    screen.blit(power_text, (10, 50))
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 90))
    time_text = font.render(f"Time: {int(remaining_time)}s", True, BLACK)
    screen.blit(time_text, (10, 130))

    # 화면 업데이트
    pygame.display.flip()

    # 게임 속도 조절
    clock.tick(FPS)

# 게임 종료 후 결과 화면 출력
screen.fill(WHITE)
final_score_text = font.render(f"Final Score: {score}", True, BLACK)
screen.blit(final_score_text, (screen_width // 2 - 100, screen_height // 2))
pygame.display.flip()
pygame.time.wait(3000)  # 3초 동안 결과를 보여줌

# 게임 종료
pygame.quit()
