from pygame import *
from random import randint
from time import time as timer

width = 900
height = 600

window = display.set_mode((width, height))
display.set_caption('galaxy')

back = transform.scale(image.load('galaxy.jpg'), (width, height))
window.blit(back, (0,0))
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 40)
font2 = font.Font(None, 80)
max_lost = 3  
lost = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x,size_y, player_speed):
        sprite.Sprite. __init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed           
        if keys[K_d] and self.rect.x < width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 7 , self.rect.top, 15,20,-15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= height:
            self.rect.x = randint(0, width - 80)
            self.rect.y = 0
            lost += 1
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= height:
            self.rect.x = randint(0, width - 50)
            self.rect.y = -50
            self.speed = randint(1, 3)  
            
ship = Player('rocket.png', 0, height - 100,80,100,10)
enemies = sprite.Group()
for i in range(6):
    enemy = Enemy('ufo.png', randint(0, width - 80),0, 80, 50, randint(1, 3))
    enemies.add(enemy)
bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(0, width - 50), randint(-150, -50), 50, 50, randint(2, 5))
    asteroids.add(asteroid)

def draw_pixel_heart(surf, x, y, size=30):
    red = (240, 50, 50)
    p = size // 5
    
    draw.rect(surf, red, (x + p, y, p, p))
    draw.rect(surf, red, (x + p*3, y, p, p))
    draw.rect(surf, red, (x, y + p, p*5, p))
    draw.rect(surf, red, (x + p, y + p*2, p*3, p))
    draw.rect(surf, red, (x + p*2, y + p*3, p, p))

game = True
finish = False
num_fire = 0
life = 3
rel_time = False
last_time = 0

win_text = font2.render('ВЫ ВЫИГРАЛИ!', True, (0, 255, 0))
lose_text = font2.render('ВЫ ПРОИГРАЛИ!', True, (255, 0, 0))


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    num_fire += 1
                    ship.fire()
                    fire_sound.play()
                    fire_sound.set_volume(0.1)

                if num_fire >= 5 and not rel_time:
                    rel_time = True
                    last_time = timer()

    if not finish:
        window.blit(back, (0, 0))
        
        ship.update()
        enemies.update()
        asteroids.update()
        bullets.update()
        
        ship.reset()
        enemies.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font1.render('ПЕРЕЗАРЯДКА...', True, (255, 0, 0))
                window.blit(reload_text, (width // 2 - 100, height - 50))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(enemies, bullets, True, True)
        for collide in collides:
            score += 1
            enemy = Enemy('ufo.png', randint(0, width - 80), randint(-40, 0), 80, 50, randint(1, 3))
            enemies.add(enemy)

        if sprite.spritecollide(ship, asteroids, True):
            life -= 1
            asteroid = Asteroid('asteroid.png', randint(0, width - 50), -50, 50, 50, randint(1,3))
            asteroids.add(asteroid)

        if sprite.spritecollide(ship, enemies, True):
            life -= 1
            enemy = Enemy('ufo.png', randint(0, width - 80), -40, 80, 50, randint(1, 3))
            enemies.add(enemy)

        if life <= 0 or lost >= max_lost:
            finish = True
            window.blit(lose_text, (width // 2 - 150, height // 2 - 40))

        if score >= 10:
            finish = True
            win_text = font2.render('YOU WIN!', True, (0, 255, 0))
            window.blit(win_text, (width // 2 - 150, height // 2 - 40))

        if life == 3:
            life_color = (0, 255, 0)
        elif life == 2:
            life_color = (255, 255, 0)
        else:
            life_color = (255, 0, 0)
            
        text_life = font1.render("Жизни: " + str(life), True, life_color)

        text_score = font1.render("Счет: " + str(score), True, (255, 255, 255))
        text_lost = font1.render("Пропущено: " + str(lost), True, (255, 255, 255))
        window.blit(text_score, (10, 20))
        window.blit(text_lost, (10, 50))

        for i in range(life):
            draw_pixel_heart(window, width - 50 - i * 45, 25, size=30)

    display.update()
    clock.tick(FPS)
    

