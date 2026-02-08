import turtle
line_length = 200
t = turtle.Turtle()
t.pencolor("red")
t.pensize(4)
for x in range(0,line_length):
    y=x
    t.goto(x,y)
turtle.done()