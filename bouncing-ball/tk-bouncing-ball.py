#! /usr/local/bin/python3

import math
import random
from tkinter import *
from tkinter import ttk

game_text_id_list = list()
def game_over():
    global game_text_id_list
    global canvas
    x = canvas.max_x()
    y = canvas.max_y()
    game_text_id_list.append(canvas.create_text(x/2, y/2, text="Game Over", anchor="center", fill="blue", font=("Helvetica", 64, "italic")))
    game_text_id_list.append(canvas.create_text(x/2, (y/2)+50, text="Press <space> to start", anchor="center", fill="green", font=("Helvetica", 24, "roman")))
    return
# _default_timeout = 10
_default_timeout = 100

def _timeout(root):
    global ball, global_start
    root.after(_default_timeout, _timeout, root)
    # print("timeout: global_start=", global_start, "ball.stop()", ball.stop())
    if not global_start:
        return
    if ball.stop():
        game_over()
        global_start = False
        return
    ball.move()
    return

def _quit():
    root.destroy()
    return

def _game_start_text():
    global canvas, game_text_id_list
    x = canvas.max_x()
    y = canvas.max_y()
    game_text_id_list.append(canvas.create_text(x/2, y/2, text="Press <space> to start", anchor="center", fill="green", font=("Helvetica", 24, "roman")))
    return

def _clear_all_text():
    global canvas, game_text_id_list
    for i in game_text_id_list:
        canvas.delete(i)
    return

global_start = False
needs_reset = False
def _start():
    global canvas, bar, ball, data
    global global_start, needs_reset
    print("------> start")
    if needs_reset:
        data.reset()
        bar.reset()
        ball.reset()
    else:
        needs_reset = True
    global_start = True
    _clear_all_text()
    return

def _on_key(event):
    global bar
    # print("Key:", event.keysym)
    if event.keysym == "q":
        _quit()
    elif event.keysym == "space":
        _start()
    elif event.keysym == "Left":
        bar.move_left()
    elif event.keysym == "Right":
        bar.move_right()
    return

class BouncingCanvas(Canvas):
    _width, _height, color = 1150, 900, 'black'
    def __init__(self, master):
        super().__init__(master, width=BouncingCanvas._width, height=BouncingCanvas._height, bg=BouncingCanvas.color)
        super().grid(column=1, columnspan=4, row=2, sticky=W)
        return
    def size(self):
        return (self._width, self._height)
    def max_x(self):
        return self._width
    def min_x(self):
        return 0
    def max_y(self):
        return self._height
    def min_y(self):
        return 0

class Object:
    _master = None
    _tk_id = None
    _border_width = None
    def __init__(self, master, tk_id, border_width=1):
        self._master = master
        self._tk_id = tk_id
        self._border_width = border_width
        return
    def moveto(self, new_coord):
        return self._master.coords(self._tk_id, new_coord)
    def coords(self):
        return self._master.coords(self._tk_id)

class Ball(Object):
    radius = 10
    max_dist_per_move = 20
    _angle = None
    _stop = False
    
    def __init__(self, master):
        self._angle = random.uniform(math.pi/4, math.pi*3/4)
        # self._angle = math.pi*3/8
        x = (int)(master.max_x()/2)
        y = (int)(master.max_y()*0.9)-Ball.radius
        pos = ( x-Ball.radius, y-Ball.radius, x+Ball.radius, y+Ball.radius)
        super().__init__(master, master.create_oval(*pos, fill='red', outline='red'))
        return
    def reset(self):
        self._angle = random.uniform(math.pi/4, math.pi*3/4)
        self._stop = False
        x = (int)(self._master.max_x()/2)
        y = (int)(self._master.max_y()*0.9)-Ball.radius
        pos = ( x-Ball.radius, y-Ball.radius, x+Ball.radius, y+Ball.radius)
        super().moveto(pos)
        return
    def stop(self):
        return self._stop
    def set_stop(self):
        self._stop = True
        return
    def angle(self) -> float:
        return self._angle
    def next_pos(self, distance):
        if distance <= 0:
            return None
        delta_x = int(distance * math.cos(self._angle))
        delta_y = 0-int(distance * math.sin(self._angle))
        pos = super().coords()
        new_pos = (pos[0]+delta_x, pos[1]+delta_y, pos[2]+delta_x, pos[3]+delta_y)
        # print("move_ball: ", pos, "-->", new_pos)
        return new_pos
    def _moveto(self, new_pos):
        pos = super().coords()
        dist = abs(int((new_pos[0] - pos[0])/math.cos(self._angle)))
        moved_dist = 0
        while moved_dist < dist:
            if dist - moved_dist >= Ball.max_dist_per_move:
                d = Ball.max_dist_per_move
                moved_dist += d
                print("move dist by max:", d)
                p = self.next_pos(d)
                super().moveto(p)
            else:
                d = dist - moved_dist
                moved_dist += d
                print("move dist:", d)
                p = self.next_pos(d)
                super().moveto(p)
        return
    def move(self):
        global wall,bar,data
        if self._stop:
            return
        for obj in [bar, wall]:
            hit, drop, distance, remain_dist, new_angle = obj.hit(self)
            print("--> ball:", hit, drop, distance, remain_dist, new_angle)
            if drop:
                self.set_stop()
                return
            if hit:
                pos = super().coords()
                next_pos = self.next_pos(distance)
                print("--> ball hit(dist=", distance, "):", pos, "-->", next_pos)
                self._moveto(next_pos)
                if remain_dist is not None:
                    if new_angle is not None:
                        self._angle = new_angle
                        # print("ball: set new angle to", self._angle)
                    next_pos = self.next_pos(remain_dist)
                    print("--> ball hit(remain dist=", remain_dist, "):", "-->", next_pos)
                    self._moveto(next_pos)
                if isinstance(obj, Bar):
                    data.bar_hit()
                return
        next_pos = self.next_pos(distance)
        self._moveto(next_pos)
        return

class Wall(Object):
    _border_width = 5
    _border_margin = 20
    _wall_color = 'gray'
    min_x, max_x, min_y, max_y = None, None, None, None
    def __init__(self, master):
        self.min_x, self.max_x, self.min_y, self.max_y = Wall._border_margin, master.max_x() - Wall._border_margin, Wall._border_margin, master.max_y() - Wall._border_margin
        print("Wall:", self.min_x, self.min_y, self.max_x, self.max_y)
        pos1 = (self.min_x , self.max_y)
        pos2 = (self.min_x , self.min_y)
        pos3 = (self.max_x , self.min_y)
        pos4 = (self.max_x , self.max_y)
        super().__init__(master, master.create_line(*pos1, *pos2, *pos3, *pos4, fill=Wall._wall_color, width=Wall._border_width))
        return
    def hit(self, ball:Ball) -> tuple[bool,bool,int,int,int]:
        hit, drop = False, False
        predict_dist = data.ball_speed()
        remain_dist = 0
        new_angle = 0
        ball_next_pos = ball.next_pos(predict_dist)
        x1, y1, x2, y2 = ball_next_pos
        if x1 > self.min_x and y1 > self.min_y and x2 < self.max_x and y2 < self.max_y:
            print("wall: ball[", x1, y1, "] [",x2, y2, "] vs", self.min_x, self.min_y, self.max_x, self.max_y, "pass")
            remain_dist = predict_dist
            return hit, drop, remain_dist, None, None
        angle = ball.angle()
        print("wall: ball[", x1, y1, "] [",x2, y2, "] vs", self.min_x, self.min_y, self.max_x, self.max_y, "angle=", angle)
        hit = True
        if angle < 0:
            angle += angle + 2*math.pi
        new_angle = angle
        if angle <= math.pi/2:
            x, y = x2, y1
            if y < self.min_y and x > self.max_x:
                angle1 = math.atan2(self.min_y - y, x - self.max_x)
                if angle1 > angle: # hit top
                    print("hit top wall to right")
                    new_angle = 2* math.pi - angle
                    remain_dist = predict_dist - int(abs((self.min_y - y)/math.sin(angle)))
                else: # hit right
                    print("hit right wall to top")
                    new_angle = math.pi - angle
                    remain_dist = predict_dist - int(abs((self.max_x - x)/math.cos(angle)))
            elif y < self.min_y: # hit top
                print("hit top wall to right")
                new_angle = 2* math.pi - angle
                remain_dist = predict_dist - int(abs((self.min_y - y)/math.sin(angle)))
            elif x > self.max_x: # hit right
                print("hit right wall to top")
                new_angle = math.pi - angle
                remain_dist = predict_dist - int(abs((self.max_x - x)/math.cos(angle)))
        elif angle <= math.pi:
            x, y = x1, y1
            if y < self.min_y and x < self.min_x:
                angle1 = math.pi - math.atan2(self.min_y - y, x - self.max_x)
                if angle1 > angle: # hit top
                    print("hit top wall to left")
                    new_angle =  2*math.pi - angle
                    remain_dist = predict_dist - int(abs((self.min_y - y)/math.sin(angle)))
                else: # hit left
                    print("hit left wall to top")
                    new_angle =  math.pi - angle
                    remain_dist = predict_dist - int(abs((x - self.min_x)/math.cos(angle)))
            elif y < self.min_y: # hit top
                print("hit top wall to left")
                new_angle =  2*math.pi - angle
                remain_dist = predict_dist - int(abs((self.min_y - y)/math.sin(angle)))
            elif x < self.min_x: # hit left
                print("hit left to top")
                new_angle =  math.pi - angle
                remain_dist = predict_dist - int(abs((x - self.min_x)/math.cos(angle)))
        elif angle <= math.pi*3/2:
            x, y = x1, y2
            if y > self.max_y and x < self.min_x:
                angle1 = math.atan2(y- self.max_y, self.min_x - x)
                if angle1 + math.pi > angle: #hit bottom
                    print("hit bottom hole to left")
                    remain_dist = 0
                    drop = True
                else: # hit left
                    print("hit left wall to bottom")
                    new_angle = 2 * math.pi - (angle - math.pi)
                    remain_dist = predict_dist - int(abs((x - self.min_x)/math.cos(angle)))
            elif x < self.min_x: # hit left
                print("hit left wall to bottom")
                new_angle = 2 * math.pi - (angle - math.pi)
                remain_dist = predict_dist - int(abs((x - self.min_x)/math.cos(angle)))
            elif y > self.max_y: # hit bottom
                print("hit bottom wall to lefrt")
                remain_dist = 0
                drop = True
        elif angle <= math.pi*2:
            x, y = x2, y2
            if y > self.max_y and x > self.max_x:
                angle1 = 2 *math.pi - math.atan2(y- self.max_y, x - self.max_x)
                if angle1 < angle: # hit bottom
                    print("hit bottom hole to right")
                    remain_dist = 0
                    drop = True
                else: # hit right
                    print("hit right wall to bottom")
                    new_angle = 3 * math.pi - angle
                    remain_dist = predict_dist - int(abs((self.max_x - x)/math.cos(angle)))
            elif y > self.max_y : # hit bottom
                print("hit bottom hole to right")
                remain_dist = 0
                drop = True
            elif x > self.max_x : # hit right
                print("hit right wall to bottom")
                new_angle = 3 * math.pi - angle
                remain_dist = predict_dist - int(abs((self.max_x - x)/math.cos(angle)))
        return hit, drop, predict_dist-remain_dist, remain_dist, new_angle

class Bar(Object):
    _width, _height = 100, 10
    _move_speed = 10
    min_x, max_x, min_y, max_y = None, None, None, None
    def __init__(self, master):
        x = (int)(master.max_x()/2)
        y = (int)(master.max_y()*0.9)
        self.min_x, self.max_x, self.min_y, self.max_y = x-(Bar._width/2), x+(Bar._width/2), y-(Bar._height/2), y+(Bar._height/2)
        pos = ( self.min_x, self.min_y, self.max_x, self.max_y)
        super().__init__(master, master.create_rectangle(*pos, fill='yellow', outline='red', width=Bar._border_width))
        return
    def reset(self):
        x = (int)(self._master.max_x()/2)
        y = (int)(self._master.max_y()*0.9)
        self.min_x, self.max_x, self.min_y, self.max_y = x-(Bar._width/2), x+(Bar._width/2), y-(Bar._height/2), y+(Bar._height/2)
        super().moveto((self.min_x, self.min_y, self.max_x, self.max_y))
        return

    def move_left(self):
        global wall, data
        wall_min_x = wall.min_x
        pos = super().coords()
        x = pos[0] - data.bar_speed()
        if x <= wall_min_x:
           x = wall_min_x
        self.min_x, self.min_y, self.max_x, self.max_y = (x, pos[1], x+Bar._width, pos[3])
        # print("move_left: ", pos, "-->", new_pos)
        self.moveto((self.min_x, self.min_y, self.max_x, self.max_y))
        return
    def move_right(self):
        global wall, data
        wall_max_x = wall.max_x
        pos = super().coords()
        x = pos[0] + data.bar_speed()
        if x  >= wall_max_x - self._width:
            x = wall_max_x - self._width
        self.min_x, self.min_y, self.max_x, self.max_y = (x, pos[1], x+Bar._width, pos[3])
        # print("move_right: ", pos, "-->", new_pos)
        self.moveto((self.min_x, self.min_y, self.max_x, self.max_y))
        return
    def hit(self, ball:Ball) -> tuple[bool,int]:
        hit, drop = False, False
        predict_dist = data.ball_speed()
        remain_dist = 0
        ball_next_pos = ball.next_pos(predict_dist)
        angle = ball.angle()
        new_angle = angle
        x1, y1, x2, y2 = ball_next_pos
        if y2 <= self.min_y:
            return hit, drop, 0, None, None
        if angle < 0:
            angle += angle + 2*math.pi
        if x2 > self.min_x and x1 < self.max_x:
            hit = True
            print("bar ([", self.min_x, self.min_y, "] [", self.max_x, self.max_y, "]): ball:[", x1, y1,"] [", x2, y2, "] angle=", angle)
            new_angle = angle
            if angle <= math.pi:
                print("Error")
            elif angle <= math.pi*3/2:
                x, y = x1, y2
                print("hit bar to left")
                new_angle =  2* math.pi - angle
                remain_dist = predict_dist - int(abs((y- self.min_y)/math.sin(angle-(math.pi))))
            elif angle <= math.pi*2:
                x, y = x1, y2
                print("hit bar to right")
                new_angle =  2*math.pi - angle
                remain_dist = predict_dist - int(abs((y- self.min_y)/math.sin((math.pi*2-angle))))
            return hit, drop, predict_dist-remain_dist, remain_dist, new_angle
        else:
            print("bar ([", self.min_x, self.min_y,"] [", self.max_x, self.max_y,"]): ball:[", x1, y1,"] [", x2, y2, "] angle=", angle)
            return hit, drop, predict_dist, None, None
        return

class Data:
    _master = None
    _ball_speed = 20
    _ball_speed_var: None
    _bar_hit  = 0
    _bar_hit_var: None
    _bar_speed = 20
    def reset(self):
        self._ball_speed = 20
        self._ball_hit = 0
        print("Data reset: ball_speed=", self._ball_speed, "ball_hit=", self._ball_hit)
        self._ball_speed_var.set(self._text_ball_speed())
        self._bar_hit_var.set(self._text_bar_hit())
        return
    def _text_ball_speed(self):
        return f'Speed: {self._ball_speed}'
    def _text_bar_hit(self):
        return f'Hit: {self._bar_hit}'
    def __init__(self, master):
        self._master = master
        self._ball_speed_var = StringVar()
        self._ball_speed_var.set(self._text_ball_speed())
        ttk.Label(master, textvariable=self._ball_speed_var, width=20, foreground="yellow", font=("Helvetica", 20, "roman")).grid(column=1, row=1, sticky=W)

        self._bar_hit_var = StringVar()
        self._bar_hit_var.set(self._text_bar_hit())
        ttk.Label(master,  textvariable=self._bar_hit_var, width=20, foreground="yellow", font=("Helvetica", 20, "roman")).grid(column=2, row=1, sticky=W)
        return
    def ball_speed(self, ball_speed=None):
        if ball_speed is not None:
            self._ball_speed = ball_speed
            self._ball_speed_var.set(self._text_ball_speed())
        return self._ball_speed
    def bar_hit(self):
        self._bar_hit += 1
        self._bar_hit_var.set(self._text_bar_hit())
        self.ball_speed(self._ball_speed + 10)
        return self._bar_hit
    def bar_speed(self, bar_speed=None):
        if bar_speed is not None:
            self._bar_speed = bar_speed
        return self._bar_speed

def init():
    global root, canvas, wall, ball, bar, data
    root = Tk()
    root.title("Bouncing Ball")
    root.geometry("1200x1000")
    mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    canvas = BouncingCanvas(mainframe)
    data = Data(mainframe)
    wall = Wall(canvas)
    bar = Bar(canvas)
    ball = Ball(canvas)
    _game_start_text()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(2, weight=1)
    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    root.bind("<KeyPress>", _on_key)
    root.focus_set()
    root.after(_default_timeout, _timeout, root)

def run():
    global root
    root.mainloop()
    return

def main():
    init()
    run()
    return

if __name__ == "__main__":
    main()