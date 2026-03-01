#! /usr/local/bin/python3

import arcade

class Pos:
    def __init__(self, x, y):
        self.x, self.y = x, y

class Data:
    window_width  = 1024
    window_height = window_width
    window_title  = "Bouncing Ball"
    bar_width     = 80
    bar_height    = 10
    bar_pos       = Pos(window_width/2, 50)
    bar_move_speed = 20
    ball_radius   = 10
    ball_pos      = Pos(window_width/2, bar_pos.y+(bar_height/2)+ball_radius)
    border_gap    = 30
    wall_width    = 10
    def __init__(self):
        return

class Wall(arcade.SpriteSolidColor):
    min_x, max_x, min_y, max_y = False, False, False, False
    def __init__(self, width, height, pos):
        super().__init__(width, height, arcade.color.BLACK_OLIVE)
        self.center_x, self.center_y = pos.x, pos.y
        return

class Border(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        # left wall
        width, height = data.wall_width, data.window_height-2*data.border_gap
        x, y = data.border_gap + data.wall_width/2, data.window_height/2
        wall = Wall(width, height, Pos(x,y))
        wall.min_x = True
        super().append(wall)
        # ceiling
        width, height = data.window_width-2*data.border_gap, data.wall_width
        x, y = data.window_width/2, data.window_height- data.border_gap -data.wall_width/2
        wall = Wall(width, height, Pos(x,y))
        super().append(wall)
        # right wall
        width, height = data.wall_width, data.window_height-2*data.border_gap
        x, y = data.window_width-data.border_gap-data.wall_width/2, data.window_height/2
        wall = Wall(width, height, Pos(x,y))
        wall.max_x = True
        super().append(wall)
        return

class Ball(arcade.SpriteCircle):
    def __init__(self):
        super().__init__(data.ball_radius, arcade.color.RED)
        self.center_x, self.center_y = data.ball_pos.x, data.ball_pos.y
        return

class Bar(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(data.bar_width, data.bar_height, arcade.color.YELLOW)
        self.center_x, self.center_y = data.bar_pos.x, data.bar_pos.y
        self.left_pressed  = False
        self.right_pressed = False
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
            self.change_x = -data.bar_move_speed
        elif self.right_pressed and not self.left_pressed:
            self.change_x = data.bar_move_speed
        return
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
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
        return
    def on_draw(self):
        self.clear()
        self.border.draw()
        self.moving_list.draw()
        return
    def on_update(self, delta_time):
        collision = arcade.check_for_collision_with_list(self.bar, self.border)
        for c in collision:
            if c.min_x and self.bar.change_x < 0:
                self.bar.change_x = 0
            if c.max_x and self.bar.change_x > 0:
                self.bar.change_x = 0
        self.bar.update(delta_time)
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
    window = BouncingView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()