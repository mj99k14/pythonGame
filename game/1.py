import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("성식이 구하기 ")
#색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#게임 패들 
# 패들 설정
paddle_width = 100
paddle_height = 10
paddle_speed = 500
paddle = pygame.Rect(350, 550, paddle_width, paddle_height)


The_end = pygame.image.load("theend.png")
The_end_rect = The_end.get_rect()
The_end_rect.topleft = (250,150)
# 공 설정
ball_image = pygame.image.load("kkk.png")
ball_rect = ball_image.get_rect()
ball_rect.topleft =(350, 350)
ball_speed = [5, -5]
# 게임 속도 설정
clock = pygame.time.Clock()
fps = 60

ball_count = 0
running = True
while running:
    dt = clock.tick(30) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #패들 움직이기
    keys = pygame.key.get_pressed()
    # 왼쪽 방향키가 눌러졌을 때
    if keys[pygame.K_LEFT]:
        paddle.x = paddle.x - paddle_speed * dt
    # 오른쪽 방향키가 눌러졌을 때
    if keys[pygame.K_RIGHT]: 
        paddle.x += paddle_speed * dt 
    #패들이 화면안에서 움직이기위해서
    # paddle.x += speed * dt
   
    #왼쪽 오른쪽 부딪힘
    if paddle.x + paddle.width > screen.get_width():
        paddle.x = screen.get_width() - paddle.width
        paddle_speed = -paddle_speed 
    if paddle.x < 0:
        paddle.x = 0
        paddle_speed = -paddle_speed
    #위아래 부딪힘
    if paddle.bottom > screen.get_height():
        paddle.y = screen.get_height() - paddle.height
        paddle_speed = -paddle_speed
    if paddle.y < 0:
        paddle.y = 0
        paddle_speed = -paddle_speed       
    # 공 이동 
    ball_rect.x += ball_speed[0]
    ball_rect.y += ball_speed[1]

    #공이 화면밖에 나가지않도록
    if ball_rect.x + ball_rect.width > screen.get_width():
        ball_rect.x = screen.get_width() - ball_rect.width
        ball_speed[0] = -ball_speed[0]
    if ball_rect.x < 0:
        ball_rect.x = 0
        ball_speed[0] = -ball_speed[0]
    #위아래 부딪힘
    
    # 공과 벽 충돌
    if ball_rect.left <= 0 or ball_rect.right >= screen.get_width():
        ball_speed[0] = -ball_speed[0]
    if ball_rect.top <= 0:
        ball_speed[1] = -ball_speed[1]
        

    #공이랑 패드가 부딪힘
    if ball_rect.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]
        ball_count += 1
        print(f"COUNT:{ball_count} ")
        ball_speed[0] *1.1
        ball_speed[1]* 1.1
        
        
    
    #공이 바닥이랑 부딪힘
    if ball_rect.bottom >= screen.get_height():
        screen.fill(BLACK)
        screen.blit(The_end,The_end_rect) #_> 이미지를 화면에 그리는 데 사용 screen.blit(image, (x, y))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
        
   
    screen.fill(BLACK)
    screen.blit(ball_image,ball_rect)
    # pygame.draw.ellipse(screen, WHITE, ball_rect)
    pygame.draw.rect(screen, (0, 0, 255), paddle) # Rect 객체 이용
    pygame.display.flip()
    
    
pygame.quit()
