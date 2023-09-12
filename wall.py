from turtle import Turtle
import random
from wrapper import check_running
COLORS = ["red", "green", "blue"]


class Wall:
    def __init__(self, game_dictionary, init_y_pos, width):
        self.game_dictionary = game_dictionary
        self.width = width
        self.y_min = init_y_pos
        self.x_pos = -int(width/2)
        self.bricks = []
        self.gap = 3
        self.y_max = self.create_wall()
        self.hide_wall()

    def create_wall(self):
        # 3 layers of bricks, 14 bricks each
        num_of_bricks = 14
        y_pos = self.y_min
        for j in range(3):
            x_pos = self.x_pos
            width = self.width
            for i in range(1, num_of_bricks + 1):
                brick = Turtle(shape='square')
                brick.pu()
                brick.color(COLORS[j])
                # the last brick of each layer gets the remaining horizontal space
                if i % 14 == 0:
                    stretch_int = (width / 2) - self.gap
                else:
                    stretch_int = random.randrange(38, 46, 2)
                brick.shapesize(stretch_wid=3, stretch_len=stretch_int / 10)
                x_pos += self.gap + stretch_int
                brick.goto(x_pos, y_pos)
                self.bricks.append(brick)
                x_pos += stretch_int
                width -= self.gap + 2 * stretch_int
            y_pos += 63
        return y_pos

    @check_running
    def hide_wall(self):
        for brick in self.bricks:
            if brick.isvisible():
                brick.hideturtle()

    @check_running
    def reset_wall(self):
        for brick in self.bricks:
            if not brick.isvisible():
                brick.showturtle()
