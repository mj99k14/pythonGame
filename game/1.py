import pygame
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("주인공 구하기")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 폰트 설정
font = pygame.font.SysFont(None, 36)

# 패들 설정
paddle_width = 100
paddle_height = 10
paddle_speed = 500
paddle = pygame.Rect(350, 550, paddle_width, paddle_height)

# 끝 화면 이미지
The_end = pygame.image.load("game/end.png")
The_end_rect = The_end.get_rect()
The_end_rect.topleft = (250, 150)

# 공 설정
ball_image = pygame.image.load("moster.png")
ball_rect = ball_image.get_rect()
ball_rect.topleft = (350, 350)
ball_speed = [5, -5]

# 게임 속도 설정
clock = pygame.time.Clock()
fps = 60

# 점수 및 시간
ball_count = 0
start_ticks = pygame.time.get_ticks()

running = True
while running:
    dt = clock.tick(fps) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 패들 움직임
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.x -= paddle_speed * dt
    if keys[pygame.K_RIGHT]:
        paddle.x += paddle_speed * dt

    # 패들 화면 경계 제한
    if paddle.x + paddle.width > screen.get_width():
        paddle.x = screen.get_width() - paddle.width
    if paddle.x < 0:
        paddle.x = 0

    # 공 이동
    ball_rect.x += ball_speed[0]
    ball_rect.y += ball_speed[1]

    # 공과 벽 충돌
    if ball_rect.left <= 0 or ball_rect.right >= screen.get_width():
        ball_speed[0] = -ball_speed[0]
    if ball_rect.top <= 0:
        ball_speed[1] = -ball_speed[1]

    # 공과 패들 충돌
    if ball_rect.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]
        ball_count += 1
        print(f"COUNT: {ball_count}")

    # 공이 바닥에 닿으면 게임 종료
    if ball_rect.bottom >= screen.get_height():
        screen.fill(BLACK)
        screen.blit(The_end, The_end_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    # 현재 시간 계산
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000

    # 점수와 시간 텍스트 생성
    score_text = font.render(f"Score: {ball_count}", True, WHITE)
    time_text = font.render(f"Time: {seconds}'s", True, WHITE)

    # 화면 그리기
    screen.fill(BLACK)
    screen.blit(ball_image, ball_rect)
    pygame.draw.rect(screen, BLUE, paddle)
    screen.blit(score_text, (20, 20))
    screen.blit(time_text, (20, 60))
    pygame.display.flip()

pygame.quit()
