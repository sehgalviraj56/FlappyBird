import os
import json
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock

WIDTH, HEIGHT = Window.width, Window.height


def c(r, g, b):
    return (r / 255, g / 255, b / 255, 1)


SKY_BLUE = c(110, 175, 255)
CLOUD_WHITE = c(245, 250, 255)
CLOUD_SHADOW = c(210, 220, 235)

BUILDING_MAIN = c(80, 95, 125)
BUILDING_LIGHT = c(120, 140, 175)
BUILDING_SHADOW = c(50, 60, 85)
WINDOW_GLOW = c(255, 235, 130)

MC_GRASS_TOP = c(100, 200, 50)
MC_GRASS_SIDE = c(65, 140, 35)
MC_GRASS_SHADOW = c(40, 90, 20)
MC_DIRT = c(145, 105, 75)
MC_DIRT_DARK = c(100, 70, 45)

PIPE_BASE = c(50, 205, 50)
PIPE_LIGHT = c(110, 235, 110)
PIPE_DARK = c(25, 120, 25)
PIPE_BORDER = c(10, 50, 10)

MC_WHITE = c(250, 250, 250)
MC_SHADOW = c(180, 185, 195)
MC_HIGHLIGHT = c(255, 255, 255)
MC_RED = c(230, 40, 40)
MC_RED_DARK = c(160, 20, 20)
MC_YELLOW = c(255, 190, 30)

BTN_TOP = c(80, 150, 210)
BTN_BASE = c(50, 110, 160)
BTN_SHADOW = c(30, 70, 110)
BTN_RESET_TOP = c(210, 80, 80)
BTN_RESET_BASE = c(160, 50, 50)
BTN_RESET_SHADOW = c(100, 30, 30)

WHITE = c(255, 255, 255)
BLACK = c(0, 0, 0)

HIGH_SCORE_FILE = "highscore.json"


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return json.load(f).get("high_score", 0)
        except Exception:
            return 0
    return 0


def save_high_score(new_high_score):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump({"high_score": new_high_score}, f)
    except Exception:
        pass


class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.snd_beep = SoundLoader.load("beep.mp3") if os.path.exists("beep.mp3") else None
        self.snd_die = SoundLoader.load("die.mp3") if os.path.exists("die.mp3") else None
        self.snd_click = SoundLoader.load("click.mp3") if os.path.exists("click.mp3") else None

        self.high_score = load_high_score()
        self.game_state = "MENU"

        self.bird_x = int(WIDTH * 0.25)
        self.bird_y = int(HEIGHT * 0.4)
        self.gravity = HEIGHT * 0.0006
        self.bird_movement = 0

        self.pipe_x = WIDTH
        self.pipe_width = int(WIDTH * 0.18)
        self.pipe_gap = int(HEIGHT * 0.26)
        self.pipe_height = random.randint(int(HEIGHT * 0.15), int(HEIGHT * 0.45))
        self.score = 0

        self.clouds = [[30, int(HEIGHT * 0.08)], [int(WIDTH * 0.5), int(HEIGHT * 0.12)], [int(WIDTH * 0.8), int(HEIGHT * 0.06)]]

        self.buildings = [
            [0, int(WIDTH * 0.22), int(HEIGHT * 0.35)],
            [int(WIDTH * 0.2), int(WIDTH * 0.28), int(HEIGHT * 0.48)],
            [int(WIDTH * 0.45), int(WIDTH * 0.2), int(HEIGHT * 0.3)],
            [int(WIDTH * 0.62), int(WIDTH * 0.25), int(HEIGHT * 0.42)],
            [int(WIDTH * 0.82), int(WIDTH * 0.25), int(HEIGHT * 0.33)],
        ]

        self.buttons = {}
        self.text_cache = {}

        # static background (sky + city) drawn ONCE, not every frame
        with self.canvas.before:
            Color(*SKY_BLUE)
            Rectangle(pos=(0, 0), size=(WIDTH, HEIGHT))
            self.draw_city()

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def play_beep(self):
        if self.snd_beep:
            self.snd_beep.play()

    def play_die(self):
        if self.snd_die:
            self.snd_die.play()

    def play_click(self):
        if self.snd_click:
            self.snd_click.play()

    def reset_game(self):
        self.bird_y = int(HEIGHT * 0.4)
        self.bird_movement = 0
        self.pipe_x = WIDTH
        self.score = 0
        self.pipe_height = random.randint(int(HEIGHT * 0.15), int(HEIGHT * 0.45))

    def reset_high_score_file(self):
        save_high_score(0)

    def draw_rect(self, color, x, y_top, w, h):
        Color(*color)
        Rectangle(pos=(x, HEIGHT - y_top - h), size=(w, h))

    def draw_circle(self, color, cx, cy_top, r):
        Color(*color)
        Ellipse(pos=(cx - r, HEIGHT - cy_top - r), size=(r * 2, r * 2))

    def draw_text(self, text, x_center, y_top_center, font_size, color=WHITE):
        key = (text, font_size)
        if key not in self.text_cache:
            label = CoreLabel(text=text, font_size=font_size)
            label.refresh()
            self.text_cache[key] = label.texture
        texture = self.text_cache[key]
        tw, th = texture.size
        Color(1, 1, 1, 1)
        Rectangle(
            texture=texture,
            pos=(x_center - tw / 2, HEIGHT - y_top_center - th / 2),
            size=(tw, th),
        )

    def draw_button(self, text, y_pos, w=200, h=50, is_reset=False, key=None):
        x = WIDTH // 2 - w // 2
        top_c = BTN_RESET_TOP if is_reset else BTN_TOP
        base_c = BTN_RESET_BASE if is_reset else BTN_BASE
        shadow_c = BTN_RESET_SHADOW if is_reset else BTN_SHADOW

        self.draw_rect(shadow_c, x, y_pos + 6, w, h)
        self.draw_rect(base_c, x, y_pos, w, h)
        self.draw_rect(top_c, x + 2, y_pos + 2, w - 4, h // 2)
        self.draw_text(text, x + w / 2, y_pos + h / 2, int(h * 0.4), WHITE)

        rect = (x, y_pos, w, h)
        if key:
            self.buttons[key] = rect
        return rect

    def point_in_rect(self, px, py, rect):
        x, y, w, h = rect
        return x <= px <= x + w and y <= py <= y + h

    def draw_bird(self, x, y):
        bw, bh = 38, 30
        bx, by = x - bw // 2, y - bh // 2
        self.draw_rect(MC_SHADOW, bx, by, bw, bh)
        self.draw_rect(MC_WHITE, bx, by, bw - 3, bh - 4)
        self.draw_rect(MC_HIGHLIGHT, bx + 2, by + 2, bw - 7, 6)
        self.draw_rect(MC_SHADOW, bx + 4, by + 12, 12, 10)
        self.draw_rect(MC_WHITE, bx + 2, by + 10, 12, 10)
        self.draw_rect(MC_HIGHLIGHT, bx + 2, by + 10, 12, 3)
        self.draw_rect(BLACK, bx + bw - 12, by + 4, 6, 8)
        self.draw_rect(WHITE, bx + bw - 10, by + 4, 2, 3)
        self.draw_rect(MC_YELLOW, bx + bw - 2, by + 10, 12, 8)
        self.draw_rect(MC_RED_DARK, bx + bw - 4, by + 18, 8, 7)
        self.draw_rect(MC_RED, bx + bw - 4, by + 18, 8, 5)

    def draw_city(self):
        ground_level = HEIGHT - 60
        for bx, bw, bh in self.buildings:
            by = ground_level - bh
            self.draw_rect(BUILDING_MAIN, bx, by, bw, bh)
            self.draw_rect(BUILDING_LIGHT, bx, by, 8, bh)
            self.draw_rect(BUILDING_SHADOW, bx + bw - 8, by, 8, bh)
            win_w, win_h = 8, 12
            for wx in range(bx + 14, bx + bw - 14, 18):
                for wy in range(by + 15, ground_level - 15, 25):
                    self.draw_rect(WINDOW_GLOW, wx, wy, win_w, win_h)

    def draw_pipe(self, x, height):
        self.draw_rect(PIPE_BASE, x, 0, self.pipe_width, height)
        self.draw_rect(PIPE_LIGHT, x + 4, 0, 10, height)
        self.draw_rect(PIPE_DARK, x + self.pipe_width - 14, 0, 14, height)

        lip_y = height - 28
        self.draw_rect(PIPE_BASE, x - 6, lip_y, self.pipe_width + 12, 28)
        self.draw_rect(PIPE_LIGHT, x - 2, lip_y + 2, 10, 24)
        self.draw_rect(PIPE_DARK, x + self.pipe_width - 10, lip_y, 12, 28)

        bottom_y = height + self.pipe_gap
        bottom_h = HEIGHT - bottom_y - 60
        self.draw_rect(PIPE_BASE, x, bottom_y, self.pipe_width, bottom_h)
        self.draw_rect(PIPE_LIGHT, x + 4, bottom_y, 10, bottom_h)
        self.draw_rect(PIPE_DARK, x + self.pipe_width - 14, bottom_y, 14, bottom_h)

        self.draw_rect(PIPE_BASE, x - 6, bottom_y, self.pipe_width + 12, 28)
        self.draw_rect(PIPE_LIGHT, x - 2, bottom_y + 2, 10, 24)
        self.draw_rect(PIPE_DARK, x + self.pipe_width - 10, bottom_y, 12, 28)

    def draw_ground(self):
        gy = HEIGHT - 60
        self.draw_rect(MC_DIRT, 0, gy, WIDTH, 60)
        self.draw_rect(MC_GRASS_TOP, 0, gy, WIDTH, 14)
        self.draw_rect(MC_GRASS_SIDE, 0, gy + 14, WIDTH, 4)

    def on_touch_down(self, touch):
        px, py = touch.x, HEIGHT - touch.y
        self.play_click()

        if self.game_state == "MENU":
            if self.point_in_rect(px, py, self.buttons.get("start", (0, 0, 0, 0))):
                self.reset_game()
                self.game_state = "PLAYING"
            elif self.point_in_rect(px, py, self.buttons.get("reset_hs", (0, 0, 0, 0))):
                self.reset_high_score_file()
                self.high_score = 0
            elif self.point_in_rect(px, py, self.buttons.get("credits", (0, 0, 0, 0))):
                self.game_state = "CREDITS"
            elif self.point_in_rect(px, py, self.buttons.get("exit", (0, 0, 0, 0))):
                App.get_running_app().stop()

        elif self.game_state == "CREDITS":
            if self.point_in_rect(px, py, self.buttons.get("back", (0, 0, 0, 0))):
                self.game_state = "MENU"

        elif self.game_state == "PLAYING":
            pause_rect = (WIDTH - 60, 20, 45, 45)
            if self.point_in_rect(px, py, pause_rect):
                self.game_state = "PAUSED"
            else:
                self.bird_movement = -HEIGHT * 0.012
                self.play_beep()

        elif self.game_state == "PAUSED":
            if self.point_in_rect(px, py, self.buttons.get("resume", (0, 0, 0, 0))):
                self.game_state = "PLAYING"
            elif self.point_in_rect(px, py, self.buttons.get("restart", (0, 0, 0, 0))):
                self.reset_game()
                self.game_state = "PLAYING"
            elif self.point_in_rect(px, py, self.buttons.get("main", (0, 0, 0, 0))):
                self.game_state = "MENU"

        elif self.game_state == "GAMEOVER":
            if self.point_in_rect(px, py, self.buttons.get("retry", (0, 0, 0, 0))):
                self.reset_game()
                self.game_state = "PLAYING"
            elif self.point_in_rect(px, py, self.buttons.get("menu", (0, 0, 0, 0))):
                self.game_state = "MENU"

    def update(self, dt):
        self.canvas.clear()
        with self.canvas:
            for cloud in self.clouds:
                cloud[0] -= 0.5
                if cloud[0] < -80:
                    cloud[0] = WIDTH + 30
                cx, cy = int(cloud[0]), cloud[1]
                self.draw_circle(CLOUD_SHADOW, cx + 2, cy + 3, 30)
                self.draw_circle(CLOUD_WHITE, cx, cy, 30)
                self.draw_circle(CLOUD_WHITE, cx + 25, cy - 12, 35)

            if self.game_state == "MENU":
                self.draw_text("FLAPPY BIRD 3D", WIDTH // 2, int(HEIGHT * 0.20), int(WIDTH * 0.09), WHITE)
                self.draw_text(f"BEST SCORE: {self.high_score}", WIDTH // 2, int(HEIGHT * 0.29), int(WIDTH * 0.04), WINDOW_GLOW)
                self.draw_button("START GAME", int(HEIGHT * 0.38), w=int(WIDTH * 0.65), key="start")
                self.draw_button("RESET HIGH SCORE", int(HEIGHT * 0.49), w=int(WIDTH * 0.65), is_reset=True, key="reset_hs")
                self.draw_button("CREDITS", int(HEIGHT * 0.60), w=int(WIDTH * 0.65), key="credits")
                self.draw_button("EXIT", int(HEIGHT * 0.71), w=int(WIDTH * 0.65), key="exit")

            elif self.game_state == "CREDITS":
                self.draw_text("CREDITS", WIDTH // 2, int(HEIGHT * 0.3), int(WIDTH * 0.07), WHITE)
                self.draw_text("Developed By:", WIDTH // 2, int(HEIGHT * 0.45), int(WIDTH * 0.04), WHITE)
                self.draw_text("TheSpookyRavager", WIDTH // 2, int(HEIGHT * 0.52), int(WIDTH * 0.07), BLACK)
                self.draw_button("BACK", int(HEIGHT * 0.7), w=int(WIDTH * 0.4), key="back")

            elif self.game_state == "PLAYING":
                self.bird_movement += self.gravity
                self.bird_y += self.bird_movement
                self.draw_bird(self.bird_x, self.bird_y)

                self.pipe_x -= WIDTH * 0.008
                if self.pipe_x < -self.pipe_width - 20:
                    self.pipe_x = WIDTH
                    self.pipe_height = random.randint(int(HEIGHT * 0.15), int(HEIGHT * 0.45))
                    self.score += 1
                    if self.score > self.high_score:
                        self.high_score = self.score
                        save_high_score(self.high_score)

                self.draw_pipe(self.pipe_x, self.pipe_height)

                bird_l, bird_r = self.bird_x - 18, self.bird_x + 18
                bird_t, bird_b = self.bird_y - 14, self.bird_y + 14
                top_pipe = (self.pipe_x, self.pipe_x + self.pipe_width, 0, self.pipe_height)
                bottom_pipe = (self.pipe_x, self.pipe_x + self.pipe_width, self.pipe_height + self.pipe_gap, HEIGHT)

                def overlap(pipe):
                    px1, px2, py1, py2 = pipe
                    return bird_r > px1 and bird_l < px2 and bird_b > py1 and bird_t < py2

                if self.bird_y <= 0 or self.bird_y >= HEIGHT - 60 or overlap(top_pipe) or overlap(bottom_pipe):
                    self.play_die()
                    self.game_state = "GAMEOVER"

                self.draw_text(f"Score: {self.score}", 90, 40, int(WIDTH * 0.045), WHITE)
                self.draw_text(f"Best: {self.high_score}", 90, 75, int(WIDTH * 0.045), WINDOW_GLOW)

                self.draw_rect(BTN_SHADOW, WIDTH - 60, 24, 45, 45)
                self.draw_rect(BTN_TOP, WIDTH - 60, 20, 45, 45)
                self.draw_rect(WHITE, WIDTH - 48, 30, 6, 25)
                self.draw_rect(WHITE, WIDTH - 36, 30, 6, 25)

            elif self.game_state == "PAUSED":
                self.draw_bird(self.bird_x, self.bird_y)
                self.draw_pipe(self.pipe_x, self.pipe_height)
                self.draw_text("GAME PAUSED", WIDTH // 2, int(HEIGHT * 0.3), int(WIDTH * 0.07), WHITE)
                self.draw_button("RESUME", int(HEIGHT * 0.45), w=int(WIDTH * 0.6), key="resume")
                self.draw_button("RESTART", int(HEIGHT * 0.55), w=int(WIDTH * 0.6), key="restart")
                self.draw_button("MAIN MENU", int(HEIGHT * 0.65), w=int(WIDTH * 0.6), key="main")

            elif self.game_state == "GAMEOVER":
                self.draw_text("GAME OVER", WIDTH // 2, int(HEIGHT * 0.32), int(WIDTH * 0.07), WHITE)
                self.draw_text(f"Score: {self.score}", WIDTH // 2, int(HEIGHT * 0.40), int(WIDTH * 0.045), WHITE)
                self.draw_text(f"High Score: {self.high_score}", WIDTH // 2, int(HEIGHT * 0.46), int(WIDTH * 0.045), WINDOW_GLOW)
                self.draw_button("RETRY", int(HEIGHT * 0.58), w=int(WIDTH * 0.5), key="retry")
                self.draw_button("MENU", int(HEIGHT * 0.68), w=int(WIDTH * 0.5), key="menu")

            self.draw_ground()


class FlappyBird3DApp(App):
    def build(self):
        return Game()


if __name__ == "__main__":
    FlappyBird3DApp().run()
