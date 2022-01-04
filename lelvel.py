
import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick
from wall import Wall

class Level():
    def __init__(self, screen,bg,levelnuber,name_saver,dbworker,channel):
        super().__init__()
        WHITE = (255, 255, 255)
        LIGHTBLUE = (0, 176, 240)
        RED = (255, 0, 0)
        ORANGE = (255, 100, 0)
        YELLOW = (255, 255, 0)

        score = 0
        lives = 3

        all_sprites_list = pygame.sprite.Group()

        paddle = Paddle(LIGHTBLUE, 100, 10)
        paddle.rect.x = 350
        paddle.rect.y = 560

        ball = Ball(WHITE, 10, 10)
        ball.rect.x = 345
        ball.rect.y = 300
        all_bricks = pygame.sprite.Group()
        for i in range(36):
            brick = Brick(RED, 20, 20)
            brick.rect.x = i * 22 + 3
            brick.rect.y = 60
            all_sprites_list.add(brick)
            all_bricks.add(brick)
        for i in range(36):
            brick = Brick(ORANGE, 20, 20)
            brick.rect.x = i * 22 + 3
            brick.rect.y = 90
            all_sprites_list.add(brick)
            all_bricks.add(brick)
        for i in range(36):
            brick = Brick(YELLOW, 20, 20)
            brick.rect.x = i * 22 + 3
            brick.rect.y = 120
            all_sprites_list.add(brick)
            all_bricks.add(brick)
        for i in range(36):
            brick = Brick(LIGHTBLUE, 20, 20)
            brick.rect.x = i * 22 + 3
            brick.rect.y = 150
            all_sprites_list.add(brick)
            all_bricks.add(brick)

        all_sprites_list.add(paddle)
        all_sprites_list.add(ball)

        if levelnuber == 2:

            wall = Wall(ORANGE, 380, 10)
            wall.rect.x = 0
            wall.rect.y = 200

            wall2 = Wall(ORANGE, 390, 10)
            wall2.rect.x = 430
            wall2.rect.y = 200

            all_sprites_list.add(wall)
            all_sprites_list.add(wall2)

        if levelnuber == 3:

                all_walls = pygame.sprite.Group()
                for i in range(8):
                    wall = Wall(RED, 5, 300)
                    wall.rect.x = i *110 + 3
                    wall.rect.y = 200
                    all_sprites_list.add(wall)
                    all_walls.add(wall)

        carryOn = True
        clock = pygame.time.Clock()
        sound1 = pygame.mixer.Sound('gamebgmusick.mp3')
        channel.play(sound1)
        while carryOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    carryOn = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.moveLeft(5)
            if keys[pygame.K_RIGHT]:
                paddle.moveRight(5)

            all_sprites_list.update()

            if ball.rect.x >= 790:
                ball.velocity[0] = -ball.velocity[0]
            if ball.rect.x <= 0:
                ball.velocity[0] = -ball.velocity[0]
            if ball.rect.y > 590:
                ball.velocity[1] = -ball.velocity[1]
                lives -= 1
                if lives == 0:
                    str1 = 'GameDataBase.PLAYER_NAME="' + name_saver+'"'
                    if levelnuber==1:
                        str2 = 'LEVEL1_MAX_SCORE='+str(score)
                        dbworker.execute_update('GameDataBase',str2,str1)
                    if levelnuber==2:
                        str2 = 'LEVEL2_MAX_SCORE='+str(score)
                        dbworker.execute_update('GameDataBase', str2,str1)
                    if levelnuber==3:
                        str2 = 'LEVEL3_MAX_SCORE='+str(score)
                        dbworker.execute_update('GameDataBase', str2, str1)
                    font = pygame.font.Font(None, 74)
                    text = font.render("GAME OVER", 1, WHITE)
                    screen.blit(text, (250, 300))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    carryOn = False

            if ball.rect.y < 40:
                ball.velocity[1] = -ball.velocity[1]

            if pygame.sprite.collide_mask(ball, paddle):
                ball.rect.x -= ball.velocity[0]
                ball.rect.y -= ball.velocity[1]
                ball.bounce()

            if levelnuber == 2:
                if pygame.sprite.collide_mask(ball, wall):
                    ball.rect.x -= ball.velocity[0]
                    ball.rect.y -= ball.velocity[1]
                    ball.bounce()

                if pygame.sprite.collide_mask(ball, wall2):
                    ball.rect.x -= ball.velocity[0]
                    ball.rect.y -= ball.velocity[1]
                    ball.bounce()
            if levelnuber == 3:

                for wall in all_walls:
                    if pygame.sprite.collide_mask(ball, wall):
                        ball.rect.x -= ball.velocity[0]
                        ball.rect.y -= ball.velocity[1]
                        ball.bounce()

            brick_collision_list = pygame.sprite.spritecollide(ball, all_bricks, False)
            for brick in brick_collision_list:
                ball.bounce()
                score += 1
                brick.kill()
                str1 = 'GameDataBase.PLAYER_NAME="' + name_saver+'"'
                if len(all_bricks) == 0:
                    if levelnuber==1:
                        str2 = 'LEVEL1_MAX_SCORE='+str(score)
                        dbworker.execute_update('GameDataBase',str2,str1)
                    if levelnuber==2:
                        str2 = 'LEVEL2_MAX_SCORE='+str(score)
                        dbworker.execute_update('GameDataBase', str2,str1)
                    if levelnuber==3:
                        str2 = 'LEVEL3_MAX_SCORE='+str(score)
                        dbworker.execute_update('GameDataBase', str2, str1)
                    font = pygame.font.Font(None, 74)
                    text = font.render("LEVEL COMPLETE", 1, WHITE)
                    screen.blit(text, (200, 300))
                    pygame.display.flip()
                    pygame.time.wait(3000)

                    carryOn = False

            screen.blit(bg, (0, 0))
            pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

            font = pygame.font.Font(None, 34)
            text = font.render("Score: " + str(score), 1, WHITE)
            screen.blit(text, (20, 10))
            text = font.render("Lives: " + str(lives), 1, WHITE)
            screen.blit(text, (650, 10))

            all_sprites_list.draw(screen)

            pygame.display.flip()

            clock.tick(90)
        sound1 = pygame.mixer.Sound('bgmusick.mp3')
        channel.play(sound1)
