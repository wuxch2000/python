#! /usr/local/bin/python3

from tkinter import *
from tkinter import ttk

def _quit():
    root.destroy()
    return

_default_timeout = 10
def _timeout(root):
    # print("timeout")
    root.after(_default_timeout, _timeout, root)
    return

def _on_key_left():
    global canvas, ball
    canvas.move(ball, -10, 0)
    return

def _on_key_right():
    global canvas, ball
    canvas.move(ball, +10, 0)
    return

def _on_key(event):
    print("Key:", event.keysym)
    if event.keysym == "q":
        _quit()
    elif event.keysym == "Left":
        _on_key_left()
    elif event.keysym == "Right":
        _on_key_right()
    return

def main():
    global root, canvas, ball
    root = Tk()
    root.title("Bouncing Ball")
    root.geometry("1200x1000")
    mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    ttk.Label(mainframe, text="Speed", width=20).grid(column=1, row=1, sticky=W)
    canvas = Canvas(mainframe, width=1150, height=900, bg='black')
    canvas.grid(column=1, row=2, sticky=W)
    bar = canvas.create_rectangle(0, 0, 20, 20, fill='yellow', outline='yellow')
    ball = canvas.create_oval(30,30, 60, 60, fill='red', outline='red')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(2, weight=1)
    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    # root.bind("<KeyPress-q>", _quit)
    # root.bind("<Left>", _on_key_left)
    # root.bind("<Right>", _on_key_right)
    root.bind("<KeyPress>", _on_key)
    root.after(_default_timeout, _timeout, root)
    root.focus_set()
    root.mainloop()
    return

if __name__ == "__main__":
    main()