#Создай собственный Шутер
from pygame import *
from random import *
from time import time as timer
font.init()
window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_w, player_h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_w, player_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 10, 20)
        bullets.add(bullet)

lost = 0
koki = 0
saba = 0
num_fire = 0
rel_time = False
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            global lost
            lost += 1
            self.rect.x = randint(0,635)
            self.rect.y = 0
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Asterouds(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            global lost
            self.rect.x = randint(0,635)
            self.rect.y = 0

pyk = True
finish = False  
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")

raceta = Player("rocket.png", 400, 430, 5, 65, 65)

monsters = sprite.Group()
for i in range(3):
    monster = Enemy("ufo.png", randint(0,635), 0, randint(1,2), 65, 40)
    monsters.add(monster)

asteroidiki = sprite.Group()
for i in range(2):
    asteroud = Enemy("asteroid.png", randint(0,635), 0, randint(1,4), 65, 40)
    asteroidiki.add(asteroud)


font1 = font.SysFont("Arial", 36)

font_3 = font.SysFont("Arial", 70)

bullets = sprite.Group()



while pyk:
    for e in event.get():
        if e.type == QUIT:
            pyk = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                if num_fire < 10 and rel_time == False:
                    raceta.fire()
                    num_fire += 1
                else:
                    rel_time = True
                    old_time = timer()

                
    if finish != True:
        text_lose1 = font1.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        text_lose2 = font1.render("Счет:"+ str(koki), 1, (255, 255, 255))
        #text_lose3 = font1.render("Жизни:"+ str(saba), 1, (255, 255, 255))
        text_WIN = font_3.render("YOU WIN!", True, (225, 215, 0))
        text_LOSe = font_3.render("YOU LOSE!", True, (225, 0, 0))
        window.blit(background, (0,0))
        raceta.reset()
        raceta.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroidiki.update()
        asteroidiki.draw(window)

        if rel_time == True:
            new_time = timer()
            if new_time - old_time >= 3:
                num_fire = 0
                rel_time = False
            else:
                text_PEREZARADKA = font1.render("Wait, reload..", True, (225, 0, 0))
                window.blit(text_PEREZARADKA, (250,450))


    

        sprite_list1 = sprite.spritecollide(raceta, monsters, False)
        sprite_list2 = sprite.groupcollide(monsters, bullets, True, True)
        sprite_list3 = sprite.spritecollide(raceta, asteroidiki, False)
        
        for s in sprite_list2:
            koki += 1
            monster = Enemy("ufo.png", randint(0,635), 0, randint(1,5), 65, 40)
            monsters.add(monster)

        if len(sprite_list1) > 0 or lost >= 10 or len(sprite_list3) > 0 :
            finish = True
            window.blit(text_LOSe, (200, 200))


        if koki >= 5 :
            finish = True
            window.blit(text_WIN, (200, 200))

        window.blit(text_lose1, (10,40))
        window.blit(text_lose2, (10,10))
        
        #window.blit(text_lose3, (420,10))
    display.update()
    clock.tick(FPS)




 