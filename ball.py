from turtle import Turtle, Vec2D
from wall import Wall
from paddle import Paddle
import random
import math
from wrapper import check_running
DETECTOR_VECS = [Vec2D(9, 0).rotate(i * 90) for i in range(4)]
INITIAL_POSITION = Vec2D(0, -250)
INITIAL_SPEED = 3


def get_initial_velocity(speed):
    return Vec2D(speed, 0).rotate(random.randrange(45, 225, 90))


def get_obj_dims(obj):
    obj_pos = obj.pos()
    x_obj, y_obj = obj_pos
    obj_half_wid, obj_half_len, _ = [10 * x for x in obj.shapesize()]
    lower_x, upper_x = x_obj - obj_half_len, x_obj + obj_half_len
    lower_y, upper_y = y_obj - obj_half_wid, y_obj + obj_half_wid
    return lower_x, upper_x, lower_y, upper_y, obj_pos, obj_half_wid


class Ball(Turtle):
    def __init__(self, game_dictionary):
        super().__init__()
        self.game_dictionary = game_dictionary
        self.shape('circle')
        self.pu()
        self.collision_dictionary = {
            'ceiling': True,
            'right_wall': True,
            'left_wall': True,
            'paddle': True,
        }
        self.destroyed_bricks = 0
        self.speed = INITIAL_SPEED
        self.velocity = get_initial_velocity(self.speed)
        self.color("green")
        self.detectors = []
        for _ in range(len(DETECTOR_VECS)):
            detector = Turtle(shape='circle')
            detector.pu()
            detector.hideturtle()
            self.detectors.append(detector)
        self.reset_pos()
        self.hide_ball()

    @check_running
    def move(self):
        self.goto(self.pos() + self.velocity)
        for detector in self.detectors:
            detector.goto(detector.pos() + self.velocity)

    def is_collision_bricks(self, wall: Wall):
        y = self.pos()[1]
        if wall.y_min - 50 <= y <= wall.y_max + 50:
            bricks = wall.bricks
            close_bricks = [brick for brick in bricks if self.distance(brick.pos()) < 100 and brick.isvisible()]
            for brick in close_bricks:
                bounced = self.bounce_obj(brick)
                if bounced:
                    self.hide_brick(brick)
                    self.change_collision()
                    self.destroyed_bricks += 1
                    self.change_speed()
                    return True
        return False

    @check_running
    def hide_brick(self, brick):
        brick.hideturtle()

    def collision_paddle(self, paddle: Paddle):
        # only the lower (3) detector is relevant for this collision
        if self.is_collision_allowed('paddle'):
            lower_x, upper_x, lower_y, upper_y, _, _ = get_obj_dims(paddle)
            x, y = self.detectors[3].pos()
            if lower_x - 5 < x < upper_x + 5 and lower_y < y < upper_y:
                self.h_bounce()
                self.change_collision('paddle')
                return True
        return False

    def bounce_obj(self, obj):
        lower_x, upper_x, lower_y, upper_y, obj_pos, obj_half_wid = get_obj_dims(obj)
        for detector in self.detectors:
            x, y = detector.pos()
            # check if detector is within the object's region
            if lower_x < x < upper_x and lower_y < y < upper_y:
                distance = self.pos() - obj_pos
                y_comp = abs(distance[1])
                # horizontal surface bouncing (happens when the ball's y_pos exceeds the objects half width)
                if y_comp > obj_half_wid:
                    self.h_bounce()
                # vertical surface bouncing
                else:
                    self.v_bounce()
                return True
        return False

    def wall_ceiling_bounce(self, width, height):
        bounced = False
        # upper detector for ceiling
        if self.detectors[1].pos()[1] > height/2 and self.is_collision_allowed('ceiling'):
            self.h_bounce()
            self.change_collision('ceiling')
            bounced = True
        # side detectors for walls
        if self.detectors[0].pos()[0] > width/2 and self.is_collision_allowed('right_wall'):
            self.v_bounce()
            self.change_collision('right_wall')
            bounced = True
        elif self.detectors[2].pos()[0] < -width/2 and self.is_collision_allowed('left_wall'):
            self.v_bounce()
            self.change_collision('left_wall')
            bounced = True
        return bounced

    def change_collision(self, obj=None):
        for key in self.collision_dictionary:
            if key == obj:
                self.collision_dictionary[key] = False
            else:
                self.collision_dictionary[key] = True

    def is_collision_allowed(self, obj):
        return self.collision_dictionary[obj]

    def h_bounce(self):
        self.velocity = Vec2D(self.velocity[0], -self.velocity[1])
        self.rotate_velocity()

    def v_bounce(self):
        self.velocity = Vec2D(-self.velocity[0], self.velocity[1])
        self.rotate_velocity()

    def rotate_velocity(self):
        self.velocity = self.velocity.rotate(random.randrange(-2, 4, 2))

    def out_of_bounds(self, height):
        if self.pos()[1] < -height/2 + 20:
            return True

    @check_running
    def reset_pos(self):
        self.goto(INITIAL_POSITION)
        self.velocity = get_initial_velocity(self.speed)
        for index, detector in enumerate(self.detectors):
            detector.goto(INITIAL_POSITION + DETECTOR_VECS[index])

    def change_speed(self):
        destroyed_bricks = self.destroyed_bricks
        if destroyed_bricks == 14 or destroyed_bricks == 28:
            self.speed = INITIAL_SPEED + destroyed_bricks/7
            current_angle = math.degrees(math.atan2(self.velocity[1], self.velocity[0]))
            self.velocity = Vec2D(self.speed, 0).rotate(current_angle)

    @check_running
    def hide_ball(self):
        if self.isvisible():
            self.hideturtle()

    @check_running
    def on_game_reset(self):
        self.destroyed_bricks = 0
        self.speed = INITIAL_SPEED
        self.reset_pos()
