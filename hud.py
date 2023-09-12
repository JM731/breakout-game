from turtle import Turtle
from wrapper import check_running
MENU_TEXT = ["BREAKOUT",
             "Press → or ← to move paddle",
             "Press Enter to start",
             "Press R to restart",
             "Press Esc to quit",
             "Press M to return to menu"
             ]
GAME_TEXT = ["Lives: ", "Score: ", "GAME OVER", "Press Enter to continue"]
TITLE_FONT = ("Small Fonts", 72, 'normal')
MENU_FONT = ("Cascadia Code", 20, 'normal')
SCORE_FONT = ("Cascadia Code", 20, 'normal')
GAME_OVER_FONT = ("Small Fonts", 100, 'normal')
MENU_FONTS = [TITLE_FONT if i == 0 else MENU_FONT for i in range(6)]
GAME_FONTS = [GAME_OVER_FONT if i == 2 else SCORE_FONT for i in range(4)]


def game_hud_pos(half_width, half_height):
    return [(-0.85 * half_width, 0.85 * half_height),
            (0.85 * half_width, 0.85 * half_height),
            (0, 0),
            (0, -0.3 * half_height)]


class HUD:
    def __init__(self, game_dictionary, width, height):
        self.game_dictionary = game_dictionary
        self.lives = 4
        self.score = 0
        self.half_width = width/2
        self.half_height = height/2
        self.menu = []
        self.menu_is_shown = False
        self.game_hud_is_shown = False
        self.game_HUD = []

        self.create_menu()
        self.create_game_hud()

    def create_menu(self):
        y_pos = 0.5 * self.half_height
        for i in range(6):
            item = Turtle()
            item.pu()
            item.hideturtle()
            item.color('black')
            if i > 0:
                y_pos = 0.2 * (2 - i) * self.half_height
            item.goto(0, y_pos)
            self.menu.append(item)

    def create_game_hud(self):
        pos_list = game_hud_pos(self.half_width, self.half_height)
        for i in range(4):
            item = Turtle()
            item.pu()
            item.hideturtle()
            item.color('black')
            item.goto(pos_list[i])
            self.game_HUD.append(item)

    @check_running
    def show_menu(self):
        for index, item in enumerate(self.menu):
            item.write(MENU_TEXT[index], False, align='center', font=MENU_FONTS[index])

    @check_running
    def hide_menu(self):
        for item in self.menu:
            item.clear()

    @check_running
    def update_game_hud(self):
        for index, item in enumerate(self.game_HUD):
            if index == 2 or index == 3:
                return
            item.clear()
            num = self.lives if index == 0 else self.score
            item.write(f"{GAME_TEXT[index]}{num}", False, align='center', font=GAME_FONTS[index])

    @check_running
    def hide_game_hud(self):
        if self.game_hud_is_shown:
            for item in self.game_HUD:
                item.clear()
            self.game_hud_is_shown = False

    @check_running
    def show_game_over(self):
        for index in range(2, 4):
            self.game_HUD[index].write(GAME_TEXT[index], False, align='center', font=GAME_FONTS[index])

    def is_menu_shown(self):
        return self.menu_is_shown

    def reset_values(self):
        self.lives = 4
        self.score = 0

    def decrease_lives(self):
        self.lives -= 1

    def increase_score(self):
        self.score += 1

    def is_game_over(self):
        return self.lives == 0

    def is_max_score(self):
        return self.score == 42
