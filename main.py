import random
import pygame
import os
WIDTH = 500  # 介面寬
HEIGHT = 600  # 介面高
FPS = 60  # 更新畫面頻率
# 顏色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# 遊戲初始化、創建視窗
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
pygame.display.set_caption("阿星的小遊戲")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
# 載入圖片

background_img = pygame.image.load(os.path.join(
    "PYGAME\\img", "background.png")).convert()
player_img = pygame.image.load(os.path.join(
    "PYGAME\\img", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)  # 左上角的圖標
# rock_img = pygame.image.load(os.path.join("PYGAME\\img","rock.png")).convert()
bullet_img = pygame.image.load(os.path.join(
    "PYGAME\\img", "bullet.png")).convert()

rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join(
        "PYGAME\\img", f"rock{i}.png")).convert())
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []

for i in range(9):
    expl_img = pygame.image.load(os.path.join(
        "PYGAME\\img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))

    player_expl_img = pygame.image.load(os.path.join(
        "PYGAME\\img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)

power_imgs = {}
power_imgs['shield'] = pygame.image.load(
    os.path.join("PYGAME\\img", "shield.png")).convert()
power_imgs['gun'] = pygame.image.load(
    os.path.join("PYGAME\\img", "gun.png")).convert()

# 載入音樂、音效
shoot_sound = pygame.mixer.Sound(os.path.join("PYGAME\\sound", "shoot.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("PYGAME\\sound", "pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("PYGAME\\sound", "pow0.wav"))
die_sound = pygame.mixer.Sound(os.path.join("PYGAME\\sound", "rumble.ogg"))
shoot_sound_setmusic = pygame.mixer.music.set_volume(0.1)

expl_sound = [
    pygame.mixer.Sound(os.path.join("PYGAME\\sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("PYGAME\\sound", "expl1.wav"))
]
pygame.mixer.music.load(os.path.join("PYGAME\\sound", "background.ogg"))
pygame.mixer.music.set_volume(0.1)  # 音樂聲音大小


def new_rock():
    r = ROCK()
    all_sprites.add(r)
    rocks.add(r)


def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


font_name = os.path.join("PYGAME\\font.ttf")  # 用出字體


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, '太空生存戰', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, '← →移動飛船 空白鍵發射子彈~', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按任意鍵開始遊戲', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
    # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False


# Player操控sprite
class Player(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))  # 創建物品大小
        self.image.set_colorkey(BLACK)  # 將黑框去掉
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius) 顯示實體範圍
        # self.rect.x=400#創建物品x座標
        # self.rect.y=400#創建物品y座標
        self.rect.centerx = WIDTH / 2  # 直接讓物品在中間寫法
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pygame.time.get_ticks()

        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        keypressed = pygame.key.get_pressed()

        if keypressed[pygame.K_d] or keypressed[pygame.K_RIGHT]:  # 判斷右鍵有沒有被按

            self.rect.x += self.speedx

        if keypressed[pygame.K_a] or keypressed[pygame.K_LEFT]:  # 判斷左鍵有沒有被按

            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:

            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not(self.hidden):  # 死亡後無法射擊
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT+500)

    def groups(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()
# ROCK物件
class ROCK(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        # self.image = pygame.transform.scale(rock_img ,(100,58))

        self.rect = self.image.get_rect()

        self.radius = int(self.rect.width * 0.8 / 2)  # 物品大小

        # pygame.draw.circle(self.image,RED, self.rect.center, self.radius)

        self.rect.x = random.randrange(0, WIDTH - self.rect.width)  # 創建物品x座標

        self.rect.y = random.randrange(-180, -100)  # 創建物品y座標

        self.speedy = random.randrange(2, 18)  # 降落速度

        self.speedx = random.randrange(-3, 5)
        self.total_degree = 0
        self.rot_degree = 3
        # self.rot_degree = random.randrange(-3,3)

        # self.image_ori = rock_img

# 設定中心點
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)

        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy

        self.rect.x += self.speedx

        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:

            self.rect.x = random.randrange(0, WIDTH-self.rect.width)

            self.rect.y = random.randrange(-100, -40)

            self.speedy = random.randrange(5, 10)

            self.speedx = random.randrange(-3, 5)
            self.total_degree = 0


all_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

rock = ROCK()

all_sprites.add(rock)

for i in range(15):  # 石頭數量

    r = ROCK()
    all_sprites.add(r)


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.image = bullet_img  # 創建物品大小
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom <= 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):

    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

# 掉寶


class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


pygame.mixer.music.play(-1)

# 遊戲迴圈
show_init = True
RUNNING = True
while RUNNING:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        rock = ROCK()
        for i in range(10):
            new_rock()
        score = 0

    clock.tick(FPS)
    # 取得輸入
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # 判斷石頭、飛船相撞
    hits = pygame.sprite.spritecollide(
        player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        player.health -= hit.radius * 3  # 石頭攻擊力
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0:
            die = Explosion(player.rect.center, 'player')
            all_sprites.add(die)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()

    # 判斷寶物、飛船相撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 20
            if player.health > 100:
                player.health = 100
                shield_sound.play()

        elif hit.type == 'gun':
            player.groups()
            gun_sound.play()

    if player.lives == 0 and not(die.alive()):
        show_init = True

    # 畫面顯示
    screen.fill(BLACK)  # 介面顏色
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    pygame.display.update()

    # 更新遊戲
    all_sprites.update()

    # 判斷石頭、子彈相撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(expl_sound).play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.95:  # 掉寶機率 0.9=9成機率
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()

pygame.quit()