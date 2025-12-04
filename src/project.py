import os
import sys
import random
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


def init_pygame():
    """Initialize pygame and create the screen + clock."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Puppy Snack Catcher")
    clock = pygame.time.Clock()
    # load cloud image from Assets folder relative to this file
    cloud_path = os.path.join(os.path.dirname(__file__), "Assets", "cloud 2.png")
    try:
        cloud_img = pygame.image.load(cloud_path).convert_alpha()
    except Exception:
        # fallback: create a simple placeholder surface if image missing
        cloud_img = pygame.Surface((120, 60), pygame.SRCALPHA)
        pygame.draw.ellipse(cloud_img, (255, 255, 255), cloud_img.get_rect())
    return screen, clock, cloud_img


def handle_events(running):
    """Handle basic events like quitting the game window."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    return running


def main_loop(screen, clock, cloud_img):
    cloud_x = 50
    cloud_y = 80

    running = True
    while running:
        running = handle_events(running)

        # move cloud
        cloud_x += 1
        if cloud_x > SCREEN_WIDTH:
            cloud_x = -cloud_img.get_width()

        # draw sky + cloud
        screen.fill((135, 206, 235))
        screen.blit(cloud_img, (cloud_x, cloud_y))

        pygame.display.flip()
        clock.tick(FPS)


def main():
    screen, clock, cloud_img = init_pygame()
    main_loop(screen, clock, cloud_img)
    pygame.quit()


if __name__ == '__main__':
    main()