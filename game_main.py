import math
import pygame
from pygame import draw
from pygame.color import Color
from pygame.sprite import Sprite

from catapult import Catapult
from stone import Stone
from alien import Alien
from explosion import Explosion
from const import *

FPS = 60
stone_count = 5
alien1_count = 10
alien2_count = 0

def decrement_stones():
    global stone_count
    stone_count -= 1
    
def decrement_aliens():
    global alien1_count
    alien1_count -= 1
    global alien2_count
    alien2_count -= 1

class Background(Sprite):
    def __init__(self):
        self.sprite_image = 'background.png'
        self.image = pygame.image.load(
            self.sprite_image).convert()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.dx = 1

        Sprite.__init__(self)

    def update(self):
        self.rect.x -= self.dx
        if self.rect.x == -800:
            self.rect.x = 0
                
if __name__ == "__main__":
    pygame.init()

    size = (400, 300)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Catapult VS Alien")

    run = True
    clock = pygame.time.Clock()
    t = 0
    fire_sound = pygame.mixer.Sound('fire.ogg')
    crash_sound = pygame.mixer.Sound('crash.ogg')

    power = 15
    direction = 45

    game_state = GAME_INIT
    background = Background()
    background_group = pygame.sprite.Group()
    background_group.add(background)

    stone = Stone()
    stone.rect.y = -100 #위치 변경
    stone_group = pygame.sprite.Group()
    stone_group.add(stone)

    catapult = Catapult(stone)
    catapult.rect.x = 50 #위치 변경
    catapult.rect.y = BASE_Y
    catapult_group = pygame.sprite.Group()
    catapult_group.add(catapult)

    alien1 = Alien()
    alien1.rect.x = 350
    alien1.rect.y = BASE_Y
    alien1_group = pygame.sprite.Group()
    alien1_group.add(alien1)

    alien2 = Alien()
    alien2.rect.x = 350
    alien2.rect.y =BASE_Y
    alien2_group = pygame.sprite.Group()
    alien2_group.add(alien2)

    explosion1 = Explosion()
    explosion1_group = pygame.sprite.Group()
    explosion1_group.add(explosion1)

    explosion2 = Explosion()
    explosion2_group = pygame.sprite.Group()
    explosion2_group.add(explosion2)

    #게임 루프
    while run:
        # 1) 사용자 입력 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    #초기화면에서 스페이스를 입력하면 시작
                    if game_state == GAME_INIT:
                        game_state = GAME_PLAY
                    elif game_state == GAME_PLAY:
                        #GAME_PLAY 상태일 때 스페이스를 입력하면 발사
                        if stone.state == STONE_READY:
                            t = 0
                            catapult.fire(power, direction)
                            fire_sound.play()

        if game_state == GAME_PLAY:
            # 누르고 있는 키 확인하기.
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                catapult.backward()
            elif keys[pygame.K_RIGHT]:
                catapult.forward()
            elif keys[pygame.K_UP]:
                if direction < MAX_DIRECTION:
                    direction += 1
            elif keys[pygame.K_DOWN]:
                if direction > MIN_DIRECTION:
                    direction -= 1
            elif keys[pygame.K_SPACE]:
                if power > MAX_POWER:
                    power = MIN_POWER
                else:
                    power += 0.2
            elif keys[pygame.K_LSHIFT]:
                catapult.isJump+=1
                
        # 2) 게임 상태 업데이트
        if stone.state == STONE_FLY:
            t += 0.5
            stone.move(t,
                       (screen.get_width(), screen.get_height()),
                       decrement_stones)            
        elif not stone.alive():
            
            stone = Stone()
            stone.rect.x = -100
            stone.rect.y = -100
            stone_group.add(stone)
            catapult.stone = stone

        if alien1.alive():
            collided = pygame.sprite.groupcollide(
                        stone_group, alien1_group, False, True)
            if collided:
                 # 폭발 좌표값 구하기
                explosion1.rect.x = \
                    (alien1.rect.x + alien1.rect.width/2) - \
                    explosion1.rect.width/2
                explosion1.rect.y = \
                    (alien1.rect.y + alien1.rect.height/2) - \
                    explosion1.rect.height/2
                crash_sound.play()

        elif not explosion1.alive():
            alien1 = Alien()
            alien1.rect.x = 350
            alien1.rect.y = BASE_Y
            alien1_group.add(alien1)
            explosion1 = Explosion()        #폭발 새로 생성
            explosion1_group.add(explosion1)

        if alien2.alive():
            collided = pygame.sprite.groupcollide(
                        stone_group, alien2_group, False, True)
            if collided:
                explosion2.rect.x = (alien2.rect.x + alien2.rect.width/2) - explosion2.rect.width/2
                explosion2.rect.y = (alien2.rect.y + alien2.rect.height/2) - explosion2.rect.height/2
                crash_sound.play()

        elif not explosion2.alive():
            alien2 = Alien()
            alien2.rect.x = 310
            alien2.rect.y = BASE_Y
            alien2_group.add(alien2)
            explosion2 = Explosion()
            explosion2_group.add(explosion2)
            
            #외계인이 죽고 폭발 애니메이션도 끝났을 때.
            
            alien1_count -= 1
            
            if alien1_count == 1:
                game_state = GAME_CLEAR

            alien2_count -= 1

            if alien2_count == 1:
                game_state = GAME_CLEAR

        #외계인1이 살아 있는데 돌맹이 수가 0이면 게임 오버.
        if alien1.alive() and stone_count == 0:
            game_state = GAME_OVER

        if alien2.alive() and stone_count == 0:
            pass

        if game_state == GAME_PLAY: #게임 객체 업데이트
            catapult_group.update()
            stone_group.update()
            alien1_group.update()
            alien2_group.update()

        # 3) 게임 상태 그리기
        background_group.update()
        background_group.draw(screen)

        if game_state == GAME_INIT:
            #초기화면
            sf = pygame.font.SysFont('Arial', 20, bold=True)
            title_str = "Catapult VS Alien1"
            title = sf.render(title_str, True, (255,0,0))
            title_size = sf.size(title_str)
            title_pos = (screen.get_width()/2 - title_size[0]/2, 100)

            sub_title_str = "Prss [Space] Key To Start"
            sub_title = sf.render(sub_title_str, True, (255,0,0))
            sub_title_size = sf.size(sub_title_str)
            sub_title_pos = (screen.get_width()/2 - sub_title_size[0]/2, 200)

            screen.blit(title, title_pos)
            screen.blit(sub_title, sub_title_pos)

        elif game_state == GAME_PLAY:
            #플레이 화면
            catapult_group.draw(screen)
            stone_group.draw(screen)
            alien1_group.draw(screen)
            alien2_group.draw(screen)

            #파워와 각도를 선으로 표현
            line_len = power*5
            r = math.radians(direction)
            pos1 = (catapult.rect.x+32, catapult.rect.y)
            pos2 = (pos1[0] + math.cos(r)*line_len,
                    pos1[1] - math.sin(r)*line_len)
            draw.line(screen, Color(255, 0, 0), pos1, pos2)

            #파워와 각도를 텍스트로 표현
            sf = pygame.font.SysFont("Arial", 15)
            text = sf.render("{0} ˚, {1} m/s".
                             format(direction, int(power)), True, (0,0,0))
            screen.blit(text, pos2)

            #돌의 개수를 표시
            sf = pygame.font.SysFont("Monospace", 20)
            text = sf.render('Stones : {0}'.
                             format(stone_count), True, (0,0,255))
            screen.blit(text, (10, 10))

            if not alien1.alive():
                explosion1_group.update()
                explosion1_group.draw(screen)

            if not alien2.alive():
                explosion2_group.update()
                explosion2_group.draw(screen)
            
        elif game_state == GAME_CLEAR:
             #게임 클리어
             sf = pygame.font.SysFont("Arial", 20, bold=True)
             title_str = "Congrations! Mission Complete"
             title = sf.render(title_str, True, (0,0,255))
             title_size = sf.size(title_str)
             title_pos = (screen.get_width()/2 - title_size[0]/2, 100)
             screen.blit(title, title_pos)

        elif game_state == GAME_OVER:
            #게임 오버
            sf = pygame.font.SysFont("Arial", 20, bold=True)
            title_str = "Game Over"
            title = sf.render(title_str, True, (255,0,0))
            title_size = sf.size(title_str)
            title_pos = (screen.get_width()/2 - title_size[0]/2, 100)
            screen.blit(title, title_pos)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


    #실행 코드
