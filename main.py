import pygame
import sys
import random
import pickle
import time

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
size = width, height = 320, 568

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Version 1.0.0')
pygame.mouse.set_visible(False)
pygame.mouse.set_pos((160, 520))

background_2 = pygame.image.load('picture\\background_2.png').convert_alpha()
bullet1 = pygame.image.load('picture\\bullet1.png').convert_alpha()
enemy1_blowup_1 = pygame.image.load('picture\\enemy1_blowup_1.png').convert_alpha()
enemy1_blowup_2 = pygame.image.load('picture\\enemy1_blowup_2.png').convert_alpha()
enemy1_blowup_3 = pygame.image.load('picture\\enemy1_blowup_3.png').convert_alpha()
enemy1_blowup_4 = pygame.image.load('picture\\enemy1_blowup_4.png').convert_alpha()
enemy1_fly_1 = pygame.image.load('picture\\enemy1_fly_1.png').convert_alpha()
enemy3_blowup_1 = pygame.image.load('picture\\enemy3_blowup_1.png').convert_alpha()
enemy3_blowup_2 = pygame.image.load('picture\\enemy3_blowup_2.png').convert_alpha()
enemy3_blowup_3 = pygame.image.load('picture\\enemy3_blowup_3.png').convert_alpha()
enemy3_blowup_4 = pygame.image.load('picture\\enemy3_blowup_4.png').convert_alpha()
enemy3_fly_1 = pygame.image.load('picture\\enemy3_fly_1.png').convert_alpha()
enemy3_hit_1 = pygame.image.load('picture\\enemy3_hit_1.png').convert_alpha()
hero_blowup_1 = pygame.image.load('picture\\hero_blowup_1.png').convert_alpha()
hero_blowup_2 = pygame.image.load('picture\\hero_blowup_2.png').convert_alpha()
hero_blowup_3 = pygame.image.load('picture\\hero_blowup_3.png').convert_alpha()
hero_blowup_4 = pygame.image.load('picture\\hero_blowup_4.png').convert_alpha()
hero_fly_1 = pygame.image.load('picture\\hero_fly_1.png').convert_alpha()
hero_fly_2 = pygame.image.load('picture\\hero_fly_2.png').convert_alpha()

bullet = pygame.mixer.Sound('sound\\bullet.wav')
game_music = pygame.mixer.Sound('sound\\game_music.wav')
game_over = pygame.mixer.Sound('sound\\game_over.wav')
enemy1_down = pygame.mixer.Sound('sound\\enemy1_down.wav')
enemy2_down = pygame.mixer.Sound('sound\\enemy2_down.wav')
enemy2_out = pygame.mixer.Sound('sound\\enemy2_out.wav')
enemy3_down = pygame.mixer.Sound('sound\\enemy3_down.wav')

def choose_enemy():
    enemy_index = random.randrange(30)
    if enemy_index < 25:
        return 1
    if enemy_index < 30:
        return 3
    return 2

def blowup_all(*groups):
    for i in groups:
        for j in i:
            j.blowup()

class Gray:
    def __init__(self, size):
        self.image = pygame.Surface(size).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.opacity = 0

    def darker(self):
        if self.opacity < 128:
            self.opacity += 1
            self.image.fill((0, 0, 0, self.opacity))

class Background:
    def __init__(self, image):
        temp_image = pygame.Surface((320, 1136)).convert_alpha()
        temp_image.blit(image, (0, 0))
        temp_image.blit(image, (0, 567))

        self.image = temp_image
        self.top = -568

    def scroll(self, distance):
        self.top += distance
        if self.top >= 0:
            self.top = -568

class Hero(pygame.sprite.Sprite):
    def __init__(self, fly_images, blowup_images):
        pygame.sprite.Sprite.__init__(self)

        self.status = False
        self.fly_images = fly_images
        self.blowup_images = blowup_images
        self.alive = True
        self.died = False
        
        self.rect = self.fly_images[0].get_rect()
        self.rect.left, self.rect.top = 170, 536

        self.dying_index = 0

        self.mask = pygame.mask.from_surface(self.fly_images[self.status])

    def move(self, pos):
        self.rect = self.fly_images[self.status].get_rect()
        self.rect.left, self.rect.top = pos
        self.mask = pygame.mask.from_surface(self.fly_images[self.status])

    def change_status(self):
        self.status = not self.status

    def die(self):
        self.alive = False

    def dying(self):
        self.dying_index += 1
        if self.dying_index == 4:
            self.died = True

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos

        self.mask = self.mask = pygame.mask.from_surface(self.image)

    def fly(self):
        self.rect.top -= 16

class Enemy1(pygame.sprite.Sprite):
    def __init__(self, fly_image, blowup_images, pos, difficulty):
        pygame.sprite.Sprite.__init__(self)
        
        self.fly_image = fly_image
        self.blowup_images = blowup_images
        self.rect = self.fly_image.get_rect()
        self.rect.left, self.rect.top = pos
        self.top = pos[1]
        self.speed = random.randrange(3200 - difficulty[0], 5301 - difficulty[1]) / 1000.0

        self.alive = True
        self.dying_index = 0
        self.died = False

        self.mask = pygame.mask.from_surface(self.fly_image)

    def fly(self):
        self.top += self.speed
        self.rect.top = self.top

    def blowup(self):
        self.alive = False

    def dying(self):
        self.dying_index += 1
        if self.dying_index == 4:
            self.died = True

class Enemy3(pygame.sprite.Sprite):
    def __init__(self, fly_image, blowup_images, hit_image, pos, difficulty, music):
        pygame.sprite.Sprite.__init__(self)

        self.music = music
        self.fly_image = fly_image
        self.blowup_images = blowup_images
        self.hit_image = hit_image
        self.rect = self.fly_image.get_rect()
        self.rect.left, self.rect.top = pos
        self.top = pos[1]
        self.speed = random.randrange(3200 - difficulty[0], 5301 - difficulty[1]) / 1500.0

        self.health = 8
        self.alive = True
        self.died = False
        self.dying_index = 0
        self.being_hit = False

        self.mask = pygame.mask.from_surface(self.fly_image)

    def fly(self):
        self.top += self.speed
        self.rect.top = self.top

    def hit(self):
        self.being_hit = True
        self.health -= 1
        if self.health == 0:
            self.alive = False
            self.music.play()

    def dying(self):
        self.dying_index += 1
        if self.dying_index == 4:
            self.died = True

    def change_status(self):
        if self.hit:
            self.being_hit = False

    def blowup(self):
        self.alive = False
        
# =============================================================================

def main():
    difficulty = [2000, 3000]
    score = 0
    
    game_music.play(-1)
    bullet.play(-1)

    font = pygame.font.SysFont('Verdana', 48)
    
    pygame.time.set_timer(24, 183) # shoot bullets
    pygame.time.set_timer(25, 100) # change status
    pygame.time.set_timer(26, 100) # enemy attacks
    pygame.time.set_timer(27, 50) # level up
    
    running = True

    background = Background(background_2)
    hero = Hero((hero_fly_1, hero_fly_2), (hero_blowup_1, hero_blowup_2, hero_blowup_3, hero_blowup_4))
    
    bullets = pygame.sprite.Group()
    enemies1 = pygame.sprite.Group()
    enemies2 = pygame.sprite.Group()
    enemies3 = pygame.sprite.Group()

    all_enemies = (enemies1, enemies2, enemies3)

    while running:
        print (difficulty)
        clock.tick(60)
        # ===== background ============================================================
        screen.blit(background.image, (0, background.top))
        background.scroll(0.5)
        # ===== event =================================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            if event.type == 24:
                bullets.add(Bullet(bullet1, [mouse_pos[0] - 2, mouse_pos[1] - 50]))
            if event.type == 25:
                # ===== hero ==================================================================
                hero.change_status()
                # ===== enemies1 ==============================================================
                for i in enemies1:
                    if not i.alive:
                        i.dying()
                        if i.died:
                            enemies1.remove(i)
                            continue
                # ===== enemies3 ==============================================================
                for i in enemies3:
                    i.change_status()
                    if not i.alive:
                        i.dying()
                        if i.died:
                            enemies3.remove(i)
                            continue
            if event.type == 26:
                enemy_index = choose_enemy()
                if enemy_index == 1:
                    enemies1.add(Enemy1(enemy1_fly_1, (enemy1_blowup_1, enemy1_blowup_2, enemy1_blowup_3, enemy1_blowup_4), [random.randrange(286), -24], difficulty))
                elif enemy_index == 3:
                    enemies3.add(Enemy3(enemy3_fly_1, (enemy3_blowup_1, enemy3_blowup_2, enemy3_blowup_3, enemy3_blowup_4), enemy3_hit_1, [random.randrange(286), -60], difficulty, enemy3_down))
                pygame.time.set_timer(26, random.randint(*difficulty))
            if event.type == 27:
                if difficulty[0] > 200:
                    difficulty[0] -= 1
                if difficulty[1] > 300:
                    difficulty[1] -= 1
                    
        # ===== collide ===============================================================
        for i in pygame.sprite.groupcollide(bullets, enemies1, True, False, pygame.sprite.collide_mask).values():
            for j in i:
                if j.alive:
                    score += 1000
                    enemy1_down.play()
                    j.blowup()
                    
        for i in pygame.sprite.groupcollide(bullets, enemies3, True, False, pygame.sprite.collide_mask).values():
            for j in i:
                j.hit()
                if not j.health:
                    score += 6000
                    enemy3_down.play()
        for i in all_enemies:
            if pygame.sprite.spritecollideany(hero, i, pygame.sprite.collide_mask):
                game_music.stop()
                bullet.stop()
                hero.die()
                blowup_all(enemies1, enemies3)
                enemy1_down.play()
                enemy2_down.play()
                enemy3_down.play()
                running = False
        # ===== hero ==================================================================
        hero.move((mouse_pos[0] - 33, mouse_pos[1] - 40))
        screen.blit(hero.fly_images[hero.status], hero.rect)
        # ===== bullets ===============================================================
        for i in bullets:
            screen.blit(i.image, i.rect)
            if i.rect.top <= -14:
                bullets.remove(i)
            i.fly()
        # ===== enemies3 ==============================================================
        for i in enemies3:
            if i.alive:
                if i.being_hit:
                    screen.blit(i.hit_image, i.rect)
                else:
                    screen.blit(i.fly_image, i.rect)
                i.fly()
            else:
                screen.blit(i.blowup_images[i.dying_index], i.rect)
            if i.rect.top >= 567:
                enemies3.remove(i)
        # ===== enemies1 ==============================================================
        for i in enemies1:
            if i.alive:
                screen.blit(i.fly_image, i.rect)
                i.fly()
            else:
                screen.blit(i.blowup_images[i.dying_index], i.rect)
            if i.rect.top >= 567:
                enemies1.remove(i)
        # ===== score =================================================================
        screen.blit(font.render(str(score), True, (0, 0, 0, 255)), (0, 0))
        # ===== end ===================================================================
        pygame.display.flip()

    if not hero.alive:
        running = True
    
    pygame.time.set_timer(24, 0)
    pygame.time.set_timer(26, 0)
    pygame.time.set_timer(27, 0)

    blowup_done = False
    setted_exit = False
    
    while running:
        clock.tick(60)
        enemy_number = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quitted = True
            if event.type == 25:
                # ===== hero ==================================================================
                hero.dying()
                # ===== enemy ================================================================
                for i in all_enemies:
                    for j in i:
                        j.dying()
            if event.type == 28:
                running = False
                quitted = False

        # ===== background ============================================================
        screen.blit(background.image, (0, background.top))
        background.scroll(0.5)
        # ===== hero ==================================================================
        if not hero.died:
            screen.blit(hero.blowup_images[hero.dying_index], hero.rect)
        # ===== enemy =================================================================
        for i in all_enemies:
            enemy_number += len(i)
            for j in i:
                if not j.died:
                    screen.blit(j.blowup_images[j.dying_index], j.rect)
                else:
                    i.remove(j)
        if not enemy_number:
            if not setted_exit:
                pygame.time.set_timer(28, 2000)
                setted_exit = True
        # ===== end ===================================================================
        pygame.display.flip()

    if not quitted:
        running = True
    
    game_over.play()
    pygame.time.set_timer(25, 0)
    pygame.time.set_timer(28, 0)
    pygame.mouse.set_visible(True)

    gray = Gray(size)

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ===== background ============================================================
        screen.blit(background.image, (0, background.top))
        background.scroll(0.5)
        screen.blit(gray.image, (0, 0))
        gray.darker()
        # ===== score =================================================================
        screen.blit(font.render(str(score), True, (0, 0, 0, 255)), (0, 0))
        # ===== end ===================================================================
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
