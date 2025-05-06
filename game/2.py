import pygame
import random

pygame.init()

# 화면 설정
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('먹이주기 게임')

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# 배경 음악 재생
background_music = pygame.mixer.music.load("tfile.mp3")
pygame.mixer.music.play(-1)

# 폰트 설정
font = pygame.font.SysFont("malgungothic", 28)
message_text = ""  # 화면에 출력할 메시지

# 장애물 생성 함수
def create_obstacles(num_obstacles, size, screen_width, screen_height):
    obstacles = []
    for _ in range(num_obstacles):
        while True:
            rect = pygame.Rect(random.randint(0, screen_width - size),
                               random.randint(0, screen_height - size), size, size)
            if not any(rect.colliderect(o) for o in obstacles):
                obstacles.append(rect)
                break
    return obstacles

# 아이템 생성 함수
def create_items(num_items, size, screen_width, screen_height, obstacles):
    items = []
    for _ in range(num_items):
        while True:
            rect = pygame.Rect(random.randint(0, screen_width - size),
                               random.randint(0, screen_height - size), size, size)
            if not any(rect.colliderect(o) for o in obstacles) and not any(rect.colliderect(i) for i in items):
                items.append(rect)
                break
    return items

# 장애물 및 아이템 생성
obstacles = create_obstacles(5, 50, screen_width, screen_height)
items = create_items(10, 20, screen_width, screen_height, obstacles)

# 몬스터 이미지 설정
monster = pygame.image.load("moster.png")
monster_rect = monster.get_rect()
monster_rect_width = monster_rect.width
monster_rect_height = monster_rect.height
monster_rect.x = monster_rect.y
monster_rect.y = monster_rect.x

# 몬스터 초기 위치 설정 (충돌 없이)
while True:
    random_x = random.randint(0, screen_width - monster_rect_width)
    random_y = random.randint(0, screen_height - monster_rect_height)
    temp_rect = pygame.Rect(random_x, random_y, monster_rect_width, monster_rect_height)
    if temp_rect.collidelist(obstacles) == -1 and temp_rect.collidelist(items) == -1:
        monster_rect.topleft = (random_x, random_y)
        break

# 이동 속도 및 기타 설정
velocity = 300
clock = pygame.time.Clock()
scale_factor = 1.0
running = True

# 게임 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    previous_position = monster_rect.topleft
    dt = clock.tick(60) / 1000.0

    # 키 입력에 따라 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        monster_rect.x -= velocity * dt
    if keys[pygame.K_RIGHT]:
        monster_rect.x += velocity * dt
    if keys[pygame.K_UP]:
        monster_rect.y -= velocity * dt
    if keys[pygame.K_DOWN]:
        monster_rect.y += velocity * dt

    # 장애물 충돌 처리
    collision_index = monster_rect.collidelist(obstacles)
    if collision_index != -1:
        message_text = f"장애물 {collision_index}와 충돌! 성식이 아픔! 병원감"
        monster_rect.topleft = previous_position
        running = False

    # 아이템 충돌 처리
    item_index = monster_rect.collidelist(items)
    if item_index != -1:
        message_text = f"먹이 나머지:{len(items) - 1}"
        del items[item_index]
        scale_factor += 0.1
        monster = pygame.transform.scale(monster,
                    (int(monster_rect_width * scale_factor),
                     int(monster_rect_height * scale_factor)))
        monster_rect = monster.get_rect(center=monster_rect.center)

    if not items:
        message_text = "몬스터 다 먹음!"
        running = False

    # 화면 그리기
    screen.fill(WHITE)

    for obs in obstacles:
        pygame.draw.rect(screen, BLUE, obs)
    for item in items:
        pygame.draw.rect(screen, YELLOW, item)

    screen.blit(monster, monster_rect)

    # 메시지 표시
    if message_text:
        message_surface = font.render(message_text, True, RED)
        screen.blit(message_surface, (20, 20))

    pygame.display.flip()

pygame.quit()
