import turtle

flower = turtle.Turtle()
flower.color("red")
flower.speed(20)

for i in range(100):
    flower.forward(300)
    flower.left(170)

turtle.done()
