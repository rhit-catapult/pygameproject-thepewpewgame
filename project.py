import pygame
import sys
import random

pygame.init()

explosion = pygame.mixer.Sound("explosion.wav")
end_explosion = pygame.mixer.Sound("explosion_big.wav")
hit = pygame.mixer.Sound("hit.wav")
laser1 = pygame.mixer.Sound("laser1.wav")
laser2 = pygame.mixer.Sound("laser2.wav")
laser3 = pygame.mixer.Sound("laser3.wav")
laser4 = pygame.mixer.Sound("laser4.wav")


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
        self.boom_factor = 0
        self.collider = pygame.draw.rect(self.screen, (0, 0, 0), (self.x-12,self.y-20, 25, 40))

    def check_collision(self, gun):
        for other in gun.bullets:
            if other.type == 1:
                if self.collider.colliderect(other.x - 14, other.y - 3, 28, 6):
                    self.health -= other.damage
                    hit.play()
                    gun.bullets.remove(other)
                    return True
            elif other.type == 2:
                if self.collider.colliderect(other.x - 12, other.y - 10, 23, 20):
                    self.health -= other.damage
                    hit.play()
                    for i in range(10):
                        gun.bullets.append(Bullet(gun.screen, other.x, other.y, 9, gun.direction))
                    gun.bullets.remove(other)
                    return True
            elif other.type == 3:
                if self.collider.colliderect(other.x - 26, other.y - 2, 52, 4):
                    self.health -= other.damage
                    hit.play()
                    gun.bullets.remove(other)
                    return True
            elif other.type == 4:
                if self.collider.colliderect(other.x - 5, other.y - 30, 10, 60):
                    gun.bullets.remove(other)
                    hit.play()
                    return True
            elif other.type == 9:
                if abs(self.x - other.x)**2 <= (50*other.explosion_factor) ** 2 and abs(
                        self.y - other.y)**2 <= (50*other.explosion_factor) ** 2:
                    self.health -= other.damage
                    hit.play()
                    return True
            return False



    def update(self, y, gun):
        self.y = y
        self.collider = pygame.draw.rect(self.screen, (0, 0, 0), (self.x - 12, self.y - 20, 25, 40))
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
        self.check_collision(gun)
        if self.health<=0 or self.boom_factor != 0:
            self.boom()


    def boom(self):
        self.boom_factor += 1
        if self.boom_factor < 255:
            self.boom_color = (255-self.boom_factor, (255-self.boom_factor)/2, 0)
            pygame.draw.circle(self.screen, self.boom_color, (self.x, self.y), self.boom_factor)
        if self.colorA > (0, 0, 0):
            self.colorA = (self.colorA[0]/2, self.colorA[1]/2, self.colorA[2]/2)
        if self.colorB > (0, 0, 0):
            self.colorB = (self.colorB[0]/2, self.colorB[1]/2, self.colorB[2]/2)

    def exploded(self):
        if self.boom_factor == 0:
            return False
        else:
            return True


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
            self.speed = 8  # pixels moved per tick       | higher = faster
            self.usage = 10  # energy used per shot        | higher = more usage
            # special = none
            self.color = (255, 255, 0)
            self.bullet = pygame.draw.rect(self.screen, self.color, (self.x - 10, self.y - 3, 20, 6))
            laser1.play()

        elif type == 2:
            self.damage = 1
            self.speed = 6
            self.usage = 50
            # special = bomb
            self.color = (50, 50, 200)
            self.bullet = pygame.draw.circle(self.screen, self.color, (self.x, self.y), 30)
            laser2.play()

        elif type == 3:
            self.damage = 15
            self.speed = 15
            self.usage = 40
            # special = penetration (spawn 3 bullets inside eachother, 60 damage total)
            self.color = (255, 30, 30)
            self.bullet = pygame.draw.rect(self.screen, self.color, (self.x - 20, self.y - 2, 40, 4))
            laser3.play()


        elif type == 4:
            self.damage = 0
            self.speed = 5
            self.usage = 60
            # special = reflects bullets
            self.color = (50, 200, 255)
            self.bullet = pygame.draw.rect(self.screen, self.color, (self.x - 2, self.y - 25, 5, 50))
            laser4.play()

        elif type == 9:
            self.damage = 2
            self.speed = 0
            self.usage = 0
            self.color = (255, 150, 0)
            self.explosion_factor = 1
            self.bullet = pygame.draw.circle(self.screen, self.color, (self.x, self.y), 50)
            explosion.play()
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
            return self.bullet.colliderect(other.x - 38, other.y - 2, 64, 4)
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
            usage = 5
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
            if bullet.x>self.screen.get_width() or bullet.x<0:
                if self.bullets.__contains__(bullet):
                    self.bullets.remove(bullet)

            for other in otherGun.bullets:
                if abs(bullet.y-other.y)<100 and abs(bullet.x-other.x)<100:
                    if bullet.check_collide(other):
                        if other.type == 9:
                            if self.bullets.__contains__(bullet) and bullet.type != 9:
                                self.bullets.remove(bullet)

                        if bullet.type == 4:
                            self.bullets.append(Bullet(self.screen, other.x, other.y, other.type, self.direction))
                            if self.bullets.__contains__(bullet):
                                self.bullets.remove(bullet)
                            otherGun.bullets.remove(other)
                            hit.play()
                        elif other.type == 4:
                            return

                        elif bullet.type == 2:
                            for i in range(10):
                                otherGun.bullets.append(Bullet(otherGun.screen, other.x, other.y, 9, otherGun.direction))
                            if self.bullets.__contains__(bullet):
                                self.bullets.remove(bullet)
                            otherGun.bullets.remove(other)
                            hit.play()
                        elif other.type == 2:
                            return
                        else:
                            if self.bullets.__contains__(bullet):
                                self.bullets.remove(bullet)
                                otherGun.bullets.remove(other)
                                hit.play()

    def usage(self):
        if self.type == 1:
            return 5
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
class AsteroidPiece:
    def __init__(self, x, y, width, height, gun1, gun2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bullets = []
        self.health = 25
        self.destroyed = False
        self.color = (255, 255, 255)
        self.gun1 = gun1
        self.gun2 = gun2
        self.collider = pygame.rect.Rect(self.x, self.y, self.width, self.height)
    def return_destroyed(self):
        return self.destroyed

    def draw(self, surface):
        if self.health <= 0:
            self.health = 0
            self.destroyed = True
            self.surface = surface
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
            for bullet1 in self.gun1.bullets:
                self.check_collisions(self.gun1, bullet1)
            for bullet2 in self.gun2.bullets:
                self.check_collisions(self.gun2, bullet2)

            self.color = (self.health*10, self.health*10, self.health*10)
            self.destroyed = False

    def check_collisions(self, gun, other):
        if other.type == 1:
            if self.collider.colliderect(other.x - 14, other.y - 3, 28, 6):
                self.health -= other.damage
                if self.health > 0:
                    gun.bullets.remove(other)
                hit.play()
                return True
        elif other.type == 2:
            if self.collider.colliderect(other.x - 5, other.y - 5, 10, 10) and abs(self.x-other.x)<100 and abs(self.y-other.y)<100:
                self.health -= other.damage
                if self.health > 0:
                    for i in range(10):
                        gun.bullets.append(Bullet(gun.screen, other.x, other.y, 9, gun.direction))
                    gun.bullets.remove(other)
                hit.play()
                return True
        elif other.type == 3:
            if self.collider.colliderect(other.x - 12, other.y - 2, 24, 4):
                self.health -= other.damage
                if self.health > 5:
                    gun.bullets.remove(other)
                else:
                    self.health += other.damage/1.07
                hit.play()
                return True
        elif other.type == 4:
            if self.collider.colliderect(other.x - 5, other.y - 30, 10, 60):
                self.health -= other.damage
                if self.health > 0:
                    gun.bullets.remove(other)
                hit.play()
                return True
        elif other.type == 9:
            if abs(self.x - other.x)**2 <= (50*other.explosion_factor) ** 2 and abs(
                    self.y - other.y)**2 <= (50*other.explosion_factor) ** 2:
                self.health -= other.damage
                hit.play()
                return True
        return False
def game():
    pygame.init()
    pygame.display.set_caption("Star Wars")
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

    asteroid = []
    asteroids = []
    current_y = 100
    asteroid_height = 80
    asteroid_width = 80
    num_asteroids = 6
    space_between_asteroids = 15


    for i in range(num_asteroids):
        x = random.randint(int(screen.get_width()/2 - 500), int(screen.get_width()/2 - asteroid_width))
        # if random.randint(0,1) == 1:
        #    asteroids.append(AsteroidPiece(x-(asteroid_width/2.5)-6, current_y-(asteroid_height/2.5)-6, asteroid_width / 5, asteroid_height / 5))
        if random.randint(0, 1) == 1:
            asteroids.append(
                AsteroidPiece(x - (asteroid_width / 5) - 3, current_y - (asteroid_height / 2.5) - 6, asteroid_width / 5,
                              asteroid_height / 5, gun1, gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(
                AsteroidPiece(x, current_y - (asteroid_height / 2.5) - 6, asteroid_width / 5, asteroid_height / 5, gun1,
                              gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(
                AsteroidPiece(x + (asteroid_width / 5) + 3, current_y - (asteroid_height / 2.5) - 6, asteroid_width / 5,
                              asteroid_height / 5, gun1, gun2))
        # if random.randint(0, 1) == 1:
        #    asteroids.append(AsteroidPiece(x+(asteroid_width/2.5)+6, current_y-(asteroid_height/2.5)-6, asteroid_width / 5, asteroid_height / 5))

        if random.randint(0, 1) == 1:
            asteroids.append(
                AsteroidPiece(x - (asteroid_width / 2.5) - 6, current_y - (asteroid_height / 5) - 3, asteroid_width / 5,
                              asteroid_height / 5, gun1, gun2))
        asteroids.append(
            AsteroidPiece(x - (asteroid_width / 5) - 3, current_y - (asteroid_height / 5) - 3, asteroid_width / 5,
                          asteroid_height / 5, gun1, gun2))
        asteroids.append(
            AsteroidPiece(x, current_y - (asteroid_height / 5) - 3, asteroid_width / 5, asteroid_height / 5, gun1,
                          gun2))
        asteroids.append(
            AsteroidPiece(x + (asteroid_width / 5) + 3, current_y - (asteroid_height / 5) - 3, asteroid_width / 5,
                          asteroid_height / 5, gun1, gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(
                AsteroidPiece(x + (asteroid_width / 2.5) + 6, current_y - (asteroid_height / 5) - 3, asteroid_width / 5,
                              asteroid_height / 5, gun1, gun2))

        if random.randint(0, 1) == 1:
            asteroids.append(
                AsteroidPiece(x - (asteroid_width / 2.5) - 6, current_y, asteroid_width / 5, asteroid_height / 5, gun1,
                              gun2))
        asteroids.append(
            AsteroidPiece(x - (asteroid_width / 5) - 3, current_y, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        asteroids.append(AsteroidPiece(x, current_y, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        asteroids.append(
            AsteroidPiece(x + (asteroid_width / 5) + 3, current_y, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(
                AsteroidPiece(x + (asteroid_width / 2.5) + 6, current_y, asteroid_width / 5, asteroid_height / 5, gun1,
                              gun2))

        if random.randint(0, 1) == 1:
            asteroids.append(
                AsteroidPiece(x - (asteroid_width / 2.5) - 6, current_y + (asteroid_height / 5) + 3, asteroid_width / 5,
                              asteroid_height / 5, gun1, gun2))
        asteroids.append(
            AsteroidPiece(x - (asteroid_width / 5) - 3, current_y + (asteroid_height / 5) + 3, asteroid_width / 5,
                          asteroid_height / 5, gun1, gun2))
        asteroids.append(
            AsteroidPiece(x, current_y + (asteroid_height / 5) + 3, asteroid_width / 5, asteroid_height / 5, gun1,
                          gun2))
        asteroids.append(
            AsteroidPiece(x + (asteroid_width / 5) + 3, current_y + (asteroid_height / 5) + 3, asteroid_width / 5,
                          asteroid_height / 5, gun1, gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(
                AsteroidPiece(x + (asteroid_width / 2.5) + 6, current_y + (asteroid_height / 5) + 3, asteroid_width / 5,
                              asteroid_height / 5, gun1, gun2))

        # if random.randint(0, 1) == 1:
        #    asteroids.append(AsteroidPiece(x - (asteroid_width / 2.5) - 6, current_y+(asteroid_height/2.5)+6, asteroid_width / 5, asteroid_height / 5))
        if random.randint(0, 1) == 1:
            asteroids.append(
                AsteroidPiece(x - (asteroid_width / 5) - 3, current_y + (asteroid_height / 2.5) + 6, asteroid_width / 5,
                              asteroid_height / 5, gun1, gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(
                AsteroidPiece(x, current_y + (asteroid_height / 2.5) + 6, asteroid_width / 5, asteroid_height / 5, gun1,
                              gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(
                AsteroidPiece(x + (asteroid_width / 5) + 3, current_y + (asteroid_height / 2.5) + 6, asteroid_width / 5,
                              asteroid_height / 5, gun1, gun2))
        # if random.randint(0, 1) == 1:
        #    asteroids.append(AsteroidPiece(x + (asteroid_width / 2.5) + 6, current_y+(asteroid_height/2.5)+6, asteroid_width / 5, asteroid_height / 5))


        current_y += asteroid_height + space_between_asteroids
    current_y = 110

    for i in range(num_asteroids):
        x = random.randint(int(screen.get_width()/2 + asteroid_width), int(screen.get_width()/2 + 500))
        #if random.randint(0,1) == 1:
        #    asteroids.append(AsteroidPiece(x-(asteroid_width/2.5)-6, current_y-(asteroid_height/2.5)-6, asteroid_width / 5, asteroid_height / 5))
        if random.randint(0, 1) == 1:
            asteroids.append(AsteroidPiece(x-(asteroid_width/5)-3, current_y-(asteroid_height/2.5)-6, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(AsteroidPiece(x, current_y-(asteroid_height/2.5)-6, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(AsteroidPiece(x+(asteroid_width/5)+3, current_y-(asteroid_height/2.5)-6, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        #if random.randint(0, 1) == 1:
        #    asteroids.append(AsteroidPiece(x+(asteroid_width/2.5)+6, current_y-(asteroid_height/2.5)-6, asteroid_width / 5, asteroid_height / 5))

        if random.randint(0, 1) == 1:
            asteroids.append(AsteroidPiece(x - (asteroid_width / 2.5) - 6, current_y-(asteroid_height/5)-3, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        asteroids.append(AsteroidPiece(x - (asteroid_width / 5) - 3, current_y-(asteroid_height/5)-3, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        asteroids.append(AsteroidPiece(x, current_y-(asteroid_height/5)-3, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        asteroids.append(AsteroidPiece(x + (asteroid_width / 5) + 3, current_y-(asteroid_height/5)-3, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(AsteroidPiece(x + (asteroid_width / 2.5) + 6, current_y-(asteroid_height/5)-3, asteroid_width / 5, asteroid_height / 5, gun1, gun2))

        if random.randint(0, 1) == 1:
            asteroids.append(AsteroidPiece(x - (asteroid_width / 2.5) - 6, current_y, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        asteroids.append(AsteroidPiece(x - (asteroid_width / 5) - 3, current_y, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        asteroids.append(AsteroidPiece(x, current_y, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        asteroids.append(AsteroidPiece(x + (asteroid_width / 5) + 3, current_y, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(AsteroidPiece(x + (asteroid_width / 2.5) + 6, current_y, asteroid_width / 5, asteroid_height / 5, gun1, gun2))

        if random.randint(0, 1) == 1:
            asteroids.append(AsteroidPiece(x - (asteroid_width / 2.5) - 6, current_y+(asteroid_height/5)+3, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        asteroids.append(AsteroidPiece(x - (asteroid_width / 5) - 3, current_y+(asteroid_height/5)+3, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        asteroids.append(AsteroidPiece(x, current_y+(asteroid_height/5)+3, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        asteroids.append(AsteroidPiece(x + (asteroid_width / 5) + 3, current_y+(asteroid_height/5)+3, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(AsteroidPiece(x + (asteroid_width / 2.5) + 6, current_y+(asteroid_height/5)+3, asteroid_width / 5, asteroid_height / 5, gun1, gun2))

        #if random.randint(0, 1) == 1:
        #    asteroids.append(AsteroidPiece(x - (asteroid_width / 2.5) - 6, current_y+(asteroid_height/2.5)+6, asteroid_width / 5, asteroid_height / 5))
        if random.randint(0, 1) == 1:
            asteroids.append(AsteroidPiece(x - (asteroid_width / 5) - 3, current_y+(asteroid_height/2.5)+6, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(AsteroidPiece(x, current_y+(asteroid_height/2.5)+6, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        if random.randint(0, 1) == 1:
            asteroids.append(AsteroidPiece(x + (asteroid_width / 5) + 3, current_y+(asteroid_height/2.5)+6, asteroid_width / 5, asteroid_height / 5, gun1, gun2))
        #if random.randint(0, 1) == 1:
        #    asteroids.append(AsteroidPiece(x + (asteroid_width / 2.5) + 6, current_y+(asteroid_height/2.5)+6, asteroid_width / 5, asteroid_height / 5))

        current_y += asteroid_height + space_between_asteroids

    health_smooth1 = 500
    health_smooth2 = 500
    speed_mul1 = 1
    speed_mul2 = 1



    while True:
        clock.tick(60)
        screen.fill((0, 0, 0))
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

        player1.update(yvalue1, gun2)
        player2.update(yvalue2, gun1)

        for asteroid in asteroids:
            asteroid.draw(screen)



        if player1.exploded() or player2.exploded():
            message_text1 = "Good Game"
            message_text2 = "Good Game"
            p += 1
            if p <= 180:
                end_explosion.play()

            if player1.boom_factor > 320 or player2.boom_factor > 320:
                return False
        else:
            p = 0
            gun1.update(gun2)
            gun2.update(gun1)
            if pushed_keys[pygame.K_w] and yvalue1 > 80:
                yvalue1 -= speed_mul1
            if pushed_keys[pygame.K_s] and yvalue1 < 670:
                yvalue1 += speed_mul1
            if pushed_keys[pygame.K_LSHIFT]:
                click1 = 1
            else:
                click1 = 0

            if pushed_keys[pygame.K_UP] and yvalue2 > 80:
                yvalue2 -= speed_mul2
            if pushed_keys[pygame.K_DOWN] and yvalue2 < 670:
                yvalue2 += speed_mul2
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

        text = font.render(message_text1, True, (122, 237, 176))
        screen.blit(text, (30,30))
        text = font.render(message_text2, True, (237, 122, 201))
        screen.blit(text, (screen.get_width()-text.get_width()-30,30))

        if energy1 < gun1.usage():
            barColor1 = (255, 10, 10)
            speed_mul1 = 1
        else:
            barColor1 = (255, 255, 255)
            speed_mul1 = 3

        if energy2 < gun2.usage():
            barColor2 = (255, 10, 10)
            speed_mul2 = 1
        else:
            barColor2 = (255, 255, 255)
            speed_mul2 = 3

        pygame.draw.rect(screen,(80, 80, 80), (0,700,1500,100))

        health_smooth1 += (player1.health*5 - health_smooth1)/10
        health_smooth2 += (player2.health*5 - health_smooth2)/10

        pygame.draw.rect(screen, (50, 50, 50), (30, 750, 500, 30))
        pygame.draw.rect(screen, (50, 20, 20), (30, 710, 500, 30))
        pygame.draw.rect(screen, (255, 20, 20), (30, 710, health_smooth1, 30))
        pygame.draw.rect(screen, (20, 255, 20), (30, 710, 5*player1.health, 30))
        pygame.draw.rect(screen, barColor1, (30, 760, energy1 * 5, 20))
        pygame.draw.rect(screen, (100, 100, 100), (28+(gun1.usage()*5), 760, 4, 20))

        pygame.draw.rect(screen, (200, 200, 200), (30, 750, gun1.reload_time() * 500, 5))

        pygame.draw.rect(screen, (50, 50, 50), (970, 750, 500, 30))
        pygame.draw.rect(screen, (50, 20, 20), (970, 710, 500, 30))
        pygame.draw.rect(screen, (255, 20, 20), (970, 710, health_smooth2, 30))
        pygame.draw.rect(screen, (20, 255, 20), (970, 710, 5*player2.health, 30))
        pygame.draw.rect(screen, barColor2, (970, 760, energy2 * 5, 20))
        pygame.draw.rect(screen, (100, 100, 100), (968 + (gun2.usage() * 5), 760, 4, 20))

        pygame.draw.rect(screen, (200, 200, 200), (970, 750, gun2.reload_time() * 500, 5))

        pygame.display.update()


# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1500
screen_height = 800

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Star Wars")

# Fonts
large_font = pygame.font.Font(None, 200)
button_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

# Text
title_text = large_font.render("Star Wars", True, white)
start_text = button_font.render("Start", True, black)
rules_text = button_font.render("Rules", True, black)
exit_text = button_font.render("Exit", True, black)

# Button dimensions
button_width = 200
button_height = 100

# Buttons
start_button_rect = pygame.Rect((screen_width // 2 - button_width // 2, screen_height // 2 - 75),
                                (button_width, button_height))
rules_button_rect = pygame.Rect((screen_width // 2 - button_width // 2, screen_height // 2 + 75),
                                (button_width, button_height))
exit_button_rect = pygame.Rect(screen_width - button_width // 2 - 30, 30, button_width/2, button_height/2)











# Rules Screen Text

rules_content = [
    "Your objective: Destroy the enemy ship before they destroy you.",
    "",
    "    You will be in a 1 vs. 1 against someone in a ship.",
    "    Your ship's display shows its health, energy, and the reload timer. (green, white, and gray respectively.)",
    "    ",
    "    ",
    "    You will have 4 types of bullets, each with different strengths and weaknesses:",
    "           |",
    "           | - Normal bullets - Relatively high fire rate and speed, with lower damage and cost.",
    "           |",
    "           | - Bombs - Low speed, long reload, and high cost, but makes up for it with massive splash damage.",
    "           |",
    "           | - Sharpshots - High speed, damage, cost, and reload time, with penetrating abilities to boot.",
    "           |",
    "           | - Reflectors - Does no damage and shatters easily, but can reflect up to 10 enemy bullets back at them.",
    "           |_________________________________________",
    "                     Player 1 controls:  |  Player 2 controls:",
    "    Move Up and Down -    W / S  |  ^ / v arrow keys",
    "    Change ammo type -    A / D  |  < / > arrow keys",
    "    Shoot                        -   LShift | RShift"

]








def draw_text_list(screen, text_list, font, color, x, y, line_spacing=10):
    for line in text_list:
        text = font.render(line, True, color)
        screen.blit(text, (x, y))
        y += text.get_height() + line_spacing


def main():
    running = False
    show_rules = False
    start_game = False
    l = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    start_game = True
                elif rules_button_rect.collidepoint(event.pos):
                    show_rules = True
                elif exit_button_rect.collidepoint(event.pos):
                    show_rules = False
        screen.fill(black)

        if show_rules:
            draw_text_list(screen, rules_content, small_font, white, 50, 50)
            pygame.draw.rect(screen, (255, 255, 0), (60, 340, 20, 6))
            pygame.draw.circle(screen, (50, 50, 255), (70, 414), 10)
            pygame.draw.circle(screen, (50, 25, 0), (70, 414), 50, 5)
            pygame.draw.rect(screen, (35, 0, 0), (30, 482, 40, 2))
            pygame.draw.rect(screen, (50, 0, 0), (40, 481, 40, 4))
            pygame.draw.rect(screen, (250, 0, 0), (50, 481, 40, 4))
            pygame.draw.rect(screen, (50, 255, 255), (67, 525, 5, 60))
            pygame.draw.rect(screen, green, exit_button_rect)
            screen.blit(exit_text, (screen_width - button_width // 2 - 18, 40))
            start_game = False

        elif start_game:
            if l == 0:
                screen.fill(black)
                l = 1
                running = True
            else:
                while running:
                    running = game()
                else:
                    running = False
                    screen.fill(black)
                    start_game = False
                    l = 0
        else:
            # Draw the title text
            screen.blit(title_text,
                        (screen_width // 2 - title_text.get_width() // 2, screen_height // 4 - title_text.get_height()//2))

            # Draw the start button
            pygame.draw.rect(screen, green, start_button_rect)
            screen.blit(start_text, (start_button_rect.x + (button_width - start_text.get_width()) // 2,
                                     start_button_rect.y + (button_height - start_text.get_height()) // 2))

            # Draw the rules button
            pygame.draw.rect(screen, green, rules_button_rect)
            screen.blit(rules_text, (rules_button_rect.x + (button_width - rules_text.get_width()) // 2,
                                     rules_button_rect.y + (button_height - rules_text.get_height()) // 2))

        pygame.display.flip()
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    main()













































































































