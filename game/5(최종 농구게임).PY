import pygame
import random
import math
import time

# 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 1024, 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Basketball Game")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# 배경 이미지
background = pygame.image.load("path_to_image.png")  # 실제 경로로 교체 필요
background = pygame.transform.scale(background, (screen_width, screen_height))

# 배경 음악
pygame.mixer.music.load("C:/Users/USER/Desktop/pythonmj/background_basketball.mp3")
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
FPS = 60

# 플레이어
player_x = 100
player_y = screen_height - 150
player_width = 50
player_height = 100

# 골대
hoop = pygame.image.load("G.png")
hoop_rect = hoop.get_rect()
hoop_rect_width = 150  # ← 크기 증가
hoop_rect_height = 40
hoop_rect_x = screen_width - hoop_rect_width
hoop_rect_y = random.randint(200, 500)

# 공
ball = pygame.image.load("ball.png")
ball_radius = 30
ball = pygame.transform.scale(ball, (ball_radius * 2, ball_radius * 2))
ball_rect_x = player_x + player_width
ball_rect_y = player_y + player_height // 2 - ball_radius * 2
ball_angle = 60
ball_fired = False
ball_power = 0
max_power = 50  # ← 줄임

# 물리 변수
gravity = 0.4  # ← 중력 증가
ball_velocity_x = 0
ball_velocity_y = 0

# 상태 변수
score = 0
ball_fired_time = None
ball_bounced_time = None
bounce_reset_time = 3
start_time = time.time()
time_limit = 60
running = True
power_charging = False

# 포물선 경로 시각화
def calculate_parabola_path(start_x, start_y, velocity_x, velocity_y, gravity, steps=100):
    path = []
    t = 0
    for _ in range(steps):
        t += 0.1
        x = start_x + velocity_x * t
        y = start_y + velocity_y * t + 0.5 * gravity * t ** 2
        if x > screen_width or y > screen_height:
            break
        path.append((x, y))
    return path

# 공 및 골대 리셋
def reset_ball_and_hoop():
    global ball_fired, ball_rect_x, ball_rect_y, ball_velocity_x, ball_velocity_y
    global ball_fired_time, ball_bounced_time, hoop_rect_y
    ball_fired = False
    ball_rect_x = player_x + player_width
    ball_rect_y = player_y + player_height // 2 - ball_radius * 2
    ball_velocity_x = 0
    ball_velocity_y = 0
    ball_fired_time = None
    ball_bounced_time = None
    hoop_rect_y = random.randint(200, 500)

# 게임 루프
while running:
    current_time = time.time()
    elapsed_time = current_time - start_time
    remaining_time = max(0, time_limit - elapsed_time)

    screen.blit(background, (0, 0))

    if remaining_time <= 0:
        running = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and not ball_fired:
                power_charging = True
            elif event.key == pygame.K_UP:
                ball_angle = min(80, ball_angle + 5)
            elif event.key == pygame.K_DOWN:
                ball_angle = max(30, ball_angle - 5)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and not ball_fired:
                power_charging = False
                ball_fired = True
                ball_fired_time = time.time()
                ball_velocity_x = ball_power * math.cos(math.radians(ball_angle))
                ball_velocity_y = -ball_power * math.sin(math.radians(ball_angle))
                ball_power = 0

    if power_charging and not ball_fired:
        ball_power = min(max_power, ball_power + 0.5)

    if ball_fired:
        ball_velocity_y += gravity
        ball_rect_x += ball_velocity_x
        ball_rect_y += ball_velocity_y

        if ball_rect_x < 0 or ball_rect_x > screen_width - ball_radius * 2 or ball_rect_y > screen_height - ball_radius * 2:
            reset_ball_and_hoop()

        if ball_rect_x <= 0 or ball_rect_x >= screen_width - ball_radius * 2:
            ball_velocity_x *= -1
            ball_bounced_time = time.time()

        if ball_rect_y <= 0 or ball_rect_y >= screen_height - ball_radius * 2:
            ball_velocity_y *= -1
            ball_bounced_time = time.time()

        if ball_bounced_time and time.time() - ball_bounced_time > bounce_reset_time:
            reset_ball_and_hoop()

        hoop_center_x = hoop_rect_x + hoop_rect_width / 2
        hoop_center_y = hoop_rect_y + hoop_rect_height / 2
        if (
            hoop_center_x - ball_radius < ball_rect_x < hoop_center_x + ball_radius and
            hoop_center_y - ball_radius < ball_rect_y < hoop_center_y + ball_radius
        ):
            score += 1
            reset_ball_and_hoop()

    if not ball_fired:
        angle_line_length = 100
        angle_line_x = ball_rect_x + angle_line_length * math.cos(math.radians(ball_angle))
        angle_line_y = ball_rect_y - angle_line_length * math.sin(math.radians(ball_angle))
        pygame.draw.line(screen, GREEN, (ball_rect_x, ball_rect_y), (angle_line_x, angle_line_y), 5)

        path = calculate_parabola_path(
            ball_rect_x,
            ball_rect_y,
            ball_power * math.cos(math.radians(ball_angle)),
            -ball_power * math.sin(math.radians(ball_angle)),
            gravity
        )
        for point in path:
            pygame.draw.circle(screen, BLUE, (int(point[0]), int(point[1])), 3)

    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
    screen.blit(hoop, (hoop_rect_x, hoop_rect_y))
    screen.blit(ball, (ball_rect_x, ball_rect_y))

    font = pygame.font.SysFont(None, 36)
    screen.blit(font.render(f"Angle: {ball_angle}°", True, BLACK), (10, 10))
    screen.blit(font.render(f"Power: {int(ball_power)}", True, BLACK), (10, 50))
    screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 90))
    screen.blit(font.render(f"Time: {int(remaining_time)}s", True, BLACK), (10, 130))

    gauge_width = 200
    gauge_height = 20
    gauge_x = 10
    gauge_y = 170
    current_gauge_width = (ball_power / max_power) * gauge_width
    pygame.draw.rect(screen, BLACK, (gauge_x, gauge_y, gauge_width, gauge_height), 2)
    pygame.draw.rect(screen, GREEN, (gauge_x, gauge_y, current_gauge_width, gauge_height))

    pygame.display.flip()
    clock.tick(FPS)

# 종료 시 최종 점수
screen.fill(WHITE)
final_score_text = font.render(f"Final Score: {score}", True, BLACK)
screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2))
pygame.display.flip()
time.sleep(2)
pygame.quit()
