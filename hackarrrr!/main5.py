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

font = pygame.font.Font(None, 48)

pygame.mixer.music.load("background_music.mp3")
vine_sound = pygame.mixer.Sound("vine.mp3")

background = pygame.image.load("background.png").convert()

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
insult_index = 0
start_hurling_insults = False
insult_timer = 0

fade_alpha = 0
fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.fill(BLACK)

insults = {
    1: ["You are stupid", "You are ugly", "You are annoying"],
    2: ["You look like a rat.", "Your skin is dryer than Nando's chicken.", "You're short."],
    3: ["You have no life.", "You have the proportions of a bitmoji.", "You smell like bin sludge."]
}
def load_man_sprites(prefix):
    left_sprites = [pygame.image.load(f"{prefix}{i}l.png") for i in range(1, 4)]
    right_sprites = [pygame.image.load(f"{prefix}{i}r.png") for i in range(1, 4)]
    return left_sprites, right_sprites

def load_monster_sprites(prefix):
    return [pygame.image.load(f"{prefix}{i}.png") for i in range(1, 3)]

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

def fade_out_in():
    global fade_alpha
    fade_alpha = 0
    while fade_alpha < 255:
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        fade_alpha += 10
        pygame.time.delay(20)
    time.sleep(2)
    fade_alpha = 255
    while fade_alpha > 0:
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        fade_alpha -= 10
        pygame.time.delay(20)

def reset_stage():
    global keys_pressed, messages, man_x, monster_x, player_is_monster, insult_index, start_hurling_insults
    keys_pressed = {"a": False, "s": False, "d": False}
    messages = []
    insult_index = 0
    start_hurling_insults = False
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

def display_instructions():
    instructions = "Press A, S, D to insult the monster."
    text_surface = font.render(instructions, True, WHITE)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 20))

clock = pygame.time.Clock()
running = True
pygame.mixer.music.play(-1)

instruction_start_time = time.time()
show_instruction = True

while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not player_is_monster and stage <= 3:
                if event.key == pygame.K_a and not keys_pressed["a"]:
                    messages.append(insults[stage][0])
                    keys_pressed["a"] = True
                    vine_sound.play()
                elif event.key == pygame.K_s and not keys_pressed["s"]:
                    messages.append(insults[stage][1])
                    keys_pressed["s"] = True
                    vine_sound.play()
                elif event.key == pygame.K_d and not keys_pressed["d"]:
                    messages.append(insults[stage][2])
                    keys_pressed["d"] = True
                    vine_sound.play()
            if event.key == pygame.K_ESCAPE:
                running = False

    delta_time = clock.get_time() / 1000
    animation_timer += delta_time

    if show_instruction and time.time() - instruction_start_time < 3:
        display_instructions()
    elif time.time() - instruction_start_time >= 3:
        show_instruction = False

    if not player_is_monster and stage <= 3:
        keys = pygame.key.get_pressed()
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
        if start_hurling_insults and insult_index < len(insults[1]):
            insult_timer += delta_time
            if insult_timer > 1.5:  # Display an insult every 1.5 seconds
                insult_text = insults[1][insult_index]
                text_surface = font.render(insult_text, True, WHITE)
                x, y = random_position_for_insult(text_surface)
                screen.blit(text_surface, (x, y))
                insult_index += 1
                insult_timer = 0
    else:
        if man_direction == "left":
            screen.blit(man_left[man_frame], (man_x, man_y-200))
        elif man_direction == "right":
            screen.blit(man_right[man_frame], (man_x, man_y-200))
        else:
            screen.blit(man_right[0], (man_x, man_y-200))

    if not player_is_monster:
        screen.blit(monster_sprites[monster_frame], (monster_x, monster_y-300))
    else:
        screen.blit(monster_sprites[monster_frame], (monster_x, monster_y-300))

    for idx, msg in enumerate(messages):
        text_surface = font.render(msg, True, WHITE)
        x, y = random_position_for_insult(text_surface)
        screen.blit(text_surface, (x, y))

    if all_keys_pressed():
        fade_out_in()
        if stage < 3:
            stage += 1
            reset_stage()
        elif stage == 3:
            stage += 1
            reset_stage()
            start_hurling_insults = True
        elif stage == 4 and insult_index >= len(insults[1]):
            fade_out_in()
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
