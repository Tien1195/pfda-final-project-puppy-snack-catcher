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

ITEM_FALL_SPEED = 3
ITEM_SPAWN_RATE = 60


ITEMS = {
    'chips.png': -10,
    'corn.png': 15,
    'corn_dog.png': 20,
    'cotton_candy.png': 25,
}


class FallingItem(pygame.sprite.Sprite):
    def __init__(self, item_name, score):
        super().__init__()
        self.score = score
        self.item_name = item_name

        img_path = os.path.join("Assets", item_name)
        loaded = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.smoothscale(loaded, (60, 60))

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

    def update(self):
        self.rect.y += ITEM_FALL_SPEED

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


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
    all_items = pygame.sprite.Group()

    puppy_x = SCREEN_WIDTH // 2 - puppy_img.get_width() // 2
    puppy_y = SCREEN_HEIGHT - puppy_img.get_height() - 20
    puppy_rect = puppy_img.get_rect(topleft=(puppy_x, puppy_y))

    puppy_img_left = puppy_img
    puppy_img_right = pygame.transform.flip(puppy_img, True, False)  
    current_puppy_img = puppy_img_right
    facing_right = True

    frame_count = 0
    running = True

    while running:
        running = handle_events(running)

 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            puppy_x -= PLAYER_SPEED
     
            if facing_right:
                current_puppy_img = puppy_img_left
                facing_right = False

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            puppy_x += PLAYER_SPEED

            if not facing_right:
                current_puppy_img = puppy_img_right
                facing_right = True

        puppy_x = max(0, min(puppy_x, SCREEN_WIDTH - current_puppy_img.get_width()))
        puppy_rect.x = puppy_x


        frame_count += 1                       
        if frame_count >= ITEM_SPAWN_RATE:
            frame_count = 0
            item_name = random.choice(list(ITEMS.keys()))
            item_score = ITEMS[item_name]
            new_item = FallingItem(item_name, item_score)
            all_items.add(new_item)

     
        all_items.update()

     
        screen.blit(background_img, (0, 0))
        all_items.draw(screen)
        screen.blit(current_puppy_img, puppy_rect.topleft)

        pygame.display.flip()
        clock.tick(FPS)


def main():
    screen, clock = init_pygame()

    background_img = pygame.image.load("Assets/background.jpg").convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    loaded_img = pygame.image.load("Assets/Puppy.png").convert_alpha()
    puppy_img = pygame.transform.smoothscale(loaded_img, (100, 100))

    main_loop(screen, clock, puppy_img, background_img)

    pygame.quit()


if __name__ == "__main__":
    main()
