# baby project for the Udacity course "Introduction to Programming"
import turtle

def draw_square():
    window = turtle.Screen()
    window.bgcolor("red")

    brad = turtle.Turtle()

    brad.shape("turtle")
    brad.speed(3)

    for n in range(1,5):
        brad.forward(50)
        brad.right(90)

    window.exitonclick()
