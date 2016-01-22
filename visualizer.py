import ez, random
from pyglet.gl import *

def generateRandomColor(mix):
    red = (random.randint(0,256)+mix[0])/2
    green = (random.randint(0,256)+mix[1])/2
    blue = (random.randint(0,256)+mix[2])/2
    
    return (red/255.0, green/255.0, blue/255.0,1)

def visualize(sizes, posns):

    win = ez.Win(caption="visualizer")
    width, height = win.width, win.height
    min_x, max_x, min_y, max_y = getSolDim(sizes,posns)

    dx, dy = max_x-min_x, max_y-min_y

    x_rat, y_rat = dx / width, dy / height
    if (x_rat > y_rat): #need to scale down x
        mul = x_rat
    else: #scale down y
        mul = y_rat

    rects = []
    for i in range(len(sizes)):
        x,y = (posns[i][0] - min_x) / mul, height - (posns[i][1]-min_y)/mul

        w,h = sizes[i][0] / mul, sizes[i][1] / mul
        win.add( ez.Polygon(v=[(x,y), (x+w,y), (x+w,y-h), (x,y-h)], color=generateRandomColor( (50,50,50) ), style=GLU_FILL) )

    ez.runWin()

def getSolDim(sizes, posns):
    min_x, min_y = posns[0]
    max_x, max_y = posns[0]
    for i in range(len(sizes)):
        min_x,min_y = min(posns[i][0],min_x), min(posns[i][1],min_y)
        max_x, max_y = max(posns[i][0]+sizes[i][0],max_x),max(posns[i][1]+sizes[i][1],max_y)
    return ( min_x, max_x, min_y, max_y )


