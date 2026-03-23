#! /usr/local/bin/python3

import random
import math
import numpy
import argparse
import pyglet
import arcade
import logging
logger = logging.getLogger("Bouncing")

def reflect_vector(incident_vector, normal_vector):
    n = normal_vector / numpy.linalg.norm(normal_vector)
    v_dot_n = numpy.dot(incident_vector, n)
    return incident_vector - 2 * v_dot_n * n

def sprite_reflect(moving_sprite, block_sprite):
    incident_vec = numpy.array([moving_sprite.change_x, moving_sprite.change_y])
    normal_vec = block_sprite.normal_vector(moving_sprite)
    if normal_vec is None:
        logger.warning("invalid normal vec:")
        return
    refect_vec = reflect_vector(incident_vec, normal_vec)
    moving_sprite.change_x, moving_sprite.change_y = refect_vec[0], refect_vec[1]
    logger.debug(f'sprite_reflect: ({incident_vec[0]:.2f},{incident_vec[1]:.2f}) -->  ({moving_sprite.change_x:.2f},{moving_sprite.change_y:.2f})')
    return

def rotate_vector_2d(vector, angle_degrees):
    """
    Rotates a 2D vector around the origin counter-clockwise.
    """
    # print("rotate vecotr by ", angle_degrees, "degree, counter-colockwise")
    angle_radians = math.radians(angle_degrees)
    # Rotation matrix
    R = numpy.array([[numpy.cos(angle_radians), -numpy.sin(angle_radians)],
                  [numpy.sin(angle_radians), numpy.cos(angle_radians)]])
    # Matrix multiplication
    rotated_vector = R @ vector
    return rotated_vector

def str_angle(angle):
    degrees = math.degrees(angle)
    return f'{angle:.2f}({degrees:.2f})'

def angle_between_pos(pos1:numpy.array, pos2:numpy.array):
    p = numpy.subtract(pos2 , pos1)
    x, y = p[0], p[1]
    radian =  math.atan2(y, x)
    # print(f'angle_between_pos: pos1:({pos1[0]:.2f},{pos1[1]:.2f}), pos2:({pos2[0]:.2f},{pos2[1]:.2f}), diff:({x:.2f},{y:.2f}), angle={str_angle(radian)}')
    return radian

class Pos(pyglet.math.Vec2):
    pass

BACK_GROUND_COLOR=arcade.csscolor.BLACK
class Data:
    game_on          = False
    window_width     = 1024
    window_height    = window_width
    window_title     = "Bouncing Ball"
    _view_list       = []
    _view_list_index = 0
    bar_width        = 100
    bar_height       = 10
    bar_pos          = Pos(window_width/2, 50)
    bar_speed        = 15
    bar_hit_score    = 3
    ball_radius      = 10
    ball_pos         = Pos(window_width/2, bar_pos.y+(bar_height/2)+ball_radius)
    ball_init_speed  = 5
    ball_max_speed   = 20
    ball_speed_inc   = 1
    border_gap       = 30
    wall_width       = 10
    score            = 0
    brick_width      = 40
    brick_height     = bar_height
    brick_hit_score  = 1
    def __init__(self):
        self._ball_speed = Data.ball_init_speed
        return
    def append_view(self, view):
        self._view_list.append(view)
        return
    def current_view(self):
        if self._view_list and self._view_list_index < len(self._view_list):
            return self._view_list[self._view_list_index]
        return None
    def last_view(self):
        if self._view_list:
            return self._view_list[-1]
        return None
    def next_view(self):
        self._view_list_index += 1
        return self.current_view()
    def inc_ball_speed(self):
        old_speed = self._ball_speed
        self._ball_speed += Data.ball_speed_inc
        if self._ball_speed > Data.ball_max_speed:
            self._ball_speed = Data.ball_max_speed
        logger.info(f'speed: {old_speed} -> {data._ball_speed}')
    def get_ball_speed(self):
        return self._ball_speed
    def start_over(self):
        self._ball_speed = Data.ball_init_speed
        self.score = 0
        self._view_list_index = 1
        self.game_on = True
        return

class Wall(arcade.SpriteSolidColor):
    stop_game = False
    def __init__(self, width, height, pos, normal_vec: numpy.array, wall_color, stop_game = False):
        super().__init__(width, height, color=wall_color)
        self.center_x, self.center_y = pos.x, pos.y
        self._normal_vec = normal_vec
        self.stop_game = stop_game
        if self.stop_game:
            self.hit_sound = arcade.load_sound( ":resources:/sounds/gameover3.wav")
        else:
            self.hit_sound = arcade.load_sound( ":resources:/sounds/hurt2.wav")
        return
    def hit(self):
        self.hit_sound.play()
        return 0
    def normal_vector(self, Ball) -> numpy.array:
        return self._normal_vec

class Border(arcade.SpriteList):
    regular_wall_color = arcade.color.BLACK_OLIVE
    bottom_wall_color = BACK_GROUND_COLOR
    def __init__(self):
        super().__init__()
        # left wall
        width, height = data.wall_width, data.window_height-2*data.border_gap
        x, y = data.border_gap + data.wall_width/2, data.window_height/2
        wall = Wall(width, height, Pos(x,y), numpy.array([1,0]), Border.regular_wall_color)
        wall.min_x = True
        super().append(wall)
        # ceiling
        width, height = data.window_width-2*data.border_gap, data.wall_width
        x, y = data.window_width/2, data.window_height- data.border_gap -data.wall_width/2
        wall = Wall(width, height, Pos(x,y), numpy.array([0, -1]), Border.regular_wall_color)
        super().append(wall)
        # right wall
        width, height = data.wall_width, data.window_height-2*data.border_gap
        x, y = data.window_width-data.border_gap-data.wall_width/2, data.window_height/2
        wall = Wall(width, height, Pos(x,y), numpy.array([-1, 0]), Border.regular_wall_color)
        wall.max_x = True
        super().append(wall)
        # bottom wall
        width, height = data.window_width-2*data.border_gap, data.wall_width
        x, y = data.window_width/2, data.border_gap +data.wall_width/2
        wall = Wall(width, height, Pos(x,y), numpy.array([0, 1]), Border.bottom_wall_color, stop_game = True)
        super().append(wall)
        return

class Brick(arcade.SpriteSolidColor):
    LEFT_SIDE = "left-side"
    RIGHT_SIDE = "right-side"
    TOP_SIDE = "top-side"
    BOTTOM_SIDE = "bottom-side"
    def _angle_to_center(self, point):
        return angle_between_pos(point, self.center_point)

    def __init__(self, pos, width=Data.brick_width, height= Data.brick_height, disappear_by_hit=True, brick_color=arcade.color.CADMIUM_ORANGE):
        super().__init__(width, height, color=brick_color)
        # print("brick: x=", pos.x, "y=", pos.y)
        self.disappear_by_hit = disappear_by_hit
        self.center_x, self.center_y = pos.x, pos.y
        self.hit_sound = arcade.load_sound( ":resources:/sounds/hurt3.wav")
        self._normal_vector_dict = {
            Brick.LEFT_SIDE:   numpy.array([-1, 0]),
            Brick.RIGHT_SIDE:  numpy.array([1, 0]),
            Brick.TOP_SIDE:    numpy.array([0, 1]),
            Brick.BOTTOM_SIDE: numpy.array([0, -1]),
        }
        self.center_point = numpy.array([self.center_x, self.center_y])
        left_x = pos.x - width/2
        right_x = pos.x + width/2
        top_y = pos.y + height/2
        bottom_y = pos.y - height/2
        self.top_left_point = numpy.array([left_x, top_y])
        self.top_left_angle = self._angle_to_center(self.top_left_point)

        self.bottom_left_point = numpy.array([left_x, bottom_y])
        self.bottom_left_angle = self._angle_to_center(self.bottom_left_point)

        self.top_right_point = numpy.array([right_x, top_y])
        self.top_right_angle = self._angle_to_center(self.top_right_point)

        self.bottom_right_point = numpy.array([right_x, bottom_y])
        self.bottom_right_angle = self._angle_to_center(self.bottom_right_point)
        # logger.debug(f'cornor: left-top={str_angle(self.top_left_angle)}, left-bot={str_angle(self.bottom_left_angle)}, right-bot={str_angle(self.bottom_right_angle)},  right-top={str_angle(self.top_right_angle)}')
        return
    def hit(self):
        self.hit_sound.play()
        return 1
    def _get_side(self, ball:Ball, ball_angle):
        if ball.change_x == 0 and ball.change_y == 0:
            return ""
        if ball.change_x == 0:
            if ball.change_y < 0:
                return Brick.TOP_SIDE
            else:
                return Brick.BOTTOM_SIDE
        if ball.change_y == 0:
            if ball.change_x < 0:
                return Brick.RIGHT_SIDE
            else:
                return Brick.LEFT_SIDE
        if ball.change_x <= 0:
            if ball.change_y < 0:
                if ball_angle > 0:
                    ball_angle -= math.pi
                if ball_angle >= self.top_right_angle:
                    return Brick.TOP_SIDE
                else:
                    return Brick.RIGHT_SIDE
            else:
                if ball_angle < 0:
                    ball_angle += math.pi
                if ball_angle >= self.bottom_right_angle:
                    return Brick.RIGHT_SIDE
                else:
                    return Brick.BOTTOM_SIDE
        else:
            if ball.change_y < 0:
                if ball_angle > 0:
                    ball_angle -= math.pi
                if ball_angle >= self.top_left_angle:
                    return Brick.LEFT_SIDE
                else:
                    return Brick.TOP_SIDE
            else:
                if ball_angle < 0:
                    ball_angle += math.pi
                if ball_angle >= self.bottom_left_angle:
                    return Brick.BOTTOM_SIDE
                else:
                    return Brick.LEFT_SIDE
    def normal_vector(self, ball:Ball) -> numpy.array:
        ball_point = numpy.array([ball.center_x, ball.center_y])
        ball_angle = self._angle_to_center(ball_point)
        side = self._get_side(ball, ball_angle)
        logger.debug(f'ball change_x={ball.change_x:.2f} change_y={ball.change_y:.2f} angle={str_angle(ball_angle)} SIDE={side} cornor: left-top={str_angle(self.top_left_angle)}, left-bot={str_angle(self.bottom_left_angle)}, right-bot={str_angle(self.bottom_right_angle)},  right-top={str_angle(self.top_right_angle)}')
        if side:
            return self._normal_vector_dict[side]
        return None
    def pos_str(self):
        str = f'brick_pos: {self.center_x:.2f},{self.center_y:.2f}'
        str += f' x: {self.center_x-self.width:.2f}->{self.center_x+self.width:.2f}'
        str += f' y: {self.center_y-self.height:.2f}->{self.center_y+self.height:.2f}'
        return str

class MetalBrick(Brick):
    def __init__(self, pos, width=Data.brick_width, height= Data.brick_height, disappear_by_hit=False, brick_color=arcade.color.SILVER):
        super().__init__(pos, width, height, disappear_by_hit, brick_color)
        return

class Barrier(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        for i in range(0, 12):
            x = 2*data.border_gap+i*2*Data.brick_width
            for j in range(0, 10):
                y = Data.window_height*14/15 - j*(2*Data.brick_height)
                brick = Brick(Pos(x,y))
                super().append(brick)
        for i in range(0, 8):
            x = 2*data.border_gap+i*3*Data.brick_width
            for j in range(10, 11):
                y = Data.window_height*14/15 - j*(2*Data.brick_height)
                brick = MetalBrick(Pos(x,y))
                super().append(brick)
        return

class Ball(arcade.SpriteCircle):
    def _update_x_y(self, angle):
        self.change_x = data.get_ball_speed() * math.cos(angle)
        self.change_y = data.get_ball_speed() * math.sin(angle)
        return
    def _set_angle(self):
        random_list = { 0:(math.pi/4, math.pi*3/8), 1:(math.pi*5/8, math.pi*6/8) }
        rand_i = random.randint(0,1)
        rand_min, rand_max = random_list[rand_i]
        angle = random.uniform(rand_min, rand_max)
        self._update_x_y(angle)
        return
    def __init__(self):
        super().__init__(data.ball_radius, arcade.color.RED)
        self.center_x, self.center_y = data.ball_pos.x, data.ball_pos.y
        return
    def reset(self, angle=None, pos=None):
        if angle is None:
            self._set_angle()
        else:
            self._update_x_y(angle)
        if pos is None:
            self.center_x, self.center_y = data.ball_pos.x, data.ball_pos.y
        else:
            self.center_x, self.center_y = pos.x, pos.y
        return
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        return
    def pos_str(self):
        str = f'ball_pos : {self.center_x:.2f},{self.center_y:.2f}'
        str += f' x: {self.center_x-data.ball_radius:.2f}->{self.center_x+data.ball_radius:.2f}'
        str += f' y: {self.center_y-data.ball_radius:.2f}->{self.center_y+data.ball_radius:.2f}'
        return str
    def update_speed(self):
        angle = math.atan2(self.change_y, self.change_x)
        self._update_x_y(angle)
        return

class Bar(arcade.SpriteSolidColor):
    hit_sound = arcade.load_sound( ":resources:/sounds/hurt5.wav")
    def __init__(self):
        super().__init__(data.bar_width, data.bar_height, color=arcade.color.YELLOW)
        self.center_x, self.center_y = data.bar_pos.x, data.bar_pos.y
        self.left_pressed  = False
        self.right_pressed = False
        self.stop_game = False
        self._normal_vec = numpy.array([0,1])
        self.min_x = data.border_gap+data.wall_width+(data.bar_width/2)
        self.max_x = data.window_width-self.min_x
        self.x_array = []
        self.x_sum = 0
        return
    def reset(self):
        pass
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        self._update_speed()
        return
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        self._update_speed()
        return
    def _update_speed(self):
        self.change_x = 0
        if self.left_pressed and not self.right_pressed:
            self.change_x = -data.bar_speed
        if self.right_pressed and not self.left_pressed:
            self.change_x = data.bar_speed
        return
    def hit(self):
        self.hit_sound.play()
        return Data.bar_hit_score
    def _pos_percent_of_bar(self, ball:Ball) -> int:
        return (ball.center_x-self.left)/(self.right-self.left)
    def normal_vector(self, ball:Ball) -> numpy.array:
        percent=self._pos_percent_of_bar(ball)
        theta_min, theta_max = -10, 10
        theta = -(theta_min + (theta_max-theta_min)*percent)
        logger.debug("percent=", percent, "rotate vecotr by ", theta, "degree, counter-colockwise")
        return rotate_vector_2d(self._normal_vec, theta)
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        if self.center_x < self.min_x:
            self.center_x = self.min_x
        elif self.center_x > self.max_x:
            self.center_x = self.max_x
        self.center_y += self.change_y
        return

class GeneralView(arcade.View):
    def __init__(self):
        super().__init__()
        return
    def setup(self):
        self.border = Border()
        self.bar= Bar()
        self.ball= Ball()
        self.ball.reset()
        self.moving_list = arcade.SpriteList()
        self.moving_list.append(self.ball)
        self.moving_list.append(self.bar)
        self.score_text = arcade.Text(f"Score: {data.score}", 10,  data.window_height - 20, arcade.color.WHITE, 14)
        self.speed_text = arcade.Text(f"Speed: {data.get_ball_speed()}", 120, data.window_height - 20, arcade.color.WHITE, 14)
        return
    def on_draw(self):
        self.clear()
        self.border.draw()
        self.moving_list.draw()
        self.score_text.draw()
        self.speed_text.draw()
        return

class GameStartView(GeneralView):
    def __init__(self):
        super().__init__()
        return
    def setup(self):
        super().setup()
        self.game_start_text = arcade.Text(f"Bouncing Ball", (data.window_width/2), data.window_height/2 + 40, anchor_x="center", anchor_y="center", color=arcade.color.YELLOW, font_size=46, bold=True, italic=True )
        self.press_space_text = arcade.Text(f"press <SPACE> to start", (data.window_width/2), data.window_height/2 - 40, anchor_x="center", anchor_y="center", color=arcade.color.YELLOW_ORANGE, font_size=20, bold=False, italic=False )
        return
    def on_draw(self):
        super().on_draw()
        self.game_start_text.draw()
        self.press_space_text.draw()
        return
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
           self.window.game_start()
        return
    def on_key_release(self, key, modifiers):
        return
class GameOverView(GeneralView):
    def __init__(self):
        super().__init__()
        return
    def setup(self):
        super().setup()
        self.game_over_text = arcade.Text(f"Game Over", (data.window_width/2), data.window_height/2 + 40, anchor_x="center", anchor_y="center", color=arcade.color.YELLOW, font_size=46, bold=True, italic=True )
        self.press_space_text = arcade.Text(f"press <SPACE> to restart", (data.window_width/2), data.window_height/2 - 40, anchor_x="center", anchor_y="center", color=arcade.color.YELLOW_ORANGE, font_size=20, bold=False, italic=False )
        return
    def on_draw(self):
        # super().on_draw() #just keep the last screen
        self.game_over_text.draw()
        self.press_space_text.draw()
        return
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
           self.window.game_start()
        return

def debug_sprite(s, name):
    logger.debug(f'{name} pos: ({s.center_x:.2f}, {s.center_y:.2f}), edge: ({s.max_y},{s.min_x},{s.min_y},{s.max_x})')

class GameTestView(GeneralView):
    def __init__(self):
        super().__init__()
        return
    def setup(self, _arg_ball_pos):
        super().setup()
        brick = MetalBrick(Pos(400,400), width=80, height=80)
        logger.debug(brick.pos_str())
        self.ball_collision_list = arcade.SpriteList()
        for s in self.border:
            self.ball_collision_list.append(s)
        self.ball_collision_list.append(self.bar)
        self._bricks = arcade.SpriteList()
        self._bricks.append(brick)
        ball_pos = Pos(_arg_ball_pos[0],_arg_ball_pos[1])
        ball_angle = angle_between_pos(numpy.array([ball_pos.x, ball_pos.y]), numpy.array([brick.center_x, brick.center_y]))
        self.ball.reset(ball_angle, ball_pos)
        logger.debug(self.ball.pos_str())
        self.last_hit = None
        return
    def on_draw(self):
        super().on_draw() #just keep the last screen
        self._bricks.draw()
        return
    def on_update(self, delta_time):
        collision_list = arcade.SpriteList()
        for c in self._bricks:
            if self.last_hit is None or c != self.last_hit:
                collision_list.append(c)
        collision = arcade.check_for_collision_with_list(self.ball, collision_list)
        for c in collision:
            logger.debug(f"hit: {self.ball.pos_str()} {c.pos_str()}")
            sprite_reflect(self.ball, c)
            c.hit()
            if isinstance(c, Brick) and c.disappear_by_hit:
                self._bricks.remove(c)
            else:
                self.last_hit = c
        collision = arcade.check_for_collision_with_list(self.ball, self.ball_collision_list)
        for c in collision:
            self.last_hit = None
            c.hit()
            sprite_reflect(self.ball, c)
        self.bar.update(delta_time)
        if data.game_on:
            self.ball.update(delta_time)
            logger.debug(f"update: {self.ball.pos_str()}")
        return
    def on_key_press(self, key, modifiers):
        global data
        if key == arcade.key.SPACE:
            logger.info("TestView: start")
            data.game_on = True
        self.bar.on_key_press(key, modifiers)
        return
    def on_key_release(self, key, modifiers):
        self.bar.on_key_release(key, modifiers)
        return

class BouncingView(GeneralView):
    def __init__(self):
        super().__init__()
        return
    def setup(self):
        super().setup()
        self._barrier = Barrier()
        self.ball_collision_list = arcade.SpriteList() 
        for s in self.border:
            self.ball_collision_list.append(s)
        self.ball_collision_list.append(self.bar)
        self.last_hit = None
        return
    def on_draw(self):
        super().on_draw()
        self._barrier.draw()
    def on_update(self, delta_time):
        global data
        if data.game_on:
            collision_list = arcade.SpriteList()
            for c in self._barrier:
                if self.last_hit is None or c != self.last_hit:
                    collision_list.append(c)
            collision = arcade.check_for_collision_with_list(self.ball, collision_list)
            for c in collision:
                sprite_reflect(self.ball, c)
                data.score += c.hit()
                if isinstance(c, Brick) and c.disappear_by_hit:
                    self._barrier.remove(c)
                else:
                    self.last_hit = c
            collision = arcade.check_for_collision_with_list(self.ball, self.ball_collision_list)
            for c in collision:
                self.last_hit = None
                sprite_reflect(self.ball, c)
                if c.stop_game:
                    logger.info("Stop game")
                    data.game_on = False
                    break
                if isinstance(c, Bar):
                    data.score += c.hit()
                    data.inc_ball_speed()
                    self.ball.update_speed()

        self.score_text.value = f"Score: {data.score}"
        self.speed_text.value = f"Speed: {data.get_ball_speed()}"
        self.bar.update(delta_time)
        if data.game_on:
            self.ball.update(delta_time)
        else:
            self.window.game_over()
        return
    def on_key_press(self, key, modifiers):
        self.bar.on_key_press(key, modifiers)
        return
    def on_key_release(self, key, modifiers):
        self.bar.on_key_release(key, modifiers)
        return

class BouncingWindow(arcade.Window):
    def __init__(self):
        super().__init__(data.window_width, data.window_height, data.window_title)
        self.background_color = BACK_GROUND_COLOR
        self.set_mouse_visible(False)
        return
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.Q:
            logger.info("BouncingWindow: start")
            self.close()
        return
    def on_key_release(self, key, modifiers):
        return
    def game_over(self):
        view = data.last_view()
        if view:
            self.show_view(view)
    def game_start(self):
        data.start_over()
        view = data.current_view()
        if view:
            view.ball.reset()
            view.bar.reset()
            self.show_view(view)

def main():
    parse = argparse.ArgumentParser()
    global data
    parse.add_argument("-t", "--test", help="run test",action='store_true')
    parse.add_argument("-v", "--verbos", help="verbos",action='store_true')
    parse.add_argument("-b", "--ball_pos", help="ball position",action='extend', nargs=2, type=int)
    args = parse.parse_args()
    if args.verbos:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s %(levelname)-5s : %(message)s')
    data = Data()
    window = BouncingWindow()
    if args.test:
        ball_pos = args.ball_pos
        if ball_pos is None:
            ball_pos = [600, 700]
        test_view = GameTestView()
        test_view.setup(ball_pos)
        data.append_view(test_view)
    else:
        data.game_on = True
        game_start_view = GameStartView()
        game_start_view.setup()
        data.append_view(game_start_view)
        bouncing_view = BouncingView()
        bouncing_view.setup()
        data.append_view(bouncing_view)
        game_over_view = GameOverView()
        game_over_view.setup()
        data.append_view(game_over_view)
    window.show_view(data.current_view())
    arcade.run()

if __name__ == "__main__":
    main()