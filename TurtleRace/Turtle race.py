import turtle
import random

width = 500
height = 500

turtles = 8

turtle.screensize(width, height)

class racer(object):
    def __init__(self,color,pos):
        self.pos = pos
        self.color = color
        self.turtle = turtle.Turtle()
        self.turtle.shape('turtle')
        self.turtle.color(color)
        self.turtle.penup()
        self.turtle.setpos(pos)
        self.turtle.setheading(90)

    def move(self):
        r = random.randrange(1,20)
        self.pos = (self.pos[0], self.pos[1] + r)
        self.turtle.pendown()
        self.turtle.forward(r)

    def reset(self):
        self.turtle.penup()
        self.turtle.setpos(self.pos)



def startGame():
    tList = []
    turtle.clearscreen()
    turtle.hideturtle()
    colors = ["red","blue","yellow","pink","orange","purple","black","green"]
    start = -(width/2)+20
    for t in range(turtles):
        newpos = start +t*height //turtles
        tList.append(racer(colors[t],(newpos,-230)))
        tList[t].turtle.showturtle()

    run = True
    while run:
        for t in tList:
            t.move()

        maxColor = []
        maxDis = 0
        for t in tList:
            if t.pos[1] > 230 and t.pos[1] > maxDis:
                maxDis = t.pos[1]
                maxColor = []
                maxColor.append(t.color)
            elif t.pos[1] > 230 and t.pos[1] == maxDis:
                maxDis = t.pos[1]
                maxColor.append(t.color)

        if len(maxColor) > 0:
            run = False
            print("the winner is: ")
            for color in maxColor:
                print(color)


    oldScore = []
    file = open("scores.txt","r")
    for line in file:
        l = line.split()
        color = l[0]
        score = l[1]
        oldScore.append([color,score])

    file.close()

    file = open("scores.txt","w")

    for entry in oldScore:
        for winner in maxColor:
            if entry[0] == winner:
                entry[1] = int(entry[1])+1

        file.write(str(entry[0]) + ' ' + str(entry[1]) + '\n')

    file.close()

start = input("start")
startGame()
while True:
    start = input("start again")
    startGame()
