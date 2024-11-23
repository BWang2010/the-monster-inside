import pygame
import sys
import time
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("You Are Your Own Enemy")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (10, 10, 50)

font = pygame.font.Font(None, 48)

pygame.mixer.music.load("background_music.mp3")

man_x = 100
man_y = HEIGHT - 150
monster_x = WIDTH - 200
monster_y = HEIGHT - 150

man_speed = 8
man_direction = "right"
man_frame = 0
monster_frame = 0
man_animation_speed = 0.2
monster_animation_speed = 0.3
animation_timer = 0
monster_timer = 0

stage = 1
player_is_monster = False
fading = False
keys_pressed = {"a": False, "s": False, "d": False}
messages = []

fade_alpha = 0
fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.fill(BLACK)

PLATFORM_HEIGHT = 100

insults = {
    1: ["You are stupid", "You are ugly", "You are annoying"],
    2: ["_", "_", "_"],
    3: ["_", "_", "_"]
}

def load_man_sprites(prefix):
    left_sprites = [pygame.image.load(f"{prefix}{i}l.png") for i in range(1, 5)]
    right_sprites = [pygame.image.load(f"{prefix}{i}r.png") for i in range(1, 5)]
    return left_sprites, right_sprites

def load_monster_sprites(prefix):
    return [pygame.image.load(f"{prefix}{i}.png") for i in range(1, 5)]

man_left, man_right = load_man_sprites("man")
monster_sprites = load_monster_sprites("monster")

def update_sprites():
    global man_left, man_right, monster_sprites
    if stage == 2:
        man_left, man_right = load_man_sprites("evilman")
        monster_sprites = load_monster_sprites("evilmonster")
    elif stage == 3:
        man_left, man_right = load_man_sprites("evilevilman")
        monster_sprites = load_monster_sprites("evilevilmonster")

def fade_screen():
    global fade_alpha
    fade_alpha += 5
    if fade_alpha >= 255:
        fade_alpha = 255
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(500)
        return True
    fade_surface.set_alpha(fade_alpha)
    screen.blit(fade_surface, (0, 0))
    return False

def reset_stage():
    global keys_pressed, messages, fade_alpha, man_x, monster_x, player_is_monster
    keys_pressed = {"a": False, "s": False, "d": False}
    messages = []
    fade_alpha = 0
    man_x = 100
    monster_x = WIDTH - 200
    if stage == 4:
        player_is_monster = True
        monster_x = 100
        man_x = WIDTH - 200
    update_sprites()

def manage_music():
    pygame.mixer.music.play(-1)

def all_keys_pressed():
    return all(keys_pressed.values())

def random_position_for_insult(text_surface):
    x = random.randint(50, WIDTH - text_surface.get_width() - 50)
    y = random.randint(50, HEIGHT // 3 - text_surface.get_height())
    return x, y

clock = pygame.time.Clock()
running = True
pygame.mixer.music.play(-1)

while running:
    screen.fill(DARK_BLUE)

    pygame.draw.rect(screen, BLACK, (0, HEIGHT - PLATFORM_HEIGHT, WIDTH, PLATFORM_HEIGHT))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not player_is_monster and stage <= 3:
                if event.key == pygame.K_a and not keys_pressed["a"]:
                    messages.append(insults[stage][0])
                    keys_pressed["a"] = True
                elif event.key == pygame.K_s and not keys_pressed["s"]:
                    messages.append(insults[stage][1])
                    keys_pressed["s"] = True
                elif event.key == pygame.K_d and not keys_pressed["d"]:
                    messages.append(insults[stage][2])
                    keys_pressed["d"] = True
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()
    delta_time = clock.get_time() / 1000
    animation_timer += delta_time

    if not player_is_monster:
        if keys[pygame.K_LEFT]:
            man_x -= man_speed
            man_direction = "left"
            if animation_timer >= man_animation_speed:
                man_frame = (man_frame + 1) % len(man_left)
                animation_timer = 0
        elif keys[pygame.K_RIGHT]:
            man_x += man_speed
            man_direction = "right"
            if animation_timer >= man_animation_speed:
                man_frame = (man_frame + 1) % len(man_right)
                animation_timer = 0
        else:
            man_frame = 0

    monster_timer += delta_time
    if monster_timer >= monster_animation_speed:
        monster_frame = (monster_frame + 1) % len(monster_sprites)
        monster_timer = 0

    if player_is_monster:
        screen.blit(monster_sprites[monster_frame], (man_x, man_y-200))
    else:
        if man_direction == "left":
            screen.blit(man_left[man_frame], (man_x, man_y-200))
        elif man_direction == "right":
            screen.blit(man_right[man_frame], (man_x, man_y-200))
        else:
            screen.blit(man_right[0], (man_x, man_y-200))

    if not player_is_monster:
        screen.blit(monster_sprites[monster_frame], (monster_x, monster_y-400))

    for idx, msg in enumerate(messages):
        text_surface = font.render(msg, True, WHITE)
        x, y = random_position_for_insult(text_surface)
        screen.blit(text_surface, (x, y))

    if all_keys_pressed():
        fading = True

    if fading:
        if fade_screen():
            fading = False
            if stage < 3:
                stage += 1
                reset_stage()
            elif stage == 3:
                stage += 1
                reset_stage()
            else:
                fade_screen()
                fade_text("You were your own enemy all along.")
                fade_text("_")
                fade_text("_")
                fade_text("_")
                fade_text("_")
                running = False

    manage_music()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
