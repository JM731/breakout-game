from turtle import Screen
from paddle import Paddle
from wall import Wall
from ball import Ball
from hud import HUD
import pygame
from functools import partial

pygame.init()
bounce_sound = pygame.mixer.Sound("beep_sound.wav")

WIDTH, HEIGHT = 1200, 700
PADDLE_Y_POS = -int(0.8 * HEIGHT/2)
game_dictionary = {
    "game": True,
    "game_started": False,
    "game_over": False,
    "is_moving_right": False,
    "is_moving_left": False
}


def play_beep():
    bounce_sound.play(maxtime=50)


def start():
    if not game_dictionary["game_started"]:
        if game_dictionary["game_over"]:
            game_dictionary["game_over"] = False
        else:
            toggle_game_key("game_started", True)
            reset()


def reset():
    if game_dictionary["game_started"]:
        wall.reset_wall()
        ball.on_game_reset()
        paddle.reset_pos()
        hud.reset_values()


def toggle_game_key(key, enabled):
    game_dictionary[key] = enabled


screen = Screen()
screen.setup(WIDTH, HEIGHT)
screen.tracer(0)
screen.listen()
screen.onkeypress(partial(toggle_game_key, "is_moving_right", True), "Right")
screen.onkeypress(partial(toggle_game_key, "is_moving_left", True), "Left")
screen.onkeyrelease(partial(toggle_game_key, "is_moving_right", False), "Right")
screen.onkeyrelease(partial(toggle_game_key, "is_moving_left", False), "Left")
screen.onkeypress(partial(toggle_game_key, "game", False), "Escape")
screen.onkeypress(start, "Return")
screen.onkeypress(partial(toggle_game_key, "game_started", False), "m")
screen.onkeypress(reset, "r")

canvas = screen.getcanvas()
root = canvas.winfo_toplevel()
root.protocol("WM_DELETE_WINDOW", partial(toggle_game_key, "game", False))

hud = HUD(game_dictionary, WIDTH, HEIGHT)
paddle = Paddle(game_dictionary, PADDLE_Y_POS, WIDTH)
ball = Ball(game_dictionary)
wall = Wall(game_dictionary, 0, WIDTH)

clock = pygame.time.Clock()
desired_fps = 120

while game_dictionary["game"]:
    for event in pygame.event.get(pump=False):
        if event.type == pygame.QUIT:
            game_dictionary["game"] = False
        pygame.event.pump()
    if not hud.is_menu_shown() and not game_dictionary["game_started"] and not game_dictionary["game_over"]:
        ball.hide_ball()
        paddle.hide_paddle()
        wall.hide_wall()
        hud.show_menu()
        hud.menu_is_shown = True
        hud.hide_game_hud()

    if game_dictionary["game_started"]:
        if hud.is_menu_shown():
            hud.hide_menu()
            hud.menu_is_shown = False
            hud.game_hud_is_shown = True
            ball.showturtle()
            paddle.showturtle()
            wall.reset_wall()

        ball.move()
        if ball.out_of_bounds(HEIGHT):
            ball.reset_pos()
            paddle.reset_pos()
            hud.decrease_lives()

        if hud.is_game_over():
            wall.hide_wall()
            paddle.hide_paddle()
            ball.hide_ball()
            hud.show_game_over()
            toggle_game_key("game_started", False)
            toggle_game_key("game_over", True)
        else:
            if ball.wall_ceiling_bounce(WIDTH, HEIGHT):
                play_beep()
            if ball.collision_paddle(paddle):
                play_beep()
            if ball.is_collision_bricks(wall):
                play_beep()
                hud.increase_score()
                if hud.is_max_score():
                    toggle_game_key("game_started", False)
            if game_dictionary["is_moving_right"]:
                paddle.move_right()
            if game_dictionary["is_moving_left"]:
                paddle.move_left()
        hud.update_game_hud()
    if not game_dictionary["game"]:
        screen.bye()
        break
    else:
        screen.update()
        clock.tick(desired_fps)

pygame.quit()
