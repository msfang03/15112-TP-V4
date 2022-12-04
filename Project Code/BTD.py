#################################################
# Term Project
#
# Your name:Max Fang
# Your andrew id:msfang
# Section: O
#################################################
from cmu_112_graphics import *
import math
import random

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)
#################################################
#when health gets to certain level remove instance and then 
#choose targeting methods
#Bloons Class
class Bloons:
    def __init__(self, x, y, life, color, speed, damage):
        self.x = x
        self.y = y
        self.r = 20
        self.life = life
        self.color = color
        self.speed = speed
        self.damage = damage

    def timerFired(self, app):
        if self.y == app.height//2 and self.x < app.width * (2/5):
            self.x += self.speed
        elif (app.width * (3/5) > self.x >= app.width * (2/5) and 
        app.height//2 <= self.y < app.height * (3/4)):
            self.y += self.speed
        elif (self.y >= app.height * (3/4) and 
        app.width * (2/5) <= self.x < app.width * (3/5)):
            self.x += self.speed
        elif self.x >= app.width * (3/5):
            self.y -= self.speed

class RedBloon(Bloons):
    def __init__(self, x, y):
        super().__init__(x, y, 1, "red", 3, 1)
    
    #redraw image from url from "Class Notes: Event-Based Animations in Tkinter"
    def redraw(self, app, canvas):
        canvas.create_image(self.x, self.y, 
        image=ImageTk.PhotoImage(app.imageRed))
 
class BlueBloon(Bloons):
    def __init__(self, x, y):
        super().__init__(x, y, 2, "blue", 5, 2)

    #redraw image from url from "Class Notes: Event-Based Animations in Tkinter"
    def redraw(self, app, canvas):
        canvas.create_image(self.x, self.y, 
        image=ImageTk.PhotoImage(app.imageBlue))

def demote(app, bloon):
    if isinstance(bloon, BlueBloon) and bloon.life == 1:
        index = app.bloons.index(bloon)
        app.bloons.append(RedBloon(bloon.x, bloon.y))
        app.bloons.pop(index)

#Monkey class
class Monkey:
    def __init__(self, x, y, r, time):
        self.x = x
        self.y = y
        self.r = r
        self.state = True
        self.placed = False
        self.time = time

    def inRange(self, bloon):
        return (distance(self.x, self.y, bloon.x, bloon.y) <= self.r or 
            self.r == 0)

    def targetStrongest(self, app, L):
        for i in range(len(app.bloons)):
            if self.inRange(app.bloons[i]):
                L.append((app.bloons[i].life, i))
        if L != []:
            strongest = L[0][0]
            strongestIndex = L[0][1]
            for bloonLife, index in L:
                if bloonLife > strongest:
                    strongestIndex = index
            bloon = app.bloons[strongestIndex]
            app.bloons[strongestIndex].life -= 1
            if app.bloons[strongestIndex].life == 0:
                app.bloons.pop(strongestIndex)
            return bloon

    def targetWeakest(self, app, L):
        for i in range(len(app.bloons)):
            if self.inRange(app.bloons[i]):
                L.append((app.bloons[i].life, i))
        if L != []:
            weakestIndex = L[0][0]
            weakestIndex = L[0][1]
            for bloon, index in L:
                if bloon < weakestIndex:
                    weakestIndex = index
            bloon = app.bloons[weakestIndex]
            app.bloons[weakestIndex].life -= 1
            return bloon

    def targetFirst(self, app, L):
        for bloons in app.bloons:
            if self.inRange(bloons):
                L.append(bloons) 
        if L != []:
            bloon = L[0]  
            L[0].life -= 1
            return bloon

    def targeting(self, app, num):
        if len(app.bloons) > 0:
            L = []
            if num == 1:
                bloon = self.targetStrongest(app, L)
            elif num == 2:
                bloon = self.targetWeakest(app, L)
            elif num == 3:
                bloon = self.targetFirst(app, L)
            if bloon != None:
                app.dart.append(Dart(self.x, self.y, self, bloon))
                app.money += 1

#most hp, fastest, first 
class Dart:
    def __init__(self, x, y, monkey, bloon):
        self.x = x
        self.y = y
        self.monkey = monkey
        self.bloon = bloon
    
    def timerFired(self, app):
        horizontal = abs(self.bloon.x - self.monkey.x)
        vertical = abs(self.bloon.y - self.monkey.y)
        if horizontal > vertical:
            if self.bloon.x - self.monkey.x < 0:
                self.x -= 10
            elif self.bloon.x - self.monkey.x > 0:
                self.x += 10
        else:
            if self.bloon.y - self.monkey.y > 0:
                self.y += 10
            elif self.bloon.y - self.monkey.y < 0:
                self.y -= 10
        if (distance(self.x, self.y, self.monkey.x, self.monkey.y) >= 
        self.monkey.r):
            i = app.dart.index(self)
            app.dart.pop(i)
    #redraw image from url from "Class Notes: Event-Based Animations in Tkinter"
    def redraw(self, app, canvas):
        canvas.create_image(self.x, self.y, 
        image=ImageTk.PhotoImage(app.imageDart))

class DartMonkey(Monkey):
    def __init__(self, x, y, time):
        super().__init__(x, y, 80, time)

    #redraw image from url from "Class Notes: Event-Based Animations in Tkinter"
    def redraw(self, app, canvas):
        canvas.create_image(self.x, self.y, 
        image=ImageTk.PhotoImage(app.imageDartMonk))

    def timerFired(self, app):
        if app.time - self.time > 250:
            self.time = app.time
            self.targeting(app, app.targetMode)

class SniperMonkey(Monkey):
    def __init__(self, x, y, time):
        super().__init__(x, y, 0, time)
    
    def timerFired(self, app):
        if app.time - self.time > 500:
            self.time = app.time
            self.targeting(app, app.targetMode)

    def redraw(self, app, canvas):
        #redraw image from url from "Class Notes: Event-Based Animations in Tkinter"
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(app.imageSnipe))

# Code structured after class notes - OOP part 1
def appStarted(app):
    app.bloons = []
    app.predictor = []
    app.time = 0
    app.timerDelay = 10
    app.health = 100
    app.monkey = []
    app.money = 650
    app.size = app.width//10
    app.row = 20
    app.col = 30
    app.cellSizeY = app.height/app.row
    app.cellSizeX = app.width/app.col
    app.board = [[True] * app.col for i in range(app.row)]
    drawPath(app)
    app.state = False
    app.dartMonkPrice = 170
    app.snipeMonkPrice = 300
    app.dart = []
    #redraw image from url from "Class Notes: Event-Based Animations in Tkinter"
    urlSnipe = 'https://static.wikia.nocookie.net/b__/images/f/ff/BTD6_Sniper_Monkey.png/revision/latest?cb=20180616150336&path-prefix=bloons'
    app.imageSnipe1 = app.loadImage(urlSnipe)
    app.imageSnipe = app.scaleImage(app.imageSnipe1, 1/8)
    urlDartMonk = 'https://static.wikia.nocookie.net/b__/images/e/e2/Btd6monkey.png/revision/latest?cb=20180426113758&path-prefix=bloons'
    app.imageDartMonk1 = app.loadImage(urlDartMonk)
    app.imageDartMonk = app.scaleImage(app.imageDartMonk1, 1/8)
    urlRedBloon = 'https://static.wikia.nocookie.net/b__/images/f/f2/BTD6Red.png/revision/latest?cb=20180809060915&path-prefix=bloons'
    app.imageRedB1 = app.loadImage(urlRedBloon)
    app.imageRed = app.scaleImage(app.imageRedB1, 3/4)
    urlBlueBloon = 'https://static.wikia.nocookie.net/b__/images/8/83/BTD6Blue.png/revision/latest?cb=20190620020620&path-prefix=bloons'
    app.imageBlueB1 = app.loadImage(urlBlueBloon)
    app.imageBlue = app.scaleImage(app.imageBlueB1, 3/4)
    urlDart = 'https://blog.knife-depot.com/wp-content/uploads/2020/03/shuriken-676x676.png'
    app.imageDart1 = app.loadImage(urlDart)
    app.imageDart = app.scaleImage(app.imageDart1, 1/26)
    app.targetMode = 1
    app.targetModeName = 'Strongest'
    app.round = 1
    app.length = 10
    app.spawnSpeed = 100
    app.roundBloons = []
    app.pause = True
    app.gameOver = False

def getCell(app, x, y):
    resultx = x//app.cellSizeX
    resulty = y//app.cellSizeY
    return int(resulty), int(resultx)

def isLegal(app, x, y):
    row, col = getCell(app, x, y)
    return app.board[row][col]

def targetingTransition(app):
    if app.targetMode == 1 :
        app.targetModeName = 'Strongest'
    elif app.targetMode == 2:
        app.targetModeName = 'Weakest'
    elif app.targetMode == 3:
        app.targetModeName = 'First'

def drawBoard(app, canvas):
    roadCol = 'burlywood'
    for i in range(app.col):
        for j in range(app.row):
            if (j == 10 or j == 9) and i <= 12:
                color = roadCol
            elif (i == 12 or i == 11) and 10 < j <= 15:
                color = roadCol
            elif (j == 15 or j == 14) and 12 < i <= 18:
                color = roadCol
            elif (i == 18 or i == 17) and j < 15:
                color = roadCol
            else: color = 'green'
            x0 = app.width * (i/app.col)
            y0 = app.height * (j/app.row)
            x1 = x0 + app.cellSizeX
            y1 = y0 + app.cellSizeY
            canvas.create_rectangle(x0,y0,x1,y1, fill=color, width = 0)

def drawPath(app):
    for i in range(app.col):
        for j in range(app.row):
            if (j == 10 or j == 9) and i <= 12:
                app.board[j][i] = False
            elif (i == 12 or i == 11) and 10 < j <= 15:
                app.board[j][i] = False
            elif (j == 15 or j == 14) and 12 < i <= 18:
                app.board[j][i] = False
            elif (i == 18 or i == 17) and j < 15:
                app.board[j][i] = False
            elif i > 23:
                app.board[j][i] = False

def drawMenu(app, canvas):
    size = app.size
    x0 = app.width*(4/5)
    y0 = 0
    x1 = x0 + size*2
    y1 = y0 + size
    canvas.create_rectangle(x0,y0,x1,y1, fill='burlywood3')
    for i in range(2):
        for j in range(7):
            x0 = app.width*(4/5) + i*size
            y0 = (j+1)*size
            x1 = x0 + size
            y1 = y0 + size
            canvas.create_rectangle(x0,y0,x1,y1, fill='burlywood3')
    canvas.create_text(app.width*(4/5)+app.size/2,app.size/2, 
    text = f'Health:\n{app.health}', font="Times 16 bold")
    canvas.create_text(app.width*(4/5)+3*app.size/2,app.size/2, 
    text = f'Money:\n{app.money}', font="Times 16 bold")
    x0 = app.width*(4/5)
    canvas.create_image(x0+ size/2, 3*size/2, 
    image=ImageTk.PhotoImage(app.imageDartMonk))
    canvas.create_image(x0+3*size/2, 3*size/2, 
    image=ImageTk.PhotoImage(app.imageSnipe))
    x1 = x0 + size*2
    y0 = 8*app.size
    y1 = y0+app.size
    canvas.create_rectangle(x0,y0,x1,y1, fill='burlywood3')
    canvas.create_text(x0+size, y0+size/2, text = f'Targeting: {app.targetModeName}', 
    font="Times 16 bold")
    canvas.create_rectangle(x0,y1,x1,y1+size, fill='burlywood3')

def timerFired(app):
    if not app.gameOver:
        targetingTransition(app)
        if app.health == 0 or app.round == 10:
                app.gameOver = True
        for monkey in app.monkey:
            if monkey.placed:
                monkey.timerFired(app)
        if not app.pause:
            app.time += app.timerDelay
            for dart in app.dart:
                dart.timerFired(app)
            if app.time % app.spawnSpeed == 0 and len(app.roundBloons) < app.length:
                num = random.randint(1, 2)
                if num == 1:
                    app.bloons.append(RedBloon(0, app.height//2))
                    app.roundBloons.append(RedBloon(0, app.height//2))
                elif num == 2:
                    app.bloons.append(BlueBloon(0, app.height//2))
                    app.roundBloons.append(BlueBloon(0, app.height//2))
            for bloon in app.bloons:
                demote(app, bloon)
                if bloon.life == 0:
                    app.bloons.remove(bloon)
                bloon.timerFired(app)
                if bloon.y < -bloon.r:
                    app.health -= bloon.damage
                    app.bloons.remove(bloon)
            if len(app.roundBloons) == app.length and app.bloons == []:
                app.round += 1
                app.length += 15
                app.spawnSpeed -= 10
                app.money += app.round + 99
                app.roundBloons = []
                app.pause = True
                app.dart = []

def keyPressed(app, event):
    if event.key == 'Space':
        app.pause = False

def mousePressed(app, event):
    size = app.size
    x0 = app.width*(4/5) 
    y0 = app.size
    x1 = x0 + size
    y1 = y0 + size
    if x0 < event.x < x1 and y0 < event.y < y1:
        if app.money - app.dartMonkPrice > 0:
            app.state = True
            app.monkey.append(DartMonkey(event.x, event.y, app.time))
    v0 = x0 + size
    w0 = y0
    v1 = v0 + size
    w1 = y0 + size
    if v0 < event.x < v1 and w0 < event.y < w1:
        if app.money - app.snipeMonkPrice > 0:
            app.state = True
            app.monkey.append(SniperMonkey(event.x, event.y, app.time))
    x1 = x0 + size*2
    y0 = 8*app.size
    y1 = y0+app.size
    if x0 < event.x < x1 and y0 < event.y < y1:
        app.targetMode += 1
        if app.targetMode > 3:
            app.targetMode = 1

def mouseDragged(app, event):
    if app.state:
        monk = app.monkey[-1]
        monk.x = event.x
        monk.y = event.y

def mouseReleased(app, event):
    if app.state:
        monkey = app.monkey[-1]
        if isLegal(app, event.x, event.y):
            app.money -= app.dartMonkPrice
            monkey.x = event.x
            monkey.y = event.y
            monkey.state = False
            app.state = False
            monkey.placed = True
        else:
            app.monkey.remove(monkey)
            app.state = False

def drawRound(app, canvas):
    x = app.width*4/5 + app.size
    y = app.size*19/2
    if not app.gameOver:
        canvas.create_text(x, y, text = f'Round {app.round}', font = 'Times 20 bold')
    if app.gameOver:
        canvas.create_text(x, y, text = f'Round {app.round - 1}', font = 'Times 20 bold')

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawMenu(app, canvas)
    drawRound(app, canvas)
    for bloon in app.bloons:
        bloon.redraw(app, canvas)
    for monkey in app.monkey:
        monkey.redraw(app, canvas)
        if monkey.state:
            x0 = monkey.x-monkey.r
            y0 = monkey.y-monkey.r
            x1 = x0 + 2*monkey.r
            y1 = y0 + 2*monkey.r
            canvas.create_oval(x0,y0,x1,y1)
    for dart in app.dart:
        dart.redraw(app, canvas)
    if app.health == 0:
        canvas.create_rectangle(app.width//3, app.height//3, 2*app.width//3,
        2*app.height//3, fill='goldenrod',)
        canvas.create_text(app.width//2, app.height//2, text = "Game Over",
        font='Times 50 bold')
    if app.gameOver:
        canvas.create_rectangle(app.width*1/4, app.height*3/8, app.width*3/4, 
            app.height*5/8, fill = 'gold')
        canvas.create_text(app.width/2, app.height/2, text = 'Congratulations! You Won!',
            font = 'Times 20 bold')
    if not app.gameOver:
        if app.pause:
            canvas.create_rectangle(app.width*1/4, app.height*3/8, app.width*3/4, 
            app.height*5/8, fill = 'gold')
            canvas.create_text(app.width/2, app.height/2, text = 'press space to start round',
            font = 'Times 20 bold')

    
    

#Full Screen code from Piazza Post question @2426
runApp(width = 790, height = 790)