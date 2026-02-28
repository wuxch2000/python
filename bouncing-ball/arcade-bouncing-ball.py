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
    bar_move_speed = 5
    def __init__(self):
        return

class BouncingView(arcade.Window):
    def __init__(self):
        super().__init__(data.window_width, data.window_height, data.window_title)
        self.background_color = arcade.csscolor.BLACK
        return
    def setup(self):
        self.bar_texture = arcade.make_soft_square_texture(size=50, color=arcade.color.RED)
        bar = arcade.SpriteSolidColor(data.bar_width, data.bar_height, arcade.color.RED)
        bar.center_x, bar.center_y = data.bar_pos.x, data.bar_pos.y
        self.bar_sprite_list = arcade.SpriteList()
        self.bar_sprite_list.append(bar)
        return
    def on_draw(self):
        self.clear()
        self.bar_sprite_list.draw()
        return
    def on_update(self, delta_time):
        # Move the player
        self.bar_sprite_list.update(delta_time)
        return
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.Q:
            self.close()
        elif key == arcade.key.LEFT:
            self.bar_sprite_list.change_x = -data.bar_move_speed
        elif key == arcade.key.RIGHT:
            self.bar_sprite_list.change_x = data.bar_move_speed
        return

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.bar_sprite_list.change_x = 0

def main():
    global data
    data = Data()
    window = BouncingView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()