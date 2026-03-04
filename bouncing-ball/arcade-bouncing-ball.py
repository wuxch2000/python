#! /usr/local/bin/python3

import random
import math
import numpy
import arcade

def reflect_vector(incident_vector, normal_vector):
    n = normal_vector / numpy.linalg.norm(normal_vector)
    v_dot_n = numpy.dot(incident_vector, n)
    return incident_vector - 2 * v_dot_n * n

class Pos:
    def __init__(self, x, y):
        self.x, self.y = x, y

class Data:
    game_on       = False
    window_width  = 1024
    window_height = window_width
    window_title  = "Bouncing Ball"
    bar_width     = 100
    bar_height    = 10
    bar_pos       = Pos(window_width/2, 50)
    bar_speed     = 15
    ball_radius   = 10
    ball_pos      = Pos(window_width/2, bar_pos.y+(bar_height/2)+ball_radius)
    ball_speed    = 5
    ball_speed_inc= 2
    border_gap    = 30
    wall_width    = 10
    hit           = 0
    def __init__(self):
        return

class Wall(arcade.SpriteSolidColor):
    min_x, max_x, min_y, max_y = False, False, False, False
    stop_game = False
    def __init__(self, width, height, pos, normal_vec: numpy.array, wall_color, stop_game = False):
        super().__init__(width, height, color=wall_color)
        self.center_x, self.center_y = pos.x, pos.y
        self.normal_vec = normal_vec
        self.stop_game = stop_game
        return
    def hit(self):
        return 0

class Border(arcade.SpriteList):
    regular_wall_color = arcade.color.BLACK_OLIVE
    bottom_wall_color = arcade.color.BLACK
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
        wall = Wall(width, height, Pos(x,y), numpy.array([0, 0]), Border.bottom_wall_color, stop_game = True) # ball will stop for normal-vector 0,0
        super().append(wall)
        return

class Ball(arcade.SpriteCircle):
    def _update_x_y(self, angle):
        self.change_x = data.ball_speed * math.cos(angle)
        self.change_y = data.ball_speed * math.sin(angle)
        return
    def __init__(self):
        super().__init__(data.ball_radius, arcade.color.RED)
        self.center_x, self.center_y = data.ball_pos.x, data.ball_pos.y
        random_list = { 0:(math.pi/4, math.pi*3/8), 1:(math.pi*5/8, math.pi*6/8) }
        rand_i = random.randint(0,1)
        rand_min, rand_max = random_list[rand_i]
        angle = random.uniform(rand_min, rand_max)
        self._update_x_y(angle)
        return
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        return
    def update_speed(self):
        angle = math.atan2(self.change_y, self.change_x)
        self._update_x_y(angle)
        return

class Bar(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(data.bar_width, data.bar_height, color=arcade.color.YELLOW)
        self.center_x, self.center_y = data.bar_pos.x, data.bar_pos.y
        self.left_pressed  = False
        self.right_pressed = False
        self.stop_game = False
        self.normal_vec = numpy.array([0,1])
        self.min_x = data.border_gap+data.wall_width+(data.bar_width/2)
        self.max_x = data.window_width-self.min_x
        return
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
        return 1
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        if self.center_x < self.min_x:
            self.center_x = self.min_x
        elif self.center_x > self.max_x:
            self.center_x = self.max_x
        self.center_y += self.change_y
        return

class BouncingView(arcade.Window):
    def __init__(self):
        super().__init__(data.window_width, data.window_height, data.window_title)
        self.background_color = arcade.csscolor.BLACK
        return
    def setup(self):
        self.moving_list = arcade.SpriteList()
        self.border = Border()
        self.bar= Bar()
        self.moving_list.append(self.bar)
        self.ball= Ball()
        self.moving_list.append(self.ball)
        self.score_text = arcade.Text(f"Hit: {data.hit}", 10,  data.window_height - 20, arcade.color.WHITE, 14)
        self.speed_text = arcade.Text(f"Speed: {data.ball_speed}", 80, data.window_height - 20, arcade.color.WHITE, 14)
        self.game_over_text = arcade.Text(f"Game Over", (data.window_width/2)-140, data.window_height/2, arcade.color.WHITE, font_size=46, bold=True, italic=True )

        self.ball_collision_list = arcade.SpriteList() 
        for s in self.border:
            self.ball_collision_list.append(s)
        self.ball_collision_list.append(self.bar)
        return
    def on_draw(self):
        global data
        self.clear()
        self.border.draw()
        self.moving_list.draw()
        self.score_text.draw()
        self.speed_text.draw()
        if not data.game_on:
            self.game_over_text.draw()
        return
    def on_update(self, delta_time):
        global data
        if data.game_on:
            collision = arcade.check_for_collision_with_list(self.ball, self.ball_collision_list)
            for c in collision:
                incident_vec = numpy.array([self.ball.change_x, self.ball.change_y])
                refect_vec = reflect_vector(incident_vec, c.normal_vec)
                self.ball.change_x, self.ball.change_y = refect_vec[0], refect_vec[1]
                if c.stop_game:
                    print("Stop game")
                    data.game_on = False
                    break
                if c.hit():
                    old_hit = data.hit
                    data.hit += c.hit()
                    print("hit: ", old_hit, "->", data.hit)
                    old_speed = data.ball_speed
                    data.ball_speed += data.ball_speed_inc
                    print("speed: ", old_speed, "->", data.ball_speed)
                    self.ball.update_speed()

        self.score_text.value = f"Hit: {data.hit}"
        self.speed_text.value = f"Speed: {data.ball_speed}"
        self.bar.update(delta_time)
        if data.game_on:
            self.ball.update(delta_time)
        return
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.Q:
            self.close()
        self.bar.on_key_press(key, modifiers)
        return
    def on_key_release(self, key, modifiers):
        self.bar.on_key_release(key, modifiers)
        return

def main():
    global data
    data = Data()
    data.game_on = True
    window = BouncingView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()