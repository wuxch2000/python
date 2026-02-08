#! /usr/local/bin/python3

from turtle import *
from random import *

class Bar(Turtle):
    _step = 10
    height = 10
    width = 100
    pos_y = -400
    def __init__(self):
        super().__init__()
        poly_size = (self.height, self.width)
        poly = ((0,0),(poly_size[0],0),(poly_size[0],poly_size[1]),(0,poly_size[1]))
        register_shape("brick", poly)
        super().teleport(0, self.pos_y)
        super().shape("brick")
        super().color("yellow")
        super().penup()
        super().speed(5)
        return
    def left(self):
        global border
        x,_ = super().pos()
        border_min_x, _ = border.border_x()
        if(x > border_min_x):
            self.backward(self._step)
        return
    def right(self):
        global border
        x,_ = super().pos()
        _, border_max_x= border.border_x()
        if(x+self.width < border_max_x):
            self.forward(self._step)
        return
    def hit(self, t_ball):
        x,y = t_ball.pos()
        heading = t_ball.heading()
        bar_x, bar_y = super().pos()
        bar_min_x = bar_x 
        bar_max_x = bar_x + self.width
        if(x >= bar_min_x and x <= bar_max_x and y <= bar_y):
            if heading <= 270:
                t_ball.right(2*(heading-180))
            else:
                t_ball.left(2*(360-heading))
            print("bar : heading ", heading, "->", t_ball.heading())
        return True

class Ball(Turtle):
    _speed = 80
    pos_y = -400
    def __init__(self):
        super().__init__()
        super().shape("circle")
        super().penup()
        super().color("red")
        super().teleport(0, self.pos_y)
        # super().setheading(randint(5,90))
        # default_degree = randint(5,90)
        default_degree = 30
        print("ball init heading=", default_degree)
        super().setheading(default_degree)
        super().speed(5)
        return
    def move(self):
        super().getscreen().tracer(0)
        global border, bar
        if border.hit(self) == False:
            return False
        if bar.hit(self) == False:
            return False
        super().forward(self._speed)
        super().getscreen().update()
        return True

class Border(Turtle):
    width, height = 800, 1000
    max_x, min_x, max_y, min_y = width/2, -width/2, height/2, -height/2
    def __init__(self):
        super().__init__()
        super().color("blue")
        super().teleport(self.min_x,self.min_y)
        super().goto(self.min_x, self.max_y)
        super().goto(self.max_x, self.max_y)
        super().goto(self.max_x, self.min_y)
        super().hideturtle()
        return
    def border_x(self):
        return (self.min_x, self.max_x)
    def hit(self, t_ball):
        x,y = t_ball.pos()
        heading = t_ball.heading()
        if x < self.max_x and x > self.min_x and y < self.max_y and y > self.min_y:
            return True
        print("x=", x, "y=", y, "heading=", heading)
        if x >= self.max_x:
            if heading <= 90:
                t_ball.left(2*(90-heading))
            else:
                t_ball.right(2*(heading-270))
            print("max x: heading ", heading, "->", t_ball.heading())
        if x <= self.min_x:
            if heading < 180:
                t_ball.right(2*(heading-90))
            else:
                t_ball.left(2*(270-heading))
            print("min x: heading ", heading, "->", t_ball.heading())
        if y >= self.max_y:
            if heading < 90:
                t_ball.right(2*heading)
            else:
                t_ball.left(2*(180-heading))
            print("max y: heading ", heading, "->", t_ball.heading())
        if y <= self.min_y:
            return False
        return True


def left():
    global bar
    bar.left()

def right():
    global bar
    bar.right()

def quit():
    global bar
    print("quit")
    bye()

def ontimer():
    global bar
    global ball
    if ball.move():
        scr = bar.getscreen()
        scr.ontimer(ontimer, 10) # 0.01s
    return

def init_screen():
    global bar
    screen = bar.getscreen()
    # print(screen.screensize())
    # screen.screensize(1800,400)
    # print(screen.screensize())
    screen.bgcolor("black")
    screen.onkey(left, "Left")
    screen.onkey(right, "Right")
    screen.onkey(quit, "q")
    screen.onkey(quit, "Escape")
    screen.ontimer(ontimer, 10) #0.01s
    return

def init_shape():
    global bar, ball, border
    border = Border()
    bar = Bar()
    ball = Ball()
    return

def init():
    seed()
    init_shape()
    init_screen()
    return

def main():
    init()
    global bar
    screen = bar.getscreen()
    screen.listen()
    screen.mainloop()

if __name__ == "__main__":
    main()