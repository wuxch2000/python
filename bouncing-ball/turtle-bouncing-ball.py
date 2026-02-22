#! /usr/local/bin/python3

from turtle import *
from random import *

class Bar(Turtle):
    _step = 10
    _height, _width = 10, 100
    _pos_y = -400
    def __init__(self):
        super().__init__()
        poly_size = (self._height, self._width)
        poly = ((0,0),(poly_size[0],0),(poly_size[0],poly_size[1]),(0,poly_size[1]))
        register_shape("brick", poly)
        super().teleport(0, self._pos_y)
        super().shape("brick")
        super().color("yellow")
        super().penup()
        return
    def left(self):
        global border
        x,_ = super().pos()
        border_min_x, _ = border.border_x()
        if(x > border_min_x):
            self.backward(self._step)
            getscreen().update()
        return
    def right(self):
        global border
        x,_ = super().pos()
        _, border_max_x= border.border_x()
        if(x+self._width < border_max_x):
            self.forward(self._step)
            getscreen().update()
        return
    def hit(self, t_ball):
        global speed, hits
        x,y = t_ball.pos()
        heading = t_ball.heading()
        bar_x, bar_y = super().pos()
        bar_min_x = bar_x 
        bar_max_x = bar_x + self._width
        if(x >= bar_min_x and x <= bar_max_x and y <= bar_y):
            if heading < 180:
                return
            if heading <= 270:
                t_ball.right(2*(heading-180))
            else:
                t_ball.left(2*(360-heading))
            speed.on_hit()
            hits.on_hit()
            t_ball.speed(speed.speed())
            print("bar : heading ", heading, "->", t_ball.heading())
        return True

class Speed(Turtle):
    _speed = 5
    _pos_x, _pos_y = -390, 470
    def __init__(self):
        super().__init__()
        super().teleport(self._pos_x, self._pos_y)
        super().color("red")
        self._speed = 5
        super().write(f"Speed:{self._speed}", font=("Arial", 20, "normal"))
        super().hideturtle()
        return
    def on_hit(self):
        if self._speed < 10:
            self._speed += 1
            super().clear()
            super().write(f"Speed:{self._speed}", font=("Arial", 20, "normal"))
        return
    def speed(self):
        return self._speed

class Hits(Turtle):
    _hits = 0
    _pos_x, _pos_y = -290, 470
    def __init__(self):
        super().__init__()
        super().teleport(self._pos_x, self._pos_y)
        super().color("yellow")
        self._speed = 0
        super().write(f"Hits:{self._speed}", font=("Arial", 20, "normal"))
        super().hideturtle()
        return
    def on_hit(self):
        self._speed += 1
        super().clear()
        super().write(f"Hits:{self._speed}", font=("Arial", 20, "normal"))
        return

class Ball(Turtle):
    _speed = 10
    _pos_y = -380
    def __init__(self):
        global speed
        super().__init__()
        super().shape("circle")
        super().penup()
        super().color("red")
        super().teleport(0, self._pos_y)
        # super().setheading(randint(5,90))
        default_degree = randint(40,80)
        # default_degree = 30
        print("ball init heading=", default_degree)
        super().setheading(default_degree)
        super().speed(speed.speed())
        return
    def move(self):
        global border, bar
        if border.hit(self) == False:
            return False
        if bar.hit(self) == False:
            return False
        super().forward(self._speed)
        getscreen().update()
        return True

class Border(Turtle):
    _width, _height = 800, 1000
    _max_x, _min_x, _max_y, _min_y = _width/2, -_width/2, _height/2, -_height/2
    def __init__(self):
        super().__init__()
        super().color("blue")
        super().pensize(4)
        super().teleport(self._min_x,self._min_y)
        super().goto(self._min_x, self._max_y)
        super().goto(self._max_x, self._max_y)
        super().goto(self._max_x, self._min_y)
        super().hideturtle()
        return
    def border_x(self):
        return (self._min_x, self._max_x)
    def hit(self, t_ball):
        x,y = t_ball.pos()
        heading = t_ball.heading()
        if x < self._max_x and x > self._min_x and y < self._max_y and y > self._min_y:
            return True
        print("x=", x, "y=", y, "heading=", heading)
        if x >= self._max_x:
            if heading <= 90:
                t_ball.left(2*(90-heading))
            else:
                t_ball.right(2*(heading-270))
            print("max x: heading ", heading, "->", t_ball.heading())
        if x <= self._min_x:
            if heading < 180:
                t_ball.right(2*(heading-90))
            else:
                t_ball.left(2*(270-heading))
            print("min x: heading ", heading, "->", t_ball.heading())
        if y >= self._max_y:
            if heading < 90:
                t_ball.right(2*heading)
            else:
                t_ball.left(2*(180-heading))
            print("max y: heading ", heading, "->", t_ball.heading())
        if y <= self._min_y:
            return False
        return True

bar_move_left, bar_move_right = False, False
def left_press():
    global bar_move_left
    bar_move_left = True
    bar.left()

def left_release():
    global bar_move_left
    bar_move_left = False

def right_press():
    global bar_move_right
    bar_move_right = True

def right_release():
    global bar_move_right
    bar_move_right = False

def quit():
    print("quit")
    bye()

def ontimer():
    global bar, ball
    if bar_move_left:
        bar.left()
    if bar_move_right:
        bar.right()
    if ball.move():
        scr = bar.getscreen()
        scr.ontimer(ontimer, 10) # 0.01s
    return

def init_screen():
    global bar
    screen = getscreen()
    # print(screen.screensize())
    # screen.screensize(1800,400)
    # print(screen.screensize())
    screen.bgcolor("black")
    screen.onkey(left, "Left")
    screen.onkey(right, "Right")
    screen.onkey(quit, "q")
    screen.onkey(quit, "Escape")
    screen.onkeypress(left_press, "Left")
    screen.onkeyrelease(left_release, "Left")
    screen.onkeypress(right_press, "Right")
    screen.onkeyrelease(right_release, "Right")
    screen.ontimer(ontimer, 10) #0.01s
    return

def init_shape():
    global bar, ball, border, speed, hits
    hits = Hits()
    speed = Speed()
    border = Border()
    bar = Bar()
    ball = Ball()
    return

def init():
    seed()
    screen = getscreen()
    screen.tracer(0)
    init_shape()
    init_screen()
    screen.update()
    return

def main():
    init()
    screen = getscreen()
    screen.listen()
    screen.mainloop()

if __name__ == "__main__":
    main()