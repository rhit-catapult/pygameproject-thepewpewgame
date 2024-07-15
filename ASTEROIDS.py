import pygame
import sys
import random
from pygame.locals import *

pygame.init()

screen_width = 1500
screen_height = 1000

black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Staggered Asteroids")

num_asteroids = 20
asteroid_width = 50
asteroid_height = 50
space_between_asteroids = 30

class Asteroid:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, surface):
        pygame.draw.rect(surface, white, (self.x, self.y, self.width, self.height))

asteroids = []
current_y = 0

for i in range(num_asteroids):
    x = random.randint(screen_width // 2 - 200, screen_width // 2 + 200 - asteroid_width)
    asteroids.append(Asteroid(x, current_y, asteroid_width, asteroid_height))
    current_y += asteroid_height + space_between_asteroids

def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(black)

        for asteroid in asteroids:
            asteroid.draw(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
