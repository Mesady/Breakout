
import pygame
from InputBox import InputBox
from lelvel import Level
import sys
from pygame.locals import *
from DataBaseWork import ServiceDB

RED = (255, 0, 0)
WHITE = (255, 255, 255)
sound_volume = 1

pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")

font = pygame.font.SysFont('Broadway', 50)

mainClock = pygame.time.Clock()

bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, size)


sound1 = pygame.mixer.Sound('bgmusick.mp3')
channel = pygame.mixer.find_channel(True)
channel.set_volume(sound_volume*0.01)
channel.play(sound1)

name_saver = ''

dbworker = ServiceDB()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def init_level_choice(name_saver, dbworker):
    click = False
    while True:
        screen.blit(bg, (0, 0))
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(300, 100, 170, 40)
        button_2 = pygame.Rect(300, 200, 170, 40)
        button_3 = pygame.Rect(300, 300, 170, 40)
        button_4 = pygame.Rect(300, 400, 170, 40)
        if button_1.collidepoint((mx, my)):
            draw_text(' Level 1', font, RED, screen, 300, 100)
            if click:
                Level(screen, bg, 1, name_saver, dbworker, channel)
        else:
            draw_text(' Level 1', font, WHITE, screen, 300, 100)
        if button_2.collidepoint((mx, my)):
            draw_text(' Level 2', font, RED, screen, 300, 200)
            if click:
                Level(screen, bg, 2, name_saver, dbworker, channel)
        else:
            draw_text(' Level 2', font, WHITE, screen, 300, 200)
        if button_3.collidepoint((mx, my)):
            draw_text(' Level 3', font, RED, screen, 300, 300)
            if click:
                Level(screen, bg, 3, name_saver, dbworker, channel)
        else:
            draw_text(' Level 3', font, WHITE, screen, 300, 300)
        if button_4.collidepoint((mx, my)):
            draw_text(' Back', font, RED, screen, 300, 400)
            if click:
                main_menu(name_saver)
        else:
            draw_text(' Back', font, WHITE, screen, 300, 400)
        click = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def options_menu(name_saver):
    click = False
    global sound_volume
    button_2 = pygame.Rect(300, 300, 170, 40)
    slider_main_road = pygame.Rect(210, 200, 320, 10)
    slider_right_end = pygame.Rect(210, 185, 10, 40)
    slider_left_end = pygame.Rect(530, 185, 10, 40)
    slider = pygame.Rect(((sound_volume * 10) + 225), 195, 30, 20)
    while True:
        screen.blit(bg, (0, 0))
        mx, my = pygame.mouse.get_pos()
        if slider_main_road.collidepoint((mx, my)):
            if click:
                if mx > 510:
                    slider.x = 500
                elif mx < 240:
                    slider.x = 220
                else:
                    slider.x = mx-15
                sound_volume = int((slider.x-220)/10)
                channel.set_volume(sound_volume*0.01)
                str1 = 'GameDataBase.PLAYER_NAME="' + name_saver + '"'
                int(sound_volume)
                str2 = 'GameDataBase.VALUME_SETTINGS=' + str(sound_volume)
                dbworker.execute_update('GameDataBase', str2, str1)
        if button_2.collidepoint((mx, my)):
            draw_text(' Back', font,RED, screen, 300, 300)
            if click:
                main_menu(name_saver)
        else:
            draw_text(' Back', font, WHITE, screen, 300, 300)
        draw_text(' Musick volume', font, WHITE, screen, 200, 100)
        pygame.draw.rect(screen, WHITE, slider_main_road)
        pygame.draw.rect(screen, WHITE, slider_right_end)
        pygame.draw.rect(screen, WHITE, slider_left_end)
        pygame.draw.rect(screen, (200, 200, 200), slider)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def leaderboard(name_saver):
    click = False
    button_1 = pygame.Rect(360, 520, 170, 100)
    while True:
        font = pygame.font.SysFont('Broadway', 30)
        screen.blit(bg, (0, 0))
        mx, my = pygame.mouse.get_pos()
        draw_text('TOP 10 BEST PLAYERS', font, WHITE, screen, 20, 10)
        draw_text('YOUR SCORE', font, WHITE, screen, 470, 10)
        draw_text('# NICKNAME L1 L2 L3', font, WHITE, screen, 20, 40)
        res = dbworker.execute_select('GameDataBase', fields=['GameDataBase.PLAYER_NAME', 'GameDataBase.LEVEL1_MAX_SCORE',
                                                              'GameDataBase.LEVEL2_MAX_SCORE', 'GameDataBase.LEVEL3_MAX_SCORE'],
                                                        order_by='GameDataBase.LEVEL1_MAX_SCORE+GameDataBase.LEVEL2_MAX_SCORE+GameDataBase.LEVEL3_MAX_SCORE')
        i = 0
        for item in res:
            str1 = str(i+1)+' '
            str1 += ' '.join(str(e) for e in res[i])
            draw_text(str1, font, WHITE, screen, 20, 90+i*55)
            i += 1
        str1 = 'select GameDataBase.PLAYER_NAME,GameDataBase.LEVEL1_MAX_SCORE,GameDataBase.LEVEL2_MAX_SCORE,''GameDataBase.LEVEL3_MAX_SCORE from GameDataBase where GameDataBase.PLAYER_NAME="'+name_saver+'"'
        dbworker.cursor.execute(str1)
        res = dbworker.cursor.fetchall()
        i = 0
        for item in res:
            str1 = ' '
            str1 += ' '.join(str(e) for e in res[i])
            draw_text(str1, font, WHITE, screen, 470, 50+i*40)
            i += 1
        if button_1.collidepoint((mx, my)):
            draw_text(' Back', font, RED, screen, 360, 550)
            if click:
                main_menu(name_saver)
        else:
            draw_text(' Back ', font, (255,255, 255), screen,  360, 550)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
               if event.button == 1:
                 click = True

            pygame.display.update()
            mainClock.tick(60)


def login_input(name_saver):
    clock = pygame.time.Clock()
    input_box1 = InputBox(300, 100, 470, 30)
    done = False
    font = pygame.font.SysFont('Broadway', 40)
    click = False
    global sound_volume
    while not done:
        button_1 = pygame.Rect(260, 260, 310, 40)
        screen.blit(bg, (0, 0))
        mx, my = pygame.mouse.get_pos()
        draw_text('Write player name and press enter', font, WHITE, screen, 20, 40)
        draw_text('or', font, WHITE, screen, 380, 170)
        if button_1.collidepoint((mx, my)):
            draw_text('just press me', font, RED, screen, 260, 260)
            if click:
                name_saver = 'NoName'
        else:
            draw_text('just press me', font, WHITE, screen, 260, 260)
        click = False
        input_box1.draw(screen)
        pygame.display.flip()
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            name_saver = input_box1.handle_event(event)
            input_box1.update()
        if name_saver != None:
            done = True
    if name_saver == None:
        name_saver = 'NoName'
    str1 = 'select GameDataBase.PLAYER_NAME,GameDataBase.LEVEL1_MAX_SCORE,GameDataBase.LEVEL2_MAX_SCORE,GameDataBase.LEVEL3_MAX_SCORE from GameDataBase where GameDataBase.PLAYER_NAME="' + name_saver + '"'
    dbworker.cursor.execute(str1)
    res = dbworker.cursor.fetchall()
    str2='"' + name_saver + '"' + ',1,0,0,0'
    if res==[]:
        dbworker.execute_insert('GameDataBase','PLAYER_NAME,VALUME_SETTINGS ,LEVEL1_MAX_SCORE ,LEVEL2_MAX_SCORE ,LEVEL3_MAX_SCORE',str2)
    str1 = 'select GameDataBase.VALUME_SETTINGS from GameDataBase where GameDataBase.PLAYER_NAME="' + name_saver + '"'
    dbworker.cursor.execute(str1)
    res = dbworker.cursor.fetchall()
    for item in res:
        str1 = ' '
        str1 += ' '.join(str(e) for e in res[0])
        sound_volume=int(str1)
    channel.set_volume(sound_volume*0.01)
    main_menu(name_saver)


def main_menu(name_saver):
    click = False
    while True:
        font = pygame.font.SysFont('Broadway', 50)
        screen.blit(bg, (0, 0))
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(250, 120, 170, 40)
        button_2 = pygame.Rect(250, 220, 190, 40)
        button_3 = pygame.Rect(250, 320, 370, 40)
        button_4 = pygame.Rect(250, 420, 370, 40)
        button_5 = pygame.Rect(250, 520, 170, 40)
        if button_1.collidepoint((mx, my)):
            draw_text(' Play', font, RED, screen, 250, 120)
            if click:
                init_level_choice(name_saver,dbworker)
        else:
            draw_text(' Play ', font, (255,255, 255), screen,  250, 120)

        if button_2.collidepoint((mx, my)):
            draw_text(' Options', font, RED, screen, 250, 220)
            if click:
                options_menu(name_saver)
        else:
            draw_text(' Options ', font, WHITE, screen, 250, 220)

        if button_3.collidepoint((mx, my)):
            draw_text(' Leaderboard', font, RED, screen, 250, 320)
            if click:
                leaderboard(name_saver)
        else:
            draw_text(' Leaderboard ', font, (255,255, 255), screen,  250, 320)

        if button_4.collidepoint((mx, my)):
            draw_text(' Change name', font, RED, screen, 250, 420)
            if click:
                name_saver = None
                login_input(name_saver)
        else:
            draw_text(' Change name ', font, (255,255, 255), screen,  250, 420)

        if button_5.collidepoint((mx, my)):
            draw_text(' Quit', font, RED, screen, 250, 520)
            if click:
                pygame.quit()
                sys.exit()
        else:
            draw_text(' Quit ', font, (255,255, 255), screen,  250, 520)

        draw_text(' Breakout', font, WHITE, screen, 250, 40)
        font = pygame.font.Font(None, 34)
        text = font.render("Now playing: " + name_saver, 1, WHITE)
        screen.blit(text, (20, 10))
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


login_input(name_saver)