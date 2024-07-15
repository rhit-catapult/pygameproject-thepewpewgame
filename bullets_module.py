import pygame
import sys
import time
import math

class Ship:
    def __init__(self, screen, player, health):
        self.screen = screen
        self.player = player
        self.health = health
        if player == 1:
            self.x = 50
            self.colorB = (0, 255, 0)
            self.colorA = (0, 155, 0)
        else:
            self.x = screen.get_width()-50
            self.colorB = (255, 0, 255)
            self.colorA = (155, 0, 155)

        self.y = screen.get_height()/2

    def draw(self, y):
        self.y = y
        if self.player == 1:
            pygame.draw.polygon(self.screen, self.colorA, (
            (self.x - 14, self.y - 10), (self.x - 8, self.y - 4), (self.x - 8, self.y + 4), (self.x - 14, self.y + 10)))

            pygame.draw.polygon(self.screen, self.colorB, ((
            (self.x - 8, self.y - 20), (self.x - 2, self.y - 20), (self.x + 6, self.y - 4), (self.x + 15, self.y - 4),
            (self.x + 15, self.y + 4), (self.x + 6, self.y + 4), (self.x - 2, self.y + 20), (self.x - 8, self.y + 20))))

        else:
            pygame.draw.polygon(self.screen, self.colorA, (
                (self.x + 14, self.y - 10), (self.x + 8, self.y - 4), (self.x + 8, self.y + 4),
                (self.x + 14, self.y + 10)))

            pygame.draw.polygon(self.screen, self.colorB, ((
                (self.x + 8, self.y - 20), (self.x + 2, self.y - 20), (self.x - 6, self.y - 4),
                (self.x - 15, self.y - 4),
                (self.x - 15, self.y + 4), (self.x - 6, self.y + 4), (self.x + 2, self.y + 20),
                (self.x + 8, self.y + 20))))


class Bullet:
    def __init__(self, screen, x, y, type, direction):
        self.screen = screen
        self.x = x
        self.y = y
        self.type = type
        self.direction = direction
        self.explosion_factor = 1

        if type == 1:
            self.damage = 10  # amt. of health subtracted | higher = more damage
            self.speed = 6  # pixels moved per tick       | higher = faster
            self.usage = 10  # energy used per shot        | higher = more usage
            # special = none
            self.color = (255, 255, 0)
            self.bullet = pygame.draw.rect(self.screen, self.color, (self.x - 10, self.y - 3, 20, 6))

        elif type == 2:
            self.damage = 5
            self.speed = 3
            self.usage = 50
            # special = bomb
            self.color = (50, 50, 200)
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

        elif type == 9:
            self.damage = 3
            self.speed = 0
            self.usage = 0
            self.color = (255, 150, 0)
            self.explosion_factor = 1
            self.bullet = pygame.draw.circle(self.screen, self.color, (self.x, self.y), 50)
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

        elif self.type == 9:
            self.bullet = pygame.draw.circle(self.screen, (255*self.explosion_factor, 150*self.explosion_factor, 0), (self.x, self.y), 55*self.explosion_factor)
            self.explosion_factor -= 0.05
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
        elif other.type == 9:
            return self.bullet.colliderect(other.x-other.explosion_factor, other.y-other.explosion_factor, other.explosion_factor*2, other.explosion_factor*2)
        else:
            return False
class Gun:
    def __init__(self, screen, player):
        if player != 1:
            self.direction = -1
            self.x = 1450
        else:
            self.direction = 1
            self.x = 50


        self.type = 1
        self.reload = 0
        self.wait_value = 0
        self.bullets = []
        self.screen = screen

    def updateType(self, newType):
        self.type = newType
        self.wait_value = 500

    def shoot(self, player_y, energy):

        self.y = player_y

        if self.type == 1:
            self.reload = 20  # ticks per shot, 60 ticks per second
            usage = 10
        elif self.type == 2:
            self.reload = 180
            usage = 50
        elif self.type == 3:
            self.reload = 60
            usage = 40
        elif self.type == 4:
            self.reload = 300
            usage = 60
        else:
            return 0



        if self.wait_value>=self.reload and energy>usage:
            self.wait_value = 0
            if self.type == 3:
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))

            elif self.type == 4:
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))
                self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))

            self.bullets.append(Bullet(self.screen, self.x, self.y, self.type, self.direction))
        else:
            return 0
        return usage

    def update(self, otherGun):
        if self.wait_value <= 500:
            self.wait_value += 1

        for bullet in self.bullets:
            if bullet.type == 9 and bullet.explosion_factor <= 0:
                self.bullets.remove(bullet)
            bullet.move()
            if bullet.x>self.screen.get_width() or bullet.x<0 and self.bullets.__contains__(bullet):
                self.bullets.remove(bullet)

            for other in otherGun.bullets:
                if abs(bullet.y-other.y)<100 and abs(bullet.x-other.x)<100:
                    if bullet.check_collide(other):
                        if other.type == 9:
                            if self.bullets.__contains__(bullet):
                                self.bullets.remove(bullet)

                        if bullet.type == 4:
                            self.bullets.append(Bullet(self.screen, other.x, other.y, other.type, self.direction))
                            if self.bullets.__contains__(bullet):
                                self.bullets.remove(bullet)
                            otherGun.bullets.remove(other)
                        elif other.type == 4:
                            return

                        elif bullet.type == 2:
                            self.bullets.append(Bullet(self.screen, bullet.x, bullet.y, 9, self.direction))
                            self.bullets.append(Bullet(self.screen, bullet.x, bullet.y, 9, self.direction))
                            self.bullets.append(Bullet(self.screen, bullet.x, bullet.y, 9, self.direction))
                            self.bullets.append(Bullet(self.screen, bullet.x, bullet.y, 9, self.direction))
                            self.bullets.append(Bullet(self.screen, bullet.x, bullet.y, 9, self.direction))
                            self.bullets.append(Bullet(self.screen, bullet.x, bullet.y, 9, self.direction))
                            if self.bullets.__contains__(bullet):
                                self.bullets.remove(bullet)
                            otherGun.bullets.remove(other)
                        elif other.type == 2:
                            return
                        else:
                            if self.bullets.__contains__(bullet):
                                self.bullets.remove(bullet)
                                otherGun.bullets.remove(other)

    def usage(self):
        if self.type == 1:
            return 10
        elif self.type == 2:
            return 50
        elif self.type == 3:
            return 40
        elif self.type == 4:
            return 60
        else:
            return 0

    def reload_time(self):
        if self.wait_value < self.reload:
            return self.wait_value/self.reload
        else:
            return 1


def main():
    pygame.init()
    pygame.display.set_caption("playground")
    screen = pygame.display.set_mode((1500, 800))
    clock = pygame.time.Clock()

    player1 = Ship(screen, 1, 100)
    player2 = Ship(screen, 2, 100)

    gun1 = Gun(screen, 1)
    gun2 = Gun(screen, 2)
    btype = 1
    btype2 = 1
    yvalue1 = 400
    yvalue2 = 400
    message_text1 = "Normal"
    message_text2 = "Normal"
    font = pygame.font.Font(None, 25)

    energy1 = 100
    energy2 = 100



    while True:
        clock.tick(60)
        screen.fill((0,0,0))
        pushed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if pushed_keys[pygame.K_d] and btype < 4:
                btype += 1
                if btype == 1:
                    gun1.updateType(1)
                    message_text1 = "Normal"
                elif btype == 2:
                    gun1.updateType(2)
                    message_text1 = "Bomb"
                elif btype == 3:
                    gun1.updateType(3)
                    message_text1 = "Penetrating"
                elif btype == 4:
                    gun1.updateType(4)
                    message_text1 = "Reflective"
            if pushed_keys[pygame.K_a] and btype > 1:
                btype -= 1
                if btype == 1:
                    gun1.updateType(1)
                    message_text1 = "Normal"
                elif btype == 2:
                    gun1.updateType(2)
                    message_text1 = "Bomb"
                elif btype == 3:
                    gun1.updateType(3)
                    message_text1 = "Penetrating"
                elif btype == 4:
                    gun1.updateType(4)
                    message_text1 = "Reflective"

            if pushed_keys[pygame.K_RIGHT] and btype2 < 4:
                btype2 += 1
                if btype2 == 1:
                    gun2.updateType(1)
                    message_text2 = "Normal"
                elif btype2 == 2:
                    gun2.updateType(2)
                    message_text2 = "Bomb"
                elif btype2 == 3:
                    gun2.updateType(3)
                    message_text2 = "Penetrating"
                elif btype2 == 4:
                    gun2.updateType(4)
                    message_text2 = "Reflective"
            if pushed_keys[pygame.K_LEFT] and btype2 > 1:
                btype2 -= 1
                if btype2 == 1:
                    gun2.updateType(1)
                    message_text2 = "Normal"
                elif btype2 == 2:
                    gun2.updateType(2)
                    message_text2 = "Bomb"
                elif btype2 == 3:
                    gun2.updateType(3)
                    message_text2 = "Penetrating"
                elif btype2 == 4:
                    gun2.updateType(4)
                    message_text2 = "Reflective"

        if pushed_keys[pygame.K_w]:
            yvalue1 -= 3
        if pushed_keys[pygame.K_s]:
            yvalue1 += 3
        if pushed_keys[pygame.K_LSHIFT]:
            click1 = 1
        else:
            click1 = 0

        if pushed_keys[pygame.K_UP]:
            yvalue2 -= 3
        if pushed_keys[pygame.K_DOWN]:
            yvalue2 += 3
        if pushed_keys[pygame.K_RSHIFT]:
            click2 = 1
        else:
            click2 = 0

        if energy1 < 100:
            energy1 += 0.2
        if click1 >= 1:
            energy1 -= gun1.shoot(yvalue1, energy1)
        if energy1 < 0:
            energy1 = 0

        if energy2 < 100:
            energy2 += 0.2
        if click2 >= 1:
            energy2 -= gun2.shoot(yvalue2, energy2)
        if energy2 < 0:
            energy2 = 0

        gun1.update(gun2)
        gun2.update(gun1)
        player1.draw(yvalue1)
        player2.draw(yvalue2)
        text = font.render(message_text1, True, (122, 237, 176))
        screen.blit(text, (30,30))
        text = font.render(message_text2, True, (237, 122, 201))
        screen.blit(text, (screen.get_width()-text.get_width()-30,30))

        if energy1 < gun1.usage():
            barColor1 = (255, 10, 10)
        else:
            barColor1 = (255, 255, 255)

        if energy2 < gun2.usage():
            barColor2 = (255, 10, 10)
        else:
            barColor2 = (255, 255, 255)

        pygame.draw.rect(screen, (50, 50, 50), (30, 750, 500, 30))
        pygame.draw.rect(screen, barColor1, (30, 760, energy1 * 5, 20))
        pygame.draw.rect(screen, (100, 100, 100), (28+(gun1.usage()*5), 760, 4, 20))

        pygame.draw.rect(screen, (200, 200, 200), (30, 750, gun1.reload_time() * 500, 5))

        pygame.draw.rect(screen, (50, 50, 50), (970, 750, 500, 30))
        pygame.draw.rect(screen, barColor2, (970, 760, energy2 * 5, 20))
        pygame.draw.rect(screen, (100, 100, 100), (968 + (gun2.usage() * 5), 760, 4, 20))

        pygame.draw.rect(screen, (200, 200, 200), (970, 750, gun2.reload_time() * 500, 5))

        pygame.display.update()

main()
