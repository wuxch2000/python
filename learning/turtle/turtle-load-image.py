#! /usr/local/bin/python3 

from turtle import *

jet = Turtle()
screen = jet.getscreen()

image_file = "jet1.gif"
print(image_file)
screen.register_shape("jet",image_file)
jet.shapesize(5,5,12)
jet.shape("jet")
jet.forward(10)

def main():
    screen.listen()
    screen.mainloop()

if __name__ == "__main__":
    main()