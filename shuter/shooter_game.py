
from pygame import *
from random import randint
from time import time as timer


'''window'''
win_width = 700
win_height = 500
display.set_caption('Космическая битва')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))



score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
max_lost = 1
goal = 60
life = 1


'''class'''
class GameSprite(sprite.Sprite):
    '''psrent_class for other classes'''
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        '''констркутор класса'''
        sprite.Sprite.__init__(self)

        '''каждый спрайт хранит св-во изображения'''
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        ''''''
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        '''method for paint hero'''
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    ''''''
    def update(self)  :
        ''''''
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        '''fire'''
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    '''enemy sprite'''
    def update(self):
        self.rect.y += self.speed
        global lost
        '''исчезает, если дойдет до края'''
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost += 1


class AsteroidEnemy(GameSprite):
    '''enemy sprite'''
    def update(self):
        self.rect.y += self.speed
        '''исчезает, если дойдет до края'''
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0


class Bullet(GameSprite):
    '''class sprite_bullet'''
    def update(self):
        ''''''
        self.rect.y += self.speed
        '''исчезает если дойдет до края экрана'''
        if self.rect.y < 0:
            self.kill()

'''player sprite'''
ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

'''asteroid'''
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = AsteroidEnemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)


'''fone music'''
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


'''шрифт и надпись'''
font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)
win = font1.render('Победа', True, (255, 255, 255))
lose = font1.render('Поражение', True, (194, 0, 0))

'''game cicle'''
finish = False
run = True

rel_time = False
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if not rel_time and num_fire < 5:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    '''if player fire 5 '''
                    last_time = timer()
                    rel_time = True



    if not finish:
        '''Обновл. фон'''
        window.blit(background, (0, 0))

        '''текст'''
        text = font2.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text, (10, 50))



        '''движ. спрайтов'''
        ship. update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)


        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Перезарядка...', 1, (170, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, False)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


        '''если спрайт коснулся врага-уменьшается жизнь'''
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
             sprite.spritecollide(ship, monsters, True)
             sprite.spritecollide(ship, asteroids, True)
             life -= 1


        '''возможный проигрыш - герой столкнулся с врагом'''
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))


        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        '''color life'''
        if life == 1:
            life_color = (152, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))


    time.delay(50)
    display.update()































