import pygame
import socket
import threading
import math
import random
import time

# 서버 연결 설정
SERVER_HOST = '210.101.236.189'  # 서버 IP 주소
SERVER_PORT = 12345              # 서버 포트 번호

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
print("서버에 연결되었습니다.")

# 상대방 점수 및 공 위치
opponent_ball_x, opponent_ball_y = 0, 0
opponent_score = 0

# 서버로부터 데이터 수신
def receive_data():
    global opponent_ball_x, opponent_ball_y, opponent_score
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                # 데이터 형식: "공_x,공_y,점수"
                ball_x, ball_y, score = data.split(",")
                opponent_ball_x = float(ball_x)
                opponent_ball_y = float(ball_y)
                opponent_score = int(score)
        except:
            break

threading.Thread(target=receive_data, daemon=True).start()

# 파이게임 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 1024, 1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Basketball Game - Multiplayer")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 배경 이미지 로드
background = pygame.image.load("path_to_image.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# 배경음악
pygame.mixer.music.load("C:/Users/USER/Desktop/pythonmj/background_basketball.mp3")
pygame.mixer.music.play(-1)

# 게임 속도 설정
clock = pygame.time.Clock()
FPS = 60

# 농구 골대 설정
hoop_width, hoop_height = 100, 20
hoop_x = screen_width - hoop_width
hoop_y = random.randint(100, screen_height - 200)
hoop_speed = 2

# 공 설정
ball_radius = 30
ball_x, ball_y = 100, screen_height - ball_radius - 50
ball_angle = 45
ball_power = 20
gravity = 0.5
ball_velocity_x, ball_velocity_y = 0, 0
ball_fired = False

# 점수 및 시간
my_score = 0
start_time = time.time()
time_limit = 60

running = True
while running:
    current_time = time.time()
    elapsed_time = current_time - start_time
    remaining_time = max(0, time_limit - elapsed_time)

    screen.blit(background, (0, 0))

    if remaining_time <= 0:
        running = False
        continue

    # 골대 움직임
    hoop_y += hoop_speed
    if hoop_y <= 0 or hoop_y + hoop_height >= screen_height:
        hoop_speed *= -1

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball_fired:
                ball_velocity_x = ball_power * math.cos(math.radians(ball_angle))
                ball_velocity_y = -ball_power * math.sin(math.radians(ball_angle))
                ball_fired = True

    # 공 이동
    if ball_fired:
        ball_velocity_y += gravity
        ball_x += ball_velocity_x
        ball_y += ball_velocity_y

        # 공이 화면 밖으로 나가면 초기화
        if ball_x < 0 or ball_x > screen_width or ball_y > screen_height:
            ball_x, ball_y = 100, screen_height - ball_radius - 50
            ball_fired = False

        # 공이 골대에 맞았는지 확인
        hoop_center_x = hoop_x + hoop_width / 2
        hoop_center_y = hoop_y + hoop_height / 2
        if (
            hoop_center_x - ball_radius < ball_x < hoop_center_x + ball_radius and
            hoop_center_y - ball_radius < ball_y < hoop_center_y + ball_radius
        ):
            my_score += 1
            client_socket.sendall(f"{ball_x},{ball_y},{my_score}".encode())  # 서버로 데이터 전송
            hoop_y = random.randint(100, screen_height - 200)

    # 텍스트 출력
    font = pygame.font.SysFont(None, 36)
    my_score_text = font.render(f"My Score: {my_score}", True, BLACK)
    opponent_score_text = font.render(f"Opponent Score: {opponent_score}", True, BLACK)
    time_text = font.render(f"Time Left: {int(remaining_time)}s", True, BLACK)

    screen.blit(my_score_text, (10, 10))
    screen.blit(opponent_score_text, (10, 50))
    screen.blit(time_text, (10, 90))

    # 상대방 공 그리기
    pygame.draw.circle(screen, BLUE, (int(opponent_ball_x), int(opponent_ball_y)), ball_radius)

    # 내 공과 골대 그리기
    pygame.draw.circle(screen, GREEN, (int(ball_x), int(ball_y)), ball_radius)
    pygame.draw.rect(screen, BLUE, (hoop_x, hoop_y, hoop_width, hoop_height))

    pygame.display.flip()
    clock.tick(FPS)

# 게임 종료 후 승자 출력
screen.fill(WHITE)
if my_score > opponent_score:
    result_text = "You Win!"
elif my_score < opponent_score:
    result_text = "You Lose!"
else:
    result_text = "It's a Draw!"

result_display = font.render(result_text, True, BLACK)
screen.blit(result_display, (screen_width // 2 - result_display.get_width() // 2, screen_height // 2))
pygame.display.flip()
time.sleep(3)

pygame.quit()
client_socket.close()
