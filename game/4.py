import pygame
import random
import sys

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("무한 점프 게임")
clock = pygame.time.Clock()

# 색상
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 폰트
font = pygame.font.SysFont("malgungothic", 24)

# 플레이어
player = pygame.Rect(WIDTH // 2, HEIGHT - 60, 30, 30)
player_vel_y = 0
GRAVITY = 0.5
JUMP_POWER = -10

# 발판
platforms = [pygame.Rect(WIDTH // 2 - 50, HEIGHT - 20, 100, 10)]
PLATFORM_WIDTH = 70
PLATFORM_HEIGHT = 10

# 게임 상태
camera_scroll = 0
max_height = 0  # ← 픽셀 기준 높이 누적

# 발판 생성 함수
def create_platform(y_pos):
    x = random.randint(0, WIDTH - PLATFORM_WIDTH)
    return pygame.Rect(x, y_pos, PLATFORM_WIDTH, PLATFORM_HEIGHT)

running = True
while running:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5

    # 가로 경계
    if player.x < 0:
        player.x = 0
    if player.x > WIDTH - player.width:
        player.x = WIDTH - player.width

    # 중력 적용
    player_vel_y += GRAVITY
    player.y += player_vel_y

    # 발판 충돌
    for platform in platforms:
        if player.colliderect(platform) and player_vel_y > 0:
            player.bottom = platform.top
            player_vel_y = JUMP_POWER

    # 화면 스크롤 처리
    if player.y < HEIGHT // 3:
        scroll_amount = HEIGHT // 3 - player.y
        player.y = HEIGHT // 3
        camera_scroll += scroll_amount
        for platform in platforms:
            platform.y += scroll_amount
        max_height += scroll_amount  # ← 스크롤 누적해서 높이로 사용

    # 발판 생성
    while len(platforms) < 10:
        last_y = min(p.y for p in platforms)
        new_y = last_y - random.randint(50, 100)
        platforms.append(create_platform(new_y))

    # 발판 제거
    platforms = [p for p in platforms if p.y < HEIGHT]

    # 게임 오버
    if player.y > HEIGHT:
        game_over_text = font.render("게임 오버! ESC로 종료", True, RED)
        height_surface = font.render(f"최고 높이: {max_height // 10}m", True, BLACK)
        screen.blit(game_over_text, (WIDTH//2 - 120, HEIGHT//2))
        screen.blit(height_surface, (WIDTH//2 - 80, HEIGHT//2 + 40))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False
        continue

    # 높이 표시 (10픽셀 = 1m 환산)
    height_surface = font.render(f"도달한 높이: {max_height // 10}m", True, BLACK)
    screen.blit(height_surface, (10, 10))

    # 발판 그리기
    for platform in platforms:
        pygame.draw.rect(screen, PINK, platform)

    # 플레이어 그리기
    pygame.draw.rect(screen, BLUE, player)

    pygame.display.flip()
    clock.tick(60)
