import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("벽돌꺠기")
#색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#게임 패들 
# 패들 설정
paddle_width = 60
paddle_height = 10
paddle_speed = 500
paddle = pygame.Rect(350, 550, paddle_width, paddle_height)
# ball_image = pygame.image.load("red_rect.png")
# 공 설정
ball_radius = 10
ball_speed = [5, -5]
ball = pygame.Rect(700, 300, ball_radius * 2, ball_radius * 2)
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
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]
    #공이 화면밖에 나가지않도록
    if ball.x + ball.width > screen.get_width():
        ball.x = screen.get_width() - ball.width
        ball_speed = -ball_speed 
    if ball.x < 0:
        ball.x = 0
        ball_speed = -ball_speed
    #위아래 부딪힘
    # 공과 벽 충돌
    if ball.left <= 0 or ball.right >= screen.get_width():
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]
        

    #공이랑 패드가 부딪힘
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]
        ball_count += 1
        print(f"count:{ball_count}")
        
    
    #공이 바닥이랑 부딪힘
    if ball.bottom >= screen.get_height():
        running = False
        print("The end~^_^ loser^_^")

    screen.fill((255, 255, 255))
    screen.fill(BLACK)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.rect(screen, (0, 0, 255), paddle) # Rect 객체 이용
    pygame.display.flip()
    
    
pygame.quit()
