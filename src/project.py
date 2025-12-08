import os
import random
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)


def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Puppy Snack Catcher")
    clock = pygame.time.Clock()
    return screen, clock


def handle_events(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    return running


def main_loop(screen, clock, background_img):

    running = True

    while running:

        running = handle_events(running)

        screen.blit(background_img, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)


def main():
    screen, clock = init_pygame()

    background_img = pygame.image.load("Assets/background.jpg").convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))


    main_loop(screen, clock, background_img)

    pygame.quit()


if __name__ == "__main__":
    main()
