import os
import random
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PLAYER_SPEED = 7


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


def main_loop(screen, clock, puppy_img, background_img):

    
    puppy_x = SCREEN_WIDTH // 2 - puppy_img.get_width() // 2
    puppy_y = SCREEN_HEIGHT - puppy_img.get_height() - 20
    puppy_rect = puppy_img.get_rect(topleft=(puppy_x, puppy_y))

    puppy_img_left = puppy_img  
    puppy_img_right = pygame.transform.flip(puppy_img, True, False)  # Flipped horizontally
    current_puppy_img = puppy_img_right
    facing_right = True

    running = True

    while running:
        running = handle_events(running)

    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            puppy_x -= PLAYER_SPEED
            

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            puppy_x += PLAYER_SPEED
            

        puppy_x = max(0, min(puppy_x, SCREEN_WIDTH - current_puppy_img.get_width()))
        puppy_rect.x = puppy_x 
        screen.blit(background_img, (0, 0))
        screen.blit(current_puppy_img, puppy_rect.topleft)  

        pygame.display.flip()
        clock.tick(FPS)


def main():
    screen, clock = init_pygame()

    background_img = pygame.image.load("Assets/background.jpg").convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

     # Load puppy image and scale it down
    loaded_img = pygame.image.load("Assets/Puppy.png").convert_alpha()
    # Scale to reasonable size (100x100)
    puppy_img = pygame.transform.smoothscale(loaded_img, (100, 100))

    main_loop(screen, clock, puppy_img, background_img)

    pygame.quit()


if __name__ == "__main__":
    main()
