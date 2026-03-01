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
    def __init__(self):
        return

class Bar(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(data.bar_width, data.bar_height, arcade.color.YELLOW)
        self.center_x, self.center_y = data.bar_pos.x, data.bar_pos.y
        return
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        return

class BarList(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.left_pressed  = False
        self.right_pressed = False
        self.change_x = 0
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
        super().move(self.change_x, 0)
        super().update()
        return


class BouncingView(arcade.Window):
    def __init__(self):
        super().__init__(data.window_width, data.window_height, data.window_title)
        self.background_color = arcade.csscolor.BLACK
        return
    def setup(self):
        self.bar_texture = arcade.make_soft_square_texture(size=50, color=arcade.color.RED)
        bar = Bar()
        self.bar_sprite_list = BarList()
        self.bar_sprite_list.append(bar)
        return
    def on_draw(self):
        self.clear()
        self.bar_sprite_list.draw()
        return
    def on_update(self, delta_time):
        self.bar_sprite_list.update(delta_time)
        return
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.Q:
            self.close()
        self.bar_sprite_list.on_key_press(key, modifiers)
        return
    def on_key_release(self, key, modifiers):
        self.bar_sprite_list.on_key_release(key, modifiers)
        return

def main():
    global data
    data = Data()
    window = BouncingView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()