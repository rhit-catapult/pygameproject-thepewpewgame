import pygame
import sys
import time
import math


class Bullet:
    def __init__(self, screen, x, y, type, direction):
        self.screen = screen
        self.x = x
        self.y = y
        self.type = type
        self.direction = direction
        if type == 1:
            self.damage = 10  # amt. of health subtracted | higher = more damage
            self.speed = 8  # pixels moved per tick     | higher = faster
            self.usage = 2  # energy used per shot      | higher = more usage
            # special = none
            self.color = (255, 255, 0)
            self.bullet = pygame.draw.rect(self.screen, self.color, (self.x - 10, self.y - 3, 20, 6))

        elif type == 2:
            self.damage = 60
            self.speed = 3
            self.usage = 50
            # special = bomb
            self.color = (20, 20, 100)
            self.bullet = pygame.draw.circle(self.screen, self.color, (self.x, self.y), 30)

        elif type == 3:
            self.damage = 20
            self.speed = 12
            self.usage = 40
            # special = penetration (spawn 3 bullets inside eachother, 60 damage total)
            self.color = (255, 30, 30)
            self.bullet = pygame.draw.rect(self.screen, self.color, (self.x - 20, self.y - 2, 40, 4))


        elif type == 4:
            self.damage = 0
            self.speed = 5
            self.usage = 60
            # special = reflects bullets
            self.color = (50, 200, 255)
            self.bullet = pygame.draw.rect(self.screen, self.color, (self.x - 2, self.y - 25, 5, 50))
        else:
            return

    def move(self):
        self.x += self.speed*self.direction

        if self.type == 1:
            self.bullet = pygame.draw.rect(self.screen, self.color, (self.x - 10, self.y - 3, 20, 6))

        elif self.type == 2:
            self.bullet = pygame.draw.circle(self.screen, self.color, (self.x, self.y), 10)

        elif self.type == 3:
            self.bullet = pygame.draw.rect(self.screen, self.color, (self.x - 20, self.y - 2, 40, 4))

        elif self.type == 4:
            self.bullet = pygame.draw.rect(self.screen, self.color, (self.x - 2, self.y - 30, 5, 60))

        else:
            return

    def check_collide(self, other):
        if other.type == 1:
            return self.bullet.colliderect(other.x - 14, other.y - 3, 28, 6)
        elif other.type == 2:
            return self.bullet.colliderect(other.x - 12, other.y - 10, 23, 20)
        elif other.type == 3:
            return self.bullet.colliderect(other.x - 26, other.y - 2, 52, 4)
        elif other.type == 4:
            return self.bullet.colliderect(other.x - 5, other.y - 30, 10, 60)



class Gun:
    def __init__(self, screen, player):
        if player != 1:
            self.direction = -1
            self.x = 1450
        else:
            self.direction = 1
            self.x = 50

        self.y = 500
        self.type = 1
        self.wait_value = 0
        self.bullets = []
        self.screen = screen

    def updateType(self, newType):
        self.type = newType
        self.wait_value = 500

    def shoot(self, player_y):
        self.y = player_y

        if self.type == 1:
            self.reload = 20  # ticks per shot, 60 ticks per second
        elif self.type == 2:
            self.reload = 180
        elif self.type == 3:
            self.reload = 60
        elif self.type == 4:
            self.reload = 300
        else:
            return

        if self.wait_value>=self.reload:
            self.wait_value = 0
            if self.type == 3:
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))
            elif self.type == 4:
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))
            else:
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))

        else:
            self.wait_value += 1


    def update(self, otherGun):
        for bullet in self.bullets:
            bullet.move()
            for other in otherGun.bullets:
                if other != bullet and abs(bullet.y-other.y)<100 and abs(bullet.x-other.x)<100:
                    if bullet.check_collide(other):
                        self.bullets.remove(bullet)
                        otherGun.bullets.remove(other)
                        return
                    elif other.check_collide(bullet):
                        self.bullets.remove(bullet)
                        otherGun.bullets.remove(other)
                        return



def main():
    pygame.init()
    pygame.display.set_caption("playground")
    screen = pygame.display.set_mode((1500, 800))
    clock = pygame.time.Clock()

    gun1 = Gun(screen, 1)
    gun2 = Gun(screen, 2)
    btype2 = 1
    yvalue = 500
    message_text = "Normal"
    font = pygame.font.Font(None, 25)
    while True:
        clock.tick(60)
        screen.fill((5, 5, 5))
        pushed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if pushed_keys[pygame.K_RIGHT] and btype2 < 4:
                btype2 += 1
                if btype2 == 1:
                    gun1.updateType(1)
                    message_text = "Normal"
                elif btype2 == 2:
                    gun1.updateType(2)
                    message_text = "Bomb"
                elif btype2 == 3:
                    gun1.updateType(3)
                    message_text = "Penetrating"
                elif btype2 == 4:
                    gun1.updateType(4)
                    message_text = "Reflective"
            if pushed_keys[pygame.K_LEFT] and btype2 > 1:
                btype2 -= 1
                if btype2 == 1:
                    gun1.updateType(1)
                    message_text = "Normal"
                elif btype2 == 2:
                    gun1.updateType(2)
                    message_text = "Bomb"
                elif btype2 == 3:
                    gun1.updateType(3)
                    message_text = "Penetrating"
                elif btype2 == 4:
                    gun1.updateType(4)
                    message_text = "Reflective"

        if pushed_keys[pygame.K_UP]:
            yvalue -= 3
        if pushed_keys[pygame.K_DOWN]:
            yvalue += 3
        if pushed_keys[pygame.K_SPACE]:
            click = 1
        else:
            click = 0

        pygame.draw.rect(screen, (255, 255, 255), (25, yvalue - 25, 50, 50))

        if click >=1:
            gun1.shoot(yvalue)
            gun2.shoot(500)

        gun1.update(gun2)
        gun2.update(gun1)
        text = font.render(message_text, True, (122, 237, 201))
        screen.blit(text, (30,30))







        pygame.display.update()


main()
