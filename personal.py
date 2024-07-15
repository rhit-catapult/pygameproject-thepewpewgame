import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1000
screen_height = 1800

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pew Pew Game")

# Fonts
large_font = pygame.font.Font(None, 100)
button_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

# Text
title_text = large_font.render("Pew Pew Game", True, white)
start_text = button_font.render("Start", True, black)
rules_text = button_font.render("Rules", True, black)

# Button dimensions
button_width = 200
button_height = 100

# Buttons
start_button_rect = pygame.Rect((screen_width // 2 - button_width // 2, screen_height // 2 + 50),
                                (button_width, button_height))
rules_button_rect = pygame.Rect((screen_width // 2 - button_width // 2, screen_height // 2 + 200),
                                (button_width, button_height))

# Rules Screen Text
rules_content = [
    "Objective of the game: kill your opponent before they kill you.",
    "",
    "Rules:",
    "1. You will be in a 1 vs. 1 against someone in a ship.",
    "2. The goal of the game is to fire enough bullets to destroy your opponent's ship.",
    "3. You will have 3 types of bullets:",
    "   a. Normal bullets: regular damage, relatively high fire rate",
    "   b. Bombs: massive damage in exchange for a low speed, fire rate",
    "   c. Sharpshots: quick bullets with higher damage",
    "   d. Reflectors: reflect up to 10 bullets before breaking."
]


def draw_text_list(screen, text_list, font, color, x, y, line_spacing=10):
    for line in text_list:
        text = font.render(line, True, color)
        screen.blit(text, (x, y))
        y += text.get_height() + line_spacing


def main():
    running = True
    show_rules = False
    start_game = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    start_game = True
                elif rules_button_rect.collidepoint(event.pos):
                    show_rules = True

        screen.fill(black)

        if show_rules:
            draw_text_list(screen, rules_content, small_font, white, 20, 750)
        elif start_game:
            # Clear the screen and show a blank black screen
            screen.fill(black)
            # In a real game, this is where you would transition to the game logic
        else:
            # Draw the title text
            screen.blit(title_text,
                        (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - title_text.get_height() // 2))

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
