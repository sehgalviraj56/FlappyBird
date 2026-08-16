import sys
import time
import random
import json
import os
import traceback

def show_crash(msg):
    try:
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Toast = autoclass('android.widget.Toast')
        String = autoclass('java.lang.String')
        activity = PythonActivity.mActivity
        activity.runOnUiThread(lambda: Toast.makeText(activity, String(str(msg)[:400]), Toast.LENGTH_LONG).show())
    except Exception:
        pass
    try:
        with open("crash_log.txt", "w") as f:
            f.write(msg)
    except Exception:
        pass
    time.sleep(15)

def crash_hook(t, v, tb):
    show_crash("".join(traceback.format_exception(t, v, tb)))

sys.excepthook = crash_hook

try:
    import pygame
    pygame.init()
except Exception:
    show_crash(traceback.format_exc())
    raise

# ---- sound manager (inlined, no separate file needed) ----
sound_enabled = False
SND_BEEP = None
SND_DIE = None
SND_CLICK = None

try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    if os.path.exists("beep.mp3"):
        SND_BEEP = pygame.mixer.Sound("beep.mp3")
    if os.path.exists("die.mp3"):
        SND_DIE = pygame.mixer.Sound("die.mp3")
    if os.path.exists("click.mp3"):
        SND_CLICK = pygame.mixer.Sound("click.mp3")
    sound_enabled = True
except Exception as e:
    print(f"Sound initialization error: {e}")
    sound_enabled = False

def play_beep():
    if sound_enabled and SND_BEEP:
        try:
            SND_BEEP.play()
        except:
            pass

def play_die():
    if sound_enabled and SND_DIE:
        try:
            SND_DIE.play()
        except:
            pass

def play_click():
    if sound_enabled and SND_CLICK:
        try:
            SND_CLICK.play()
        except:
            pass
# ---- end sound manager ----

# FULL SCREEN RESOLUTION FOR MOBILE
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

clock = pygame.time.Clock()

def play_sound(snd=None):
    pass

# --- 3D ENHANCED COLOR PALETTE ---
SKY_BLUE = (110, 175, 255)
CLOUD_WHITE = (245, 250, 255)
CLOUD_SHADOW = (210, 220, 235)

BUILDING_MAIN = (80, 95, 125)
BUILDING_LIGHT = (120, 140, 175)
BUILDING_SHADOW = (50, 60, 85)
WINDOW_GLOW = (255, 235, 130)

MC_GRASS_TOP = (100, 200, 50)
MC_GRASS_SIDE = (65, 140, 35)
MC_GRASS_SHADOW = (40, 90, 20)
MC_DIRT = (145, 105, 75)
MC_DIRT_DARK = (100, 70, 45)

PIPE_BASE = (50, 205, 50)
PIPE_LIGHT = (110, 235, 110)
PIPE_DARK = (25, 120, 25)
PIPE_BORDER = (10, 50, 10)

MC_WHITE = (250, 250, 250)
MC_SHADOW = (180, 185, 195)
MC_HIGHLIGHT = (255, 255, 255)
MC_RED = (230, 40, 40)
MC_RED_DARK = (160, 20, 20)
MC_YELLOW = (255, 190, 30)

BTN_TOP = (80, 150, 210)
BTN_BASE = (50, 110, 160)
BTN_SHADOW = (30, 70, 110)
BTN_RESET_TOP = (210, 80, 80)
BTN_RESET_BASE = (160, 50, 50)
BTN_RESET_SHADOW = (100, 30, 30)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

HIGH_SCORE_FILE = "highscore.json"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except:
            return 0
    return 0

def save_high_score(new_high_score):
    try:
        data = {"high_score": new_high_score}
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump(data, f)
    except:
        pass

def reset_high_score_file():
    save_high_score(0)

high_score = load_high_score()

game_state = "MENU"

bird_x = int(WIDTH * 0.25)
bird_y = int(HEIGHT * 0.4)
gravity = HEIGHT * 0.0006
bird_movement = 0

pipe_x = WIDTH
pipe_width = int(WIDTH * 0.18)
pipe_gap = int(HEIGHT * 0.26)
pipe_height = random.randint(int(HEIGHT * 0.15), int(HEIGHT * 0.45))
score = 0

font_title = pygame.font.Font(None, int(WIDTH * 0.13))
font_large = pygame.font.Font(None, int(WIDTH * 0.1))
font_small = pygame.font.Font(None, int(WIDTH * 0.055))

clouds = [[30, int(HEIGHT * 0.08)], [int(WIDTH * 0.5), int(HEIGHT * 0.12)], [int(WIDTH * 0.8), int(HEIGHT * 0.06)]]

buildings = [
    [0, int(WIDTH * 0.22), int(HEIGHT * 0.35)],
    [int(WIDTH * 0.2), int(WIDTH * 0.28), int(HEIGHT * 0.48)],
    [int(WIDTH * 0.45), int(WIDTH * 0.2), int(HEIGHT * 0.3)],
    [int(WIDTH * 0.62), int(WIDTH * 0.25), int(HEIGHT * 0.42)],
    [int(WIDTH * 0.82), int(WIDTH * 0.25), int(HEIGHT * 0.33)]
]

def reset_game():
    global bird_y, bird_movement, pipe_x, score, pipe_height
    bird_y = int(HEIGHT * 0.4)
    bird_movement = 0
    pipe_x = WIDTH
    score = 0
    pipe_height = random.randint(int(HEIGHT * 0.15), int(HEIGHT * 0.45))

def draw_3d_button(text, y_pos, w=200, h=50, is_reset=False):
    rect = pygame.Rect(WIDTH // 2 - w // 2, y_pos, w, h)
    top_c = BTN_RESET_TOP if is_reset else BTN_TOP
    base_c = BTN_RESET_BASE if is_reset else BTN_BASE
    shadow_c = BTN_RESET_SHADOW if is_reset else BTN_SHADOW
    pygame.draw.rect(screen, shadow_c, (rect.x, rect.y + 6, rect.width, rect.height), border_radius=10)
    pygame.draw.rect(screen, base_c, rect, border_radius=10)
    pygame.draw.rect(screen, top_c, (rect.x + 2, rect.y + 2, rect.width - 4, rect.height // 2), border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
    txt_surf = font_small.render(text, True, WHITE)
    txt_rect = txt_surf.get_rect(center=(rect.centerx, rect.centery + 1))
    screen.blit(txt_surf, txt_rect)
    return rect

def draw_3d_bird(x, y):
    bw, bh = 38, 30
    bx, by = x - bw // 2, y - bh // 2
    pygame.draw.rect(screen, MC_SHADOW, (bx, by, bw, bh))
    pygame.draw.rect(screen, MC_WHITE, (bx, by, bw - 3, bh - 4))
    pygame.draw.rect(screen, MC_HIGHLIGHT, (bx + 2, by + 2, bw - 7, 6))
    pygame.draw.rect(screen, MC_SHADOW, (bx + 4, by + 12, 12, 10))
    pygame.draw.rect(screen, MC_WHITE, (bx + 2, by + 10, 12, 10))
    pygame.draw.rect(screen, MC_HIGHLIGHT, (bx + 2, by + 10, 12, 3))
    pygame.draw.rect(screen, BLACK, (bx + bw - 12, by + 4, 6, 8))
    pygame.draw.rect(screen, WHITE, (bx + bw - 10, by + 4, 2, 3))
    pygame.draw.rect(screen, MC_YELLOW, (bx + bw - 2, by + 10, 12, 8))
    pygame.draw.rect(screen, BLACK, (bx + bw - 2, by + 10, 12, 8), 1)
    pygame.draw.rect(screen, MC_RED_DARK, (bx + bw - 4, by + 18, 8, 7))
    pygame.draw.rect(screen, MC_RED, (bx + bw - 4, by + 18, 8, 5))

def draw_3d_city():
    ground_level = HEIGHT - 60
    for b in buildings:
        bx, bw, bh = b[0], b[1], b[2]
        by = ground_level - bh
        pygame.draw.rect(screen, BUILDING_MAIN, (bx, by, bw, bh))
        pygame.draw.rect(screen, BUILDING_LIGHT, (bx, by, 8, bh))
        pygame.draw.rect(screen, BUILDING_SHADOW, (bx + bw - 8, by, 8, bh))
        win_w, win_h = 8, 12
        for wx in range(bx + 14, bx + bw - 14, 18):
            for wy in range(by + 15, ground_level - 15, 25):
                pygame.draw.rect(screen, BUILDING_SHADOW, (wx - 1, wy - 1, win_w + 2, win_h + 2))
                pygame.draw.rect(screen, WINDOW_GLOW, (wx, wy, win_w, win_h))

def draw_3d_pipe(x, height):
    pygame.draw.rect(screen, PIPE_BASE, (x, 0, pipe_width, height))
    pygame.draw.rect(screen, PIPE_LIGHT, (x + 4, 0, 10, height))
    pygame.draw.rect(screen, PIPE_DARK, (x + pipe_width - 14, 0, 14, height))
    pygame.draw.rect(screen, PIPE_BORDER, (x, 0, pipe_width, height), 3)
    lip_y = height - 28
    pygame.draw.rect(screen, PIPE_BASE, (x - 6, lip_y, pipe_width + 12, 28))
    pygame.draw.rect(screen, PIPE_LIGHT, (x - 2, lip_y + 2, 10, 24))
    pygame.draw.rect(screen, PIPE_DARK, (x + pipe_width - 10, lip_y, 12, 28))
    pygame.draw.rect(screen, PIPE_BORDER, (x - 6, lip_y, pipe_width + 12, 28), 3)
    bottom_y = height + pipe_gap
    bottom_h = HEIGHT - bottom_y - 60
    pygame.draw.rect(screen, PIPE_BASE, (x, bottom_y, pipe_width, bottom_h))
    pygame.draw.rect(screen, PIPE_LIGHT, (x + 4, bottom_y, 10, bottom_h))
    pygame.draw.rect(screen, PIPE_DARK, (x + pipe_width - 14, bottom_y, 14, bottom_h))
    pygame.draw.rect(screen, PIPE_BORDER, (x, bottom_y, pipe_width, bottom_h), 3)
    pygame.draw.rect(screen, PIPE_BASE, (x - 6, bottom_y, pipe_width + 12, 28))
    pygame.draw.rect(screen, PIPE_LIGHT, (x - 2, bottom_y + 2, 10, 24))
    pygame.draw.rect(screen, PIPE_DARK, (x + pipe_width - 10, bottom_y, 12, 28))
    pygame.draw.rect(screen, PIPE_BORDER, (x - 6, bottom_y, pipe_width + 12, 28), 3)

def draw_3d_ground():
    gy = HEIGHT - 60
    pygame.draw.rect(screen, MC_DIRT, (0, gy, WIDTH, 60))
    for x in range(0, WIDTH, 28):
        pygame.draw.rect(screen, MC_DIRT_DARK, (x + 4, gy + 22, 12, 12))
        pygame.draw.rect(screen, MC_DIRT_DARK, (x + 16, gy + 40, 10, 10))
    pygame.draw.rect(screen, MC_GRASS_TOP, (0, gy, WIDTH, 14))
    pygame.draw.rect(screen, MC_GRASS_SIDE, (0, gy + 14, WIDTH, 4))
    for x in range(0, WIDTH, 16):
        h = 8 if (x // 16) % 2 == 0 else 14
        pygame.draw.rect(screen, MC_GRASS_SIDE, (x, gy + 14, 12, h))
        pygame.draw.rect(screen, MC_GRASS_SHADOW, (x, gy + 14 + h - 3, 12, 3))

while True:
    mouse_pos = pygame.mouse.get_pos()
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
            click = True

    screen.fill(SKY_BLUE)

    for cloud in clouds:
        cloud[0] -= 0.5
        if cloud[0] < -80:
            cloud[0] = WIDTH + 30
        cx, cy = int(cloud[0]), cloud[1]
        pygame.draw.circle(screen, CLOUD_SHADOW, (cx + 2, cy + 3), 30)
        pygame.draw.circle(screen, CLOUD_WHITE, (cx, cy), 30)
        pygame.draw.circle(screen, CLOUD_WHITE, (cx + 25, cy - 12), 35)

    draw_3d_city()

    if game_state == "MENU":
        title_surf = font_title.render("FLAPPY BIRD 3D", True, WHITE)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT * 0.20))
        screen.blit(title_surf, title_rect)
        hs_surf = font_small.render(f"BEST SCORE: {high_score}", True, WINDOW_GLOW)
        screen.blit(hs_surf, hs_surf.get_rect(center=(WIDTH // 2, HEIGHT * 0.29)))
        btn_start = draw_3d_button("START GAME", int(HEIGHT * 0.38), w=int(WIDTH * 0.65))
        btn_reset_hs = draw_3d_button("RESET HIGH SCORE", int(HEIGHT * 0.49), w=int(WIDTH * 0.65), is_reset=True)
        btn_credits = draw_3d_button("CREDITS", int(HEIGHT * 0.60), w=int(WIDTH * 0.65))
        btn_exit = draw_3d_button("EXIT", int(HEIGHT * 0.71), w=int(WIDTH * 0.65))
        if click:
            if btn_start.collidepoint(mouse_pos):
                reset_game()
                game_state = "PLAYING"
            elif btn_reset_hs.collidepoint(mouse_pos):
                reset_high_score_file()
                high_score = 0
            elif btn_credits.collidepoint(mouse_pos):
                game_state = "CREDITS"
            elif btn_exit.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    elif game_state == "CREDITS":
        cred_title = font_large.render("CREDITS", True, WHITE)
        screen.blit(cred_title, cred_title.get_rect(center=(WIDTH // 2, HEIGHT * 0.3)))
        dev_txt = font_small.render("Developed By:", True, WHITE)
        name_txt = font_large.render("TheSpookyRavager", True, BLACK)
        screen.blit(dev_txt, dev_txt.get_rect(center=(WIDTH // 2, HEIGHT * 0.45)))
        screen.blit(name_txt, name_txt.get_rect(center=(WIDTH // 2, HEIGHT * 0.52)))
        btn_back = draw_3d_button("BACK", int(HEIGHT * 0.7), w=int(WIDTH * 0.4))
        if click and btn_back.collidepoint(mouse_pos):
            game_state = "MENU"

    elif game_state == "PLAYING":
        if click:
            pause_btn_rect = pygame.Rect(WIDTH - 60, 20, 45, 45)
            if pause_btn_rect.collidepoint(mouse_pos):
                game_state = "PAUSED"
            else:
                bird_movement = -HEIGHT * 0.012

        bird_movement += gravity
        bird_y += bird_movement
        draw_3d_bird(bird_x, bird_y)

        pipe_x -= WIDTH * 0.008
        if pipe_x < -pipe_width - 20:
            pipe_x = WIDTH
            pipe_height = random.randint(int(HEIGHT * 0.15), int(HEIGHT * 0.45))
            score += 1
            if score > high_score:
                high_score = score
                save_high_score(high_score)

        draw_3d_pipe(pipe_x, pipe_height)

        bird_rect = pygame.Rect(bird_x - 18, bird_y - 14, 36, 28)
        top_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
        bottom_pipe = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT)

        if bird_y <= 0 or bird_y >= HEIGHT - 60 or bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            game_state = "GAMEOVER"

        score_surf = font_small.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (20, 25))
        best_surf = font_small.render(f"Best: {high_score}", True, WINDOW_GLOW)
        screen.blit(best_surf, (20, 60))

        pause_rect = pygame.Rect(WIDTH - 60, 20, 45, 45)
        pygame.draw.rect(screen, BTN_SHADOW, (WIDTH - 60, 24, 45, 45), border_radius=8)
        pygame.draw.rect(screen, BTN_TOP, pause_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, (WIDTH - 48, 30, 6, 25))
        pygame.draw.rect(screen, WHITE, (WIDTH - 36, 30, 6, 25))

    elif game_state == "PAUSED":
        draw_3d_bird(bird_x, bird_y)
        draw_3d_pipe(pipe_x, pipe_height)
        p_title = font_large.render("GAME PAUSED", True, WHITE)
        screen.blit(p_title, p_title.get_rect(center=(WIDTH // 2, HEIGHT * 0.3)))
        btn_resume = draw_3d_button("RESUME", int(HEIGHT * 0.45), w=int(WIDTH * 0.6))
        btn_restart = draw_3d_button("RESTART", int(HEIGHT * 0.55), w=int(WIDTH * 0.6))
        btn_main = draw_3d_button("MAIN MENU", int(HEIGHT * 0.65), w=int(WIDTH * 0.6))
        if click:
            if btn_resume.collidepoint(mouse_pos):
                game_state = "PLAYING"
            elif btn_restart.collidepoint(mouse_pos):
                reset_game()
                game_state = "PLAYING"
            elif btn_main.collidepoint(mouse_pos):
                game_state = "MENU"

    elif game_state == "GAMEOVER":
        go_txt = font_large.render("GAME OVER", True, WHITE)
        screen.blit(go_txt, go_txt.get_rect(center=(WIDTH // 2, HEIGHT * 0.32)))
        score_txt = font_small.render(f"Score: {score}", True, WHITE)
        best_txt = font_small.render(f"High Score: {high_score}", True, WINDOW_GLOW)
        screen.blit(score_txt, score_txt.get_rect(center=(WIDTH // 2, HEIGHT * 0.40)))
        screen.blit(best_txt, best_txt.get_rect(center=(WIDTH // 2, HEIGHT * 0.46)))
        btn_retry = draw_3d_button("RETRY", int(HEIGHT * 0.58), w=int(WIDTH * 0.5))
        btn_menu = draw_3d_button("MENU", int(HEIGHT * 0.68), w=int(WIDTH * 0.5))
        if click:
            if btn_retry.collidepoint(mouse_pos):
                reset_game()
                game_state = "PLAYING"
            elif btn_menu.collidepoint(mouse_pos):
                game_state = "MENU"

    draw_3d_ground()
    pygame.display.update()
    clock.tick(60)
