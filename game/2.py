import pygame
import random

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('성식이 먹이주기 게임')
#색상정의
WHITE = (255, 255, 255)
BLUE =(0, 0, 255)
RED = (255, 0 ,0)
GREEN = (0, 255 ,0)
YELLOW = (255, 255 , 0)

background_music = pygame.mixer.music.load("tfile.mp3")
pygame.mixer.music.play(-1)
#장애물 생성 함수
def create_obstacles(num_obstacles, size , screen_width, screen_height):

    obstacles = []

    for _ in range(num_obstacles):
        while True:
            rect = pygame.Rect(random.randint(0, screen_width - size),\
                               random.randint(0, screen_height - size), size, size)
            if not any(rect.colliderect(o) for o in obstacles):
                obstacles.append(rect)
                break
    return obstacles
#아이템 생성함수
def create_items(num_items, size , screen_width, screen_height, obstacles):

    items = []

    for _ in range(num_items):
        while True:
            rect = pygame.Rect(random.randint(0, screen_width - size),\
                                random.randint(0, screen_height - size),size, size)
            if not any(rect.colliderect(o) for o in obstacles) and \
                not any(rect.colliderect(i) for i in items):
                items.append(rect)
                break
    return items
#장애물 및 아이템 생성
obstacles = create_obstacles(5, 50 , screen_width, screen_height)
items = create_items(10, 20 , screen_width, screen_height ,obstacles)
#이동하는 rect생성
monster = pygame.image.load("kkk.png")
monster_rect = monster.get_rect()
monster_rect_width = monster_rect.width
monster_rect_height = monster_rect.height
monster_rect.x = monster_rect.y 
monster_rect.y = monster_rect.x

while True:
    #이동하는 객체 랜덤 위치 
    random_x = random.randint(0, screen_width - monster_rect_width)
    random_y = random.randint(0, screen_height - monster_rect_height)
    temp_rect = pygame.Rect(random_x, random_y, monster_rect_width, monster_rect_height)
    #장애물 및 아이템과 겹치지 않는 위치 찾기
    if temp_rect.collidelist(obstacles) == -1 and temp_rect.collidelist(items) == -1:
        monster_rect.topleft = (random_x, random_y)
        break

#이동 속도 설정
velocity = 300
#fps 제어위한 clock 객체생성
clock = pygame.time.Clock()
#게임 시작
running = True
scale_factor =1.0 #이미지 커지게 하기위해

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    previous_position = monster_rect.topleft

    dt = clock.tick(60)/1000.0
#키입력에 따른 이동처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        monster_rect.x -= velocity * dt
    if keys[pygame.K_RIGHT]:
        monster_rect.x += velocity * dt
    if keys[pygame.K_UP]:
        monster_rect.y -= velocity * dt
    if keys[pygame.K_DOWN]:
        monster_rect.y += velocity * dt
    #장애물 충돌 처리
    collision_index = monster_rect.collidelist(obstacles)
    if collision_index != -1:
        print(f"장애물 {collision_index}와 충돌 ! 성식이 아픔!병원감  ")
        monster_rect.topleft = previous_position
        screen.fill(BLUE)
        pygame.display.flip()
        running = False
    #아이템 충돌 처리
    item_index = monster_rect.collidelist(items)
    if item_index != -1:
        print(f"성식이 먹이 나머지:{len(items)-1}")
        del items[item_index]
        scale_factor += 0.1  # -> 이미지 커지는 
        # 이미지 커지게해줌
        monster = pygame.transform.scale(monster, 
                        (int(monster_rect_width * scale_factor), 
                         int(monster_rect_height * scale_factor)))
        monster_rect = monster.get_rect(center=monster_rect.center)
       
    if not items:
        print("성식이 다 먹음!") 
        running = False

    screen.fill(WHITE)

    for obs in obstacles:
        pygame.draw.rect(screen, BLUE, obs)

    for item in items:
        pygame.draw.rect(screen ,YELLOW, item)
    
    screen.blit(monster,monster_rect)
    

    pygame.display.flip()


pygame.quit()