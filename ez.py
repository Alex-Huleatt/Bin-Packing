from __future__ import division, print_function, unicode_literals
import pyglet,math,sys,socket,random,time,threading,select,re
from pyglet.gl import *
from pyglet.window import key
from pyglet import font
from pyglet import clock
from pyglet import window
from pyglet import image
from pyglet.window import mouse
from pyglet.window import event

all_windows = []
_keyboard = set({})
_mouse = set({})

class Win(pyglet.window.Window):

    def __init__(self, caption='Window', show_fps=False, verbose=False, width=640, height=480, FPS=60):
        smoothConfig = getSmoothConfig()
        super(Win, self).__init__(fullscreen=False, caption=caption, config=smoothConfig, width=width, height=height)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        pyglet.clock.schedule_interval(self._update, 1.0/FPS)

        self.show_fps = show_fps
        if (show_fps):
            self.fps_display = pyglet.clock.ClockDisplay()
        self.verbose=verbose

        self._entities = set({ })

        '''Callback event functions'''
        self.mousemotion = None
        self.mousepress = None
        self.mouserelease = None
        self.mousedrag = None
        self.keypress = None
        self.keyrelease = None
        self.tock = None

        global all_windows
        all_windows.append(self)

    def __del__(self):
        all_windows.remove(self)
        
    def on_draw(self):
        self.clear()
        for e in self._entities:
            e.render()
        if (self.show_fps):
            self.fps_display.draw()

    '''
    add thing to render
    '''
    def add(self, el):
        self._entities.add(el)

    '''
    remove thing that was being rendered
    '''
    def remove(self, el):
        self._entities.remove(el)

    '''
    win = window that had this event
    posn = (x,y)
    vel = (dx,dy)
    '''
    def on_mouse_motion(self, x, y, dx, dy):
        if self.verbose:
            print("motion")

        if self.mousemotion is not None:
            kwargs = {
            "window":self,
            "posn":(x,y),
            "vel":(dx,dy)
            }
            self.mousemotion(**kwargs)   

    # def on_close(window):
    #     return pyglet.event.EVENT_HANDLED


    '''
    win = window that had this event
    x,y = x and y posn
    buttons = one of ["LEFT","RIGHT","MIDDLE"]
    modifiers = list of keyboard modifiers
    '''
    def on_mouse_press(self, x, y, button, modifiers):
        if self.verbose:
            print("press")
        _mouse.add(_button_string(button))
        if self.mousepress is not None:
            kwargs = {
            "window":self,
            "posn":(x,y),
            "button":_button_string(button),
            "modifiers":key.modifiers_string(modifiers)
            }
            self.mousepress(**kwargs)
   
    '''
    win = window that had this event
    x,y = x and y posn
    buttons = one of ["LEFT","RIGHT","MIDDLE"]
    modifiers = list of keyboard modifiers
    '''
    def on_mouse_release(self, x, y, button, modifiers):
        if self.verbose:
            print("release")
        _mouse.remove(_button_string(button))
        if self.mouserelease is not None:
            kwargs = {
            "window":self, 
            "posn":(x,y), 
            "button":_button_string(button), 
            "modifiers":key.modifiers_string(modifiers)
            }
            self.mouserelease(**kwargs)

    '''
    win = window that had this event
    x,y = x and y posn
    buttons = list of some of ["LEFT","RIGHT","MIDDLE"]
    modifiers = list of keyboard modifiers
    '''
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.verbose:
            print("drag")
        if self.mousedrag is not None:
            kwargs = {
            "window":self, 
            "posn":(x,y), 
            "button":button, 
            "modifiers":key.modifiers_string(modifiers)
            }
            self.mousedrag(**kwargs)

    '''
    win = the window that had this event
    symbol = string representation of pressed key
    modifiers = string of modifiers
    '''
    def on_key_press(self, symbol, modifiers):
        letter = key.symbol_string(symbol)
        if self.verbose:
            print("press:",letter,key.modifiers_string(modifiers))
        _keyboard.add(key.symbol_string(symbol))
        if self.keypress is not None:
            kwargs = {
            "window":self,
            "symbol":key.symbol_string(symbol),
            "modifiers":key.modifiers_string(modifiers)
            }
            self.keypress(**kwargs)

    '''
    win = the window that had this event
    symbol = string representation of pressed key
    modifiers = string of modifiers
    '''
    def on_key_release(self, symbol, modifiers):
        letter = key.symbol_string(symbol)
        if self.verbose: print("release:",letter,key.modifiers_string(modifiers))
        
        _keyboard.remove(key.symbol_string(symbol))
        if self.keyrelease is not None:
            kwargs = {
            "window":self,
            "symbol":key.symbol_string(symbol),
            "modifiers":key.modifiers_string(modifiers)
            }
            self.keyrelease(**kwargs)

    '''
    function needs to accept (win, dt)
    win = window that is getting updated
    dt = time since last update
    '''
    def _update(self, dt):
        if (self.tock is not None):
            self.tock(**{"window":self,"dt":dt})

    '''set all or some of the callbacks'''
    def set_callbacks(self, mousemotion=None, mousepress=None, mouserelease=None, mousedrag=None, keypress=None, keyrelease=None, tock=None):
        self.mousemotion = mousemotion
        self.mousepress = mousepress
        self.mouserelease = mouserelease   
        self.mousedrag = mousedrag
        self.keypress = keypress
        self.keyrelease = keyrelease
        self.tock = tock

class Ent():
    None

def _button_string(button):
    if (button == pyglet.window.mouse.LEFT):
        return str('LEFT')
    elif (button == pyglet.window.mouse.RIGHT):
        return str('RIGHT')
    elif (button == pyglet.window.mouse.MIDDLE):
        return str('MIDDLE')
        
def runWin():pyglet.app.run()

def is_pressed(symbol, mouse=False):
    if (mouse):
        return symbol in _mouse
    return (symbol in _keyboard)


#PRIMITIVES.PY
"""
Implementing 2D drawing primitives using
pyglet.gl
copyright 2007 by Flavio Codeco Coelho
originally primitives.py
"""
class Base(object):
    """
    Basic attributes of all drawing primitives
    """
    def __init__(self, x, y, z=0, color=(0.,0.,0.,1.), stroke=0, rotation=0):
        try :
            self.rect
        except AttributeError:
            self.rect = Rect(x,y,1,1) # this inits x,y and loc as well
        self.visible = 1 #
        self.z = z 
        self.rotation = rotation
        self.stroke = stroke
        self.color = color
        self.q = gluNewQuadric()
    def setLoc(self, p) : self.rect.loc = p 
    def getLoc(self) : return self.rect.loc
    def setX(self, x) : self.rect.x = x 
    def getX(self) : return self.rect.x 
    def setY(self, y) : self.rect.y = y 
    def getY(self) : return self.rect.y
    loc = property(getLoc, setLoc)
    x = property(getX, setX)
    y = property(getY, setY)
    def setWidth(self,w) : self.rect.width = w
    def getWidth(self) : return self.rect.width
    def setHeight(self, h) : self.rect.height = h
    def getHeight(self) : return self.rect.height
    width = property(getWidth, setWidth)
    height = property(getHeight, setHeight)
        
class Pixel(Base):
    """ A pixel at a given x,y,z position and color.
        Pixel(x=12, y=100, z=900, color=(1,0,0,0.5))
    """
    def render(self):
        """
            Draws a pixel at a given x and y with given color .
            Color = 3 or 4 arg tuple. RGB values from 0 to 1 being 1 max value (1, 1, 1) would be white
        """
        glColor4f(*self.color)
##        glDisable(GL_TEXTURE_2D) # disable in case it was on
            
        glPushMatrix() # remember previous matrix state before translating, rotating
        glTranslatef(self.x, self.y, -self.z) # translate to point to draw

        glBegin(GL_POINTS) # draw point
        glVertex3f(0.0, 0.0, 0.0)
        glEnd()

        glPopMatrix() # back to previous matrix state

    def intersects(self, x,y):
        if x==self.x and y==self.y : return True

class Circle(Base):
    """ Circle class
        Circle(x=20, y=100, z=1, width=300, color=(1,1,0,0.3), stroke=5, rotation=0, style=GLU_FILL)
        style choices are : GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT
    """
    def __init__(self, x=10, y=10, z=0, width=2, color=(0,0,0,1), stroke=0, rotation=0.0, style=GLU_FILL):
        self.radius = width*0.5
        self.rect = Rect(x, y, width, width)
        self.style = style
        self.circleresolution = 60
        Base.__init__(self, x,y,z,color, stroke, rotation)
        
    def setWidth(self, w):
        self.radius = w*0.5
        self.rect.width = w
    width = property(Base.getWidth, setWidth)
        
    def render(self):
        """ Draw Circle
            x, y, z, width in pixel, rotation, color and line width in px
            style choices are : GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT
            TO DO : textured circles
        """
        
        glColor4f(*self.color)
        glPushMatrix()

        glTranslatef(self.x, self.y, -self.z)
        glRotatef(self.rotation, 0, 0, 0.1)


        if self.radius < 1 : self.radius = 1

        if self.stroke :
            inner = self.radius - self.stroke # outline width
            if inner < 0: inner=0
        else :
             inner = 0 # filled
        
        gluQuadricDrawStyle(self.q, self.style)

        gluDisk(self.q, inner, self.radius, self.circleresolution, 1) # gluDisk(quad, inner, outer, slices, loops)
            
        glPopMatrix()



class Arc(Base):
    """ Arc class
        Arc(x=10, y=10, z=0, radius=1, start=0, sweep=1, color=(0,0,0,1), stroke=0, rotation=0.0, style=GLU_FILL)
        style choices are : GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT
    """
    def __init__(self, x=10, y=10, z=0, radius=1, start=0, sweep=1, color=(0,0,0,1), stroke=0,
                 rotation=0.0, style=GLU_FILL):

        Base.__init__(self, x,y,z,color, stroke, rotation)
        self.radius = radius
        self.start = start
        self.sweep = sweep
        self.style = style
        self.circleresolution = 60
        
    def render(self):
        """
        Draws Arc
        """
        glColor4f(*self.color)
        glPushMatrix()

        glTranslatef(self.x, self.y, -self.z)
        glRotatef(self.rotation, 0, 0, 0.1)

        if self.stroke : 
            inner = self.radius - self.stroke
            if inner < 0: inner=0
        else :
            inner = 0 # full, no inner
        self.start -= 180
        
        gluQuadricDrawStyle(self.q, self.style)
        
        gluPartialDisk(self.q, inner, self.radius, self.circleresolution, 1, self.start, self.sweep)
        
        glPopMatrix()



class Polygon(Base):
    def __init__(self, v, z=0, color=(0,0,0,1), stroke=0, rotation=0.0, style=0):
        """ polygon class
            Polygon(vertexarray=[(0, 0), (29, 100), (30, 200)], z=100, color=(0,0.3,0.1,1), stroke=0, rotation=23)
            overwrites few methods from superclass as polygons are more complex, needs to update everyvertex.
        """
        self.v = v
        l, t, r, b = calcPolygonRect(v) # get the bounding rect
        self.rect = Rect(l+(r-l)*0.5, t+(b-t)*0.5, r-l, b-t)
        self.v2 = [(i[0] - self.rect.x, i[1] - self.rect.y) for i in v] #relative polygon

        self.style = style
        
        Base.__init__(self, self.rect.x, self.rect.y, z,color,stroke,rotation)

    def updateV(self):
        self.v = [(self.rect.x + n[0], self.rect.y + n[1]) for n in self.v2]

    def setLoc(self, p):
        self.rect.loc = p ; self.updateV()
    def setX(self, x):
        self.rect.x = x ; self.updateV()
    def setY(self, y):
        self.rect.y = y; self.updateV()
    x = property(Base.getX, setX)
    y = property(Base.getY, setY)
    loc = property(Base.getLoc, setLoc)
    
    def render(self):
        """ Draw Polygon
            v is an array with tuple points like [(x, y), (x2, y2), (x3, y3)]
            min vertex number to draw a polygon is 3
            stroke=0 to fil with color the inside of the shape or stroke=N just to draw N-px thick outline.
            Note. It doesnt work with non convex polygons, need to implement tesselation yet
        """
        l,t,r,b = calcPolygonRect(self.v)
        x,y = calcRectCenter(l,t,r,b)
        self.drawVertex(x, y, self.z, [(i[0] - x, i[1] - y) for i in self.v], self.color, self.stroke, self.rotation, self.style)

    
    def drawVertex(self, x, y,  z=0, v=(), color=(0,0,0,1), stroke=0, rotation=0.0,   style=0):
        
        glColor4f(*self.color)    
        glPushMatrix()

        glTranslatef(x, y, -z)
        glRotatef(self.rotation, 0, 0, 0.1)

        if self.style :
            glEnable(GL_LINE_STIPPLE)
            glLineStipple(1, style)
##        else :
##            glDisable(GL_LINE_STIPPLE)
##            0xF0F0 # dashed line
##            0xF00F # long dashed line
##            0x8888 # dotted lines
##        glRect(x1,y,1,x1,x2)
##        glRectiv(v1,v2) # oposite vertex of rectangle
        # -- start drawing
        if self.stroke : # outlined polygon
            glLineWidth(self.stroke)
            glBegin(GL_LINE_LOOP)
        else: # filled polygon
            if   len(v) == 4 : glBegin(GL_QUADS)
            elif len(v)  > 4 : glBegin(GL_POLYGON)
            else :             glBegin(GL_TRIANGLES) # which type of polygon are we drawing?

        for p in v:
            glVertex3f(p[0], p[1],0)  # draw each vertex

        glEnd()
        # -- end drawing
        
        if self.style : glDisable(GL_LINE_STIPPLE)
        
        glPopMatrix()


class LineRel(Base):
    def __init__(self, x,y, a=(0,0), b=(0,0), z=0, color=(0,0,0,1), stroke=0, rotation=0.0, style=0):
        """ Draws a basic line given the begining and end point (tuples), color (tuple) and stroke
            (thickness of line)
            Line( x,y, a=(1,1), b=(100,100), z=0, color=(0.2,0,0,1), stroke=10, rotation=45)
        """
        w = (b[0] - a[0]) 
        h = (b[1] - a[1]) 
        x = abs(a[0] + w*0.5)
        y = abs(a[1] + h*0.5)
        self.a2 = abs(a[0]) - x, abs(a[1]) - y
        self.b2 = abs(b[0]) - x, abs(b[1]) - y
        self.a = x - w*0.5, y - w*0.5
        self.b = x + w*0.5, y + w*0.5
        self.rect = Rect(x, y, w, h)
        self.style = style
        Base.__init__(self, x, y, z,color,stroke,rotation)

    def render(self):
        """
        Draws Line
        """
        p1 = self.a2
        p2 = self.b2
        glColor4f(*self.color)
        color  = (GLfloat *4)(*self.color)
               
        glPushMatrix()

        glTranslatef(self.x, self.y, -self.z) # translate to GL loc ppint
        glRotatef(self.rotation, 0, 0, 0.1)

        if self.style :
            glEnable(GL_LINE_STIPPLE)
            glLineStipple(1, self.style)
##        else :
##            glDisable(GL_LINE_STIPPLE)
            
        if self.stroke <= 0:
            self.stroke = 1
        glLineWidth(self.stroke)

        glBegin(GL_LINES)
        glVertex2i(int(p1[0]), int(p1[1])) # draw pixel points
        glVertex2i(int(p2[0]), int(p2[1]))
        glEnd()

        if self.style :
            glDisable(GL_LINE_STIPPLE)
        
        glPopMatrix()


    def updateAB(self):
        self.a = self.x + self.a[0], self.y + self.a[0]
        self.b = self.x + self.b[0], self.y + self.b[0]

    def setLoc(self, p):
        self.rect.loc = p ; self.updateAB()
    def setX(self, x):
        self.rect.x = x ; self.updateAB()
    def setY(self, y):
        self.rect.y = y; self.updateAB()
    x = property(Base.getX, setX)
    y = property(Base.getY, setY)
    loc = property(Base.getLoc, setLoc)


class Line(LineRel):
    def __init__(self, a=(0,0), b=(0,0), z=0, color=(0,0,0,1), stroke=0, rotation=0.0, style=0):
        """ Draws a basic line given the begining and end point (tuples), color (tuple) and stroke
            (thickness of line)
            Line( a=(1,1), b=(100,100), z=20, color=(0.2,0,0,1), stroke=10, rotation=45)
        """
        w = (b[0] - a[0]) 
        h = (b[1] - a[1]) 
        x = abs(a[0] + w*0.5) # abs x,y
        y = abs(a[1] + h*0.5)
        a = x-w*0.5, y-h*0.5 # relative a,b
        b = x+w*0.5, y+h*0.5
        LineRel.__init__(self, x, y, a, b, z, color, stroke, rotation, style)

        

# intersectable shapes (draggable)

class Rect(object):
    def __init__(self, x=0,y=0,w=0,h=0):
        """ rect(self, x=0,y=0,w=0,h=0)
            x,y,loc, width, height
            left,top,right,bottom
            quad ->
            --------------------
            topleft = quad[0]
            topright = quad[1]
            bottomright = quad[2]
            bottomleft = quad[3]
        """
        self.rect = x,y,w,h

    def setRect(self, r):
        self.__x = r[0]
        self.__y = r[1]
        self.__width = r[2]
        self.__height = r[3]
        w = r[2]*0.5 ; h = r[3]*0.5
        self.__rect = r[0]-w, r[1]-h, r[0]+w, r[1]+h # l t r b
    def getRect(self):
        return self.__rect
    rect = property(getRect, setRect)

    def setQuad(self, q): # [ q[0][0], q[0][1], q[1][0], q[2][1] ] # l t r b
        self.rect = q[0][0]+(q[1][0]-q[0][0])*0.5, q[0][1]+(q[2][1]-q[0][1])*0.5, q[1][0]-q[0][0], q[2][1]-q[0][1] 
    def getQuad(self):
        return [(self.rect[0], self.rect[1]),(self.rect[2], self.rect[1]),(self.rect[2], self.rect[3]),(self.rect[0], self.rect[3])] # tl tr br bl
    quad = property(getQuad, setQuad)

    def setX(self, x):
        self.rect = x, self.y, self.width, self.height
    def getX(self) : return self.__x
    x = property(getX, setX)

    def setY(self, y):
        self.rect = self.x, y, self.width, self.height
    def getY(self) : return self.__y
    y = property(getY, setY)

    def setLoc(self, p):
        self.rect = p[0], p[1], self.width, self.height
    def getLoc(self) : return self.__x, self.__y # self.x, self.y
    loc = property(getLoc, setLoc)

    def setWidth(self, w):
        self.rect = self.x, self.y, w, self.height
    def getWidth(self): return self.__width
    width = property(getWidth, setWidth)
    
    def setHeight(self, h):
        self.rect = self.x, self.y, self.width, h
    def getHeight(self): return self.__height
    height = property(getHeight, setHeight)

    def setLeft(self,x):
        self.rect = x+self.width*0.5, self.y, self.width, self.height
    def getLeft(self): return self.rect[0]
    left = property(getLeft, setLeft)
    
    def setTop(self,y):
        self.rect = self.x, y+self.width*0.5, self.width, self.height
    def getTop(self): return self.rect[1]
    top = property(getTop, setTop)
    
    def setRight(self,x):
        self.rect = x-self.width*0.5, self.y, self.width, self.height
    def getRight(self): return self.rect[2]
    right = property(getRight, setRight)
    
    def setBottom(self,x):
        self.rect = self.x, y-self.width*0.5, self.width, self.height
    def getBottom(self): return self.rect[3]
    bottom = property(getBottom, setBottom)


def calcPolygonRect(pointArray):
    """ receives a point list and returns the rect that contains them as a tupple -> tuple left, top, right, bottom
    """
    # init to ridiculously big values. not very elegant or eficient
    l, t, r, b = 10000000, 10000000, -10000000, -10000000
##    l = pointArray[0]
##    t = pointArray[1]
##    r = l
##    b = t

    for n in pointArray: # calc bounding rectangle rect
        if n[0] < l : l = n[0]
        if n[0] > r : r = n[0]
        if n[1] < t : t = n[1]
        if n[1] > b : b = n[1]

    return l, t, r, b


def calcRectCenter(l,t,r,b):#,v=()):
    """ returns rect center point -> x,y
        calcRectCenter(l,t,r,b)
    """
##    if len(v) : l,t,r,b = v[0],v[1],v[2],v[3]
    return l+((r-l)*0.5), t+((b-t)*0.5)

'''
end primitives.py
'''

#UTILS.PY
'''
begin utils.py
pyglet.utils.py
02
www.akeric.com - 2011-03-17

'''

def screenshot(name='screenshot'):
    """
    Take a screenshot

    Parameters:
    name : string : Default 'screenshot'.  Name of the saved image.  Will
        always save as .png
    """
    # Get the 'the back-left color buffer'
    pyglet.image.get_buffer_manager().get_color_buffer().save('%s.png'%name)

def getPixelValue(x, y):
    """
    Return the RGBA 0-255 color value of the pixel at the x,y position.
    """
    # BufferManager, ColorBufferImage
    color_buffer = pyglet.image.get_buffer_manager().get_color_buffer()
    # AbstractImage, ImageData, sequece of bytes
    pix = color_buffer.get_region(x,y,1,1).get_image_data().get_data("RGBA", 4)
    return pix[0], pix[1], pix[2], pix[3]

def drawPoint(x, y, color):
    """
    Based on the (r,g,b) color passed in, draw a point at the given x,y coord.
    """
    pyglet.graphics.draw(1, GL_POINTS,
                         ('v2i', (x, y)),
                         ('c3B', (color[0], color[1], color[2]) ) )

def getSmoothConfig():
    """
    Sets up a configuration that allows of smoothing\antialiasing.
    The return of this is passed to the config parameter of the created window.
    """
    try:
        # Try and create a window config with multisampling (antialiasing)
        config = Config(sample_buffers=1, samples=4,
                        depth_size=16, double_buffer=True)
    except pyglet.window.NoSuchConfigException:
        print("Smooth contex could not be aquiried.")
        config = None
    return config

def printEvents(window):
    """
    Debug tool that will print the events to the console.

    window is an instance of a Window object receiving the events.
    """
    window.push_handlers(pyglet.window.event.WindowEventLogger())

def playMusic(music):
    """
    Simple wrapper to play a music (mp3) file.

    music : music file relative to application.
    """
    music = pyglet.resource.media(music)
    music.play()

def setBackgroundColor(color):
    """
    Color is a list of four values, [r,g,b,a], each from 0 -> 1
    """
    pyglet.gl.glClearColor(*color)

'''
end utils.py
'''

#Geometry TODO
def _seg_seg_intersect(a1,a2,b1,b2):
    pass

def _line_seg_intersect(center,vect, p1,p2):
    pass

def _point_in_poly(p, verts):
    pass

def _poly_poly_collision(aVerts, bVerts):
    pass



#Client
class Client():

    def __init__(self,ip,port):
        self._kill = False
        self._ip = ip
        self._port = port

        server_address = (ip, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(0)
        rec_th = threading.Thread(target=rec,args=(ih,sock))
        rec_th.start()
        rec_th.join()

    def rec(self,callback,sock):
        while not self._kill:
            try:
                data, server = sock.recvfrom(4096)
            except:
                continue
            callback(data)
        

    def send(self, st, sock):
        while 1:
            try: 
                sent = sock.sendto(st, server_address)
            except:
                continue #sorrynotsorry

    def kill(self):

        self._kill = True

#Server
class Server():


    def __init__(self,port): #callback gotta have sig callback(serverenum, data)
        signal.signal(signal.SIGINT, signal_handler)
    
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(0)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to the port
        self.server_address = ('', port)
        print >>sys.stderr, 'starting up on %s port %s' % server_address
        sock.bind(self.server_address)
        self.usrs = {}
        self.user_ids = {}
        self._kill = False
        self.id_num = 0

        self.nu_fun = None
        self.receive_fun = None
        self.timeout_fun = None

    def set_new_user_fun(self,fun):
        self.nu_fun = fun

    def set_receive_fun(self,fun):
        self.receive_fun = fun
    
    def set_timeout_fun(self,fun):
        self.timeout_fun = fun

    def rec(self):
        r = re.compile('\s')
        while not kill:
            try:
                data, address = sock.recvfrom(4096)
            except:
                if (kill):
                    return
                continue
            if (address not in usrs):
                user_ids[address]=id_num

                if (self.nu_fun is not none):
                    self.nu_fun(id_num) #send new user id.

                id_num += 1

            usrs[address]=time.time() #update user's age.

            if (self.receive_fun is not null):
                self.receive_fun(self.user_ids[address], data) #send id and data

    def start(self):
        threading.Thread(target=rec).start()

    def _signal_handler(signal, frame):
        sock.close()
        self._kill = True
        sys.exit(0)

    def send(self, message):
        toPop=[]
        for u in usrs:
            if (t - usrs[u] > 1000):
                toPop.append(u)
                if (self.timeout_fun is not none):
                    self.timeout_fun(user_ids[u]) #send address of person.
            else:
                sent = sock.sendto(message, u)
        for u in toPop:
            usrs.pop(u,None)

    def kill(self):
        self._kill=True
