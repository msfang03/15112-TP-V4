# from cmu_112_graphics import *

# def appStarted(app): 
#     app.messages = ['appStarted']

# def appStopped(app):
#     app.messages.append('appStopped')
#     print('appStopped!')

# def keyPressed(app, event):
#     app.messages.append('keyPressed: ' + event.key)

# def keyReleased(app, event):
#     app.messages.append('keyReleased: ' + event.key)

# def mousePressed(app, event):
#     app.messages.append(f'mousePressed at {(event.x, event.y)}')

# def mouseReleased(app, event):
#     app.messages.append(f'mouseReleased at {(event.x, event.y)}')

# def mouseMoved(app, event):
#     app.messages.append(f'mouseMoved at {(event.x, event.y)}')

# def mouseDragged(app, event):
#     app.messages.append(f'mouseDragged at {(event.x, event.y)}')

# def sizeChanged(app):
#     app.messages.append(f'sizeChanged to {(app.width, app.height)}')

# def redrawAll(app, canvas):
#     font = 'Arial 20 bold'
#     canvas.create_text(app.width/2,  30, text='Events Demo',
#                        font=font, fill='black')
#     n = min(10, len(app.messages))
#     i0 = len(app.messages)-n
#     for i in range(i0, len(app.messages)):
#         canvas.create_text(app.width/2, 100+50*(i-i0),
#                            text=f'#{i}: {app.messages[i]}',
#                            font=font, fill='black')

# runApp(width=600, height=600)

# from cmu_112_graphics import *

# def appStarted(app):
#     app.counter = 0

# def timerFired(app):
#     app.counter += 1

# def redrawAll(app, canvas):
#     canvas.create_text(200,  50,
#                        text='Keyboard Shortcut Demo', fill='black')
#     canvas.create_text(200, 100,
#                        text='Press control-p to pause/unpause', fill='black')
#     canvas.create_text(200, 150,
#                        text='Press control-s to save a snapshot', fill='black')
#     canvas.create_text(200, 200,
#                        text='Press control-q to quit', fill='black')
#     canvas.create_text(200, 250,
#                        text='Press control-x to hard exit', fill='black')
#     canvas.create_text(200, 300, text=f'{app.counter}', fill='black')

# runApp(width=400, height=400) # quit still runs next one, exit does not
# runApp(width=600, height=600)

# This demos using image.size

from cmu_112_graphics import *

def appStarted(app):
    url = 'https://blog.knife-depot.com/wp-content/uploads/2020/03/shuriken-676x676.png'
    app.image1 = app.loadImage(url)
    app.image2 = app.scaleImage(app.image1, 1/26)

def drawImageWithSizeBelowIt(app, canvas, image, cx, cy):
    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(image))
    imageWidth, imageHeight = image.size
    msg = f'Image size: {imageWidth} x {imageHeight}'
    canvas.create_text(app.width//2, app.height//2,
                       text=msg, font='Arial 20 bold', fill='black')

def redrawAll(app, canvas):
    #drawImageWithSizeBelowIt(app, canvas, app.image1, 400, 300)
    drawImageWithSizeBelowIt(app, canvas, app.image2, 385, 
    app.height//2)
    canvas.create_text(385, app.height//2 + 30, text = 'hi', font = 'Times 28 bold')

runApp(width=1000, height=792)