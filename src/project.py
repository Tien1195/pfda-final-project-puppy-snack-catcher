import os
import random
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PLAYER_SPEED = 8

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)

ITEM_FALL_SPEED = 7
ITEM_SPAWN_RATE = 10
GAME_TIME = 10


ITEMS = {
    'chips.png': 5,
    'corn.png': 10,
    'corn_dog.png': 20,
    'cotton_candy.png': 25,
    'fish_bone.png': -20,
    'sock.png': -15
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
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Puppy Snack Catcher")
    clock = pygame.time.Clock()
    return screen, clock


def handle_events(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    return running


def main_loop(screen, clock, puppy_img, background_img, happy_sound, sad_sound):
    all_items = pygame.sprite.Group()

    puppy_x = SCREEN_WIDTH // 2 - puppy_img.get_width() // 2
    puppy_y = SCREEN_HEIGHT - puppy_img.get_height() - 20
    puppy_rect = puppy_img.get_rect(topleft=(puppy_x, puppy_y))

    puppy_img_left = puppy_img
    puppy_img_right = pygame.transform.flip(puppy_img, True, False)  
    current_puppy_img = puppy_img_right
    facing_right = True

    score = 10
    frame_count = 0
    start_time = pygame.time.get_ticks()
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)
    large_font = pygame.font.Font(None, 72)

    running = True
    game_over = False

    while running:
        running = handle_events(running)

        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  
        remaining_time = max(0, GAME_TIME - elapsed_time)

        if (remaining_time <= 0 or score <= 0 or score >= 100) and not game_over:
            game_over = True

        if not game_over:
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

        for item in all_items:
            if puppy_rect.colliderect(item.rect):
                if item.score > 0:
                    happy_sound.play()
                else:
                    sad_sound.play()      
                score += item.score
                if score < 0:
                    score = 0
                if score >= 100:
                    score = 100
                    game_over = True
                item.kill()
     
        screen.blit(background_img, (0, 0))

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)  
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        if not game_over:    
            all_items.draw(screen)

            screen.blit(current_puppy_img, puppy_rect.topleft)

            score_text = font.render(f'Score: {score}', True, WHITE)
            score_shadow = font.render(f'Score: {score}', True, BLACK)
            screen.blit(score_shadow, (22, 22))
            screen.blit(score_text, (20, 20))

            timer_text = font.render(f'Time: {int(remaining_time)}', True, WHITE)
            timer_shadow = font.render(f'Time: {int(remaining_time)}', True, BLACK)
            screen.blit(timer_shadow, (SCREEN_WIDTH - timer_text.get_width() - 18, 22))
            screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 20, 20))


        else:
            
            if score >= 100:
                game_over_text = large_font.render('YOU WIN!', True, WHITE)
                game_over_shadow = large_font.render('YOU WIN!', True, BLACK)
            else:
                game_over_text = large_font.render('GAME OVER!', True, WHITE)
                game_over_shadow = large_font.render('GAME OVER!', True, BLACK)
            screen.blit(game_over_shadow, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2 + 3, 153))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))

            final_score_text = font.render(f'Final Score: {score}', True, WHITE)
            final_score_shadow = font.render(f'Final Score: {score}', True, BLACK)
            screen.blit(final_score_shadow, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2 + 2, 252))
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 250))

            restart_text = small_font.render('Press R to Restart or ESC to Quit', True, WHITE)
            restart_shadow = small_font.render('Press R to Restart or ESC to Quit', True, BLACK)
            screen.blit(restart_shadow, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2 + 2, 352))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:              
                return True  
            if keys[pygame.K_ESCAPE]:
                running = False
   
        pygame.display.flip()
        clock.tick(FPS)

    return False  
def main():
    screen, clock = init_pygame()

    background_img = pygame.image.load("Assets/background.jpg").convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    loaded_img = pygame.image.load("Assets/Puppy.png").convert_alpha()
    puppy_img = pygame.transform.smoothscale(loaded_img, (100, 100))

    happy_sound = pygame.mixer.Sound("Assets/happy.mp3")
    sad_sound = pygame.mixer.Sound("Assets/sad.mp3")

    restart = True
    while restart:
        restart = main_loop(screen, clock, puppy_img, background_img, happy_sound, sad_sound)

    pygame.quit()


if __name__ == "__main__":
    main()
