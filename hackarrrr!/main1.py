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
RED = (255, 0, 0)
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

blob_moving_back = False
stage = 1
messages = []
current_insult = 0
fading = False
player_is_monster = False
keys_pressed = {"a": False, "s": False, "d": False}
start_time = time.time()

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

def fade_text(message):
    fade_alpha = 0
    text_surface = font.render(message, True, WHITE)
    while fade_alpha < 255:
        screen.fill(BLACK)
        text_surface.set_alpha(fade_alpha)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2,
                                   HEIGHT // 2 - text_surface.get_height() // 2))
        pygame.display.flip()
        fade_alpha += 5
        pygame.time.delay(50)

    pygame.time.delay(2000)

    while fade_alpha > 0:
        screen.fill(BLACK)
        text_surface.set_alpha(fade_alpha)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2,
                                   HEIGHT // 2 - text_surface.get_height() // 2))
        pygame.display.flip()
        fade_alpha -= 5
        pygame.time.delay(50)

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
    global messages, fade_alpha, blob_moving_back, stage, monster_x, man_x, player_is_monster, current_insult, keys_pressed, start_time
    messages = []
    fade_alpha = 0
    blob_moving_back = False
    man_x = 100
    monster_x = WIDTH - 200
    keys_pressed = {"a": False, "s": False, "d": False}
    if stage == 2:
        monster_x = 100
        man_x = WIDTH - 200
    stage += 1
    player_is_monster = (stage == 4)
    current_insult = 0
    start_time = time.time()
    update_sprites()

def manage_music():
    elapsed_time = time.time() - start_time
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_pos(elapsed_time % 180)

def random_position_for_insult(text_surface):
    x = random.randint(50, WIDTH - text_surface.get_width() - 50)
    y = random.randint(50, HEIGHT // 3 - text_surface.get_height())
    return x, y

clock = pygame.time.Clock()
running = True
pygame.mixer.music.play(-1)

show_instruction = True
instruction_start_time = time.time()

while running:
    screen.fill(DARK_BLUE)

    pygame.draw.rect(screen, BLACK, (0, HEIGHT - PLATFORM_HEIGHT, WIDTH, PLATFORM_HEIGHT))

    if show_instruction and time.time() - instruction_start_time < 4:
        instructions = "Press a, s, d to insult the monster"
        instructions_surface = font.render(instructions, True, WHITE)
        screen.blit(instructions_surface, (WIDTH // 2 - instructions_surface.get_width() // 2, 20))
    elif time.time() - instruction_start_time >= 4:
        show_instruction = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if stage <= 3 and not player_is_monster:
                if event.key == pygame.K_a and not keys_pressed["a"]:
                    messages.append(insults[stage][0])
                    keys_pressed["a"] = True
                    blob_moving_back = True
                elif event.key == pygame.K_s and not keys_pressed["s"]:
                    messages.append(insults[stage][1])
                    keys_pressed["s"] = True
                    blob_moving_back = True
                elif event.key == pygame.K_d and not keys_pressed["d"]:
                    messages.append(insults[stage][2])
                    keys_pressed["d"] = True
                    blob_moving_back = True

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
        screen.blit(monster_sprites[monster_frame], (man_x, man_y - 200))
    else:
        if man_direction == "left":
            screen.blit(man_left[man_frame], (man_x, man_y- 200))
        elif man_direction == "right":
            screen.blit(man_right[man_frame], (man_x, man_y - 200))
        else:
            screen.blit(man_right[0], (man_x, man_y - 200))

    if not player_is_monster:
        screen.blit(monster_sprites[monster_frame], (monster_x, monster_y - 400))

    if stage <= 3 and current_insult < len(insults[stage]):
        text_surface = font.render(insults[stage][current_insult], True, WHITE)
        x, y = random_position_for_insult(text_surface)
        screen.blit(text_surface, (x, y))
        current_insult += 1

    for idx, msg in enumerate(messages):
        text = font.render(msg, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + idx * 50))

    if len(messages) == 3 and stage <= 3:
        fading = True

    if current_insult == len(insults[stage]) and stage == 4:
        fading = True

    if fade_screen():
        if stage < 3:
            reset_stage()
            fading = False
        else:
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
