import turtle
# Set key parameters
gravity = -0.005  # pixels/(time of iteration)^2
y_velocity = 1  # pixels/(time of iteration)
x_velocity = 0.25  # pixels/(time of iteration)
energy_loss = 0.95
width = 600ight = 800
# Set window and ball
window = turtle.Screen()
window.setup(width, height)
window.tracer(0)
ball = turtle.Turtle()
ball.penup()
ball.color("green")
ball.shape("circle")
# Main loop
while True:
    # Move ball
    ball.sety(ball.ycor() + y_velocity)
    ball.setx(ball.xcor() + x_velocity)
    # Acceleration due to gravity
    y_velocity += gravity
    # Bounce off the ground
    if ball.ycor() < -height / 2:
        y_velocity = -y_velocity * energy_loss
        # Set ball to ground level to avoid it getting "stuck"
        ball.sety(-height / 2)
    # Bounce off the walls (left and right)
    if ball.xcor() > width / 2 or ball.xcor() < -width / 2:
        x_velocity = -x_velocity
    window.update()