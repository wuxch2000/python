#! /usr/local/bin/python3

import arcade

WINDOW_WIDTH  = 1024
WINDOW_HEIGHT = WINDOW_WIDTH
WINDOW_TITLE  = "Bouncing Ball"

class BouncingView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.background_color = arcade.csscolor.BLACK
        return
    def setup(self):
        pass 
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.Q:
            self.close()
        return
    def on_draw(self):
        self.clear()
        return

def main():
    window = BouncingView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()