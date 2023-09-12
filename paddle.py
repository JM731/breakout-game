from turtle import Turtle, Vec2D
from wrapper import check_running
PADDLE_VELOCITY = Vec2D(7, 0)


class Paddle(Turtle):
    def __init__(self, game_dictionary, y_pos, width):
        super().__init__()
        self.game_dictionary = game_dictionary
        self.y_pos = y_pos
        self.paddle_velocity = PADDLE_VELOCITY
        self.shape('square')
        self.stretch_len = 7
        self.paddle_bounds = width/2 - self.stretch_len * 10
        self.shapesize(stretch_wid=0.8, stretch_len=self.stretch_len)
        self.pu()
        self.reset_pos()
        self.hide_paddle()

    @check_running
    def reset_pos(self):
        self.goto(0, self.y_pos)

    @check_running
    def move_right(self):
        if not self.pos()[0] > self.paddle_bounds:
            self.goto(self.pos() + self.paddle_velocity)

    @check_running
    def move_left(self):
        if not self.pos()[0] < -self.paddle_bounds:
            self.goto(self.pos() - self.paddle_velocity)

    @check_running
    def hide_paddle(self):
        if self.isvisible():
            self.hideturtle()
