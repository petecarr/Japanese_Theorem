#!/usr/bin/python
# In geometry, the Japanese theorem states that the centers of the 
# incircles of certain triangles inside a cyclic quadrilateral are 
# vertices of a rectangle.
# Theorem may have actually come from China but, apparently, Japanese
# people during the early 19th Century used to do geometry for fun and one
# of them (anonymously) came up with this. The problem or solution
# was written on a wooden tablet and placed as an offering at a Shinto 
# shrine. 
# There is also a theory of cyclic polygons.

from tkinter import *
from math import sqrt

CANVASWIDTH=600
CANVASHEIGHT=CANVASWIDTH
cx = CANVASWIDTH
cy = CANVASHEIGHT

BGCOLOR="black"
LINECOLOR="green"
linecolor=LINECOLOR
colors = ("red", "orange", "yellow", "green", "cyan", "blue", "magenta")


# Nice 345 triangles to start with
A = [cx/6, cy/4]      #[100,150]
B = [cx-cx/6, cy/4]   #[500,150]
C = [cx-cx/6, cy*3/4] #[500,450]
D = [cx/6, cy*3/4]    #[100,450]
Ox = cx/2    # 300
Oy = cy/2
R = (cx-cx/6)/2  # 250

global inner_q
inner_q = [0,0,0,0,0,0,0,0]

#----------------------------------------------------------------------------
def rect(x1,y1,x2,y2,x3,y3,x4,y4):
    # compare diagonals - leave a little slack
    l1 = sqrt((x3-x1)*(x3-x1) +(y3-y1)*(y3-y1))
    l2 = sqrt((x4-x2)*(x4-x2) +(y4-y2)*(y4-y2))
    if abs(l2-l1) >= 2:
        # If you see this the program is wrong (or inaccurate)
        print("Not a rectangle")
        print("Diagonal difference ={0:.1f}-{1:.1f}={2:.1f}".format(
                                             l2,l1,abs(l2-l1)))
    return abs(l2-l1) < 2

def inscribe_circle(A,B,C):
    bcx = B[0]-C[0]
    bcy = B[1]-C[1]
    a = sqrt(bcx*bcx+bcy*bcy)
    acx = A[0]-C[0]
    acy = A[1]-C[1]
    b = sqrt(acx*acx+acy*acy)
    bax = B[0]-A[0]
    bay = B[1]-A[1]
    c = sqrt(bax*bax+bay*bay)
    p = a+b+c
    halfp = p/2.0
    # Center of incircle
    x = (a*A[0] +b*B[0] +c*C[0])/p
    y = (a*A[1] +b*B[1] +c*C[1])/p
    # Heron's method 
    area = sqrt(halfp*(halfp-a)*(halfp-b)*(halfp-c))
    r = 2.0*area/p
    #print("a={0:.0f}, b={1:.0f}, c={2:.0f}".format(a,b,c))
    #print("perimeter = {0:.0f}".format(p))
    #print("x={0:.0f}, y={1:.0f}, area={2:.0f}, r={3:.0f}".format(x,y,area,r))
    return int(x),int(y),int(r) 

def draw(canvas):
    global linecolor
    
    canvas.delete(ALL)
    canvas.create_oval(50,50,550,550, outline = "blue")
    canvas.create_polygon(A[0],A[1],B[0],B[1],C[0],C[1],D[0],D[1], 
                          fill="", outline=linecolor)

    canvas.create_text(A[0],A[1],offset="-20,-10", fill="red", text="A")
    canvas.create_text(B[0],B[1],offset="20,-10",  fill="red", text="B")
    canvas.create_text(C[0],C[1],offset="20,10",   fill="red", text="C")
    canvas.create_text(D[0],D[1],offset="-20,10",  fill="red", text="D")

    canvas.create_line(A[0],A[1],C[0],C[1], fill = linecolor)
    canvas.create_line(B[0],B[1],D[0],D[1], fill = linecolor)

    x1,y1,r1 = inscribe_circle(A,B,C)
    canvas.create_oval(x1+r1,y1+r1,x1-r1,y1-r1, outline = "orange")
    x2,y2,r2 = inscribe_circle(B,C,D)
    canvas.create_oval(x2+r2,y2+r2,x2-r2,y2-r2, outline = "orange")
    x3,y3,r3 = inscribe_circle(C,D,A)
    canvas.create_oval(x3+r3,y3+r3,x3-r3,y3-r3, outline = "orange")
    x4,y4,r4 = inscribe_circle(D,A,B)
    canvas.create_oval(x4+r4,y4+r4,x4-r4,y4-r4, outline = "orange")

    canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,
                          outline="blue", fill="")
    global inner_q
    inner_q = [x1,y1,x2,y2,x3,y3,x4,y4]
            

def vertex(x,y):
    dx = 10
    dy = 10

    if x < (A[0]+dx) and x > (A[0]-dx) and y < (A[1]+dy) and y> (A[1]-dy):
        return 1
    elif x < (B[0]+dx) and x > (B[0]-dx) and y < (B[1]+dy) and y> (B[1]-dy):
        return 2
    elif x < (C[0]+dx) and x > (C[0]-dx) and y < (C[1]+dy) and y> (C[1]-dy):
        return 3
    elif x < (D[0]+dx) and x > (D[0]-dx) and y < (D[1]+dy) and y> (D[1]-dy):
        return 4
    else:
        return 0


def fix_on_circle(x, y):
    # Wherever you release the mouse button keep the same angle but 
    # make sure it is on the circle defined by Ox, Ox, R
    # i.e. snap the quadrilateral back to being cyclic 
    # Current radius
    CR = sqrt((x-Ox)*(x-Ox)+(y-Oy)*(y-Oy))
    if abs(CR-R) < 1:
        return x,y
    xr = Ox+ (x-Ox)*R/CR
    yr = Oy+ (y-Oy)*R/CR
    return xr,yr


def quitNow():
    global root
    root.destroy()

#--------------------------------------------------------------------------


def key(event):
    if (event.keysym == 'Escape'):
        print("Pressed Escape, quitting")
        quitNow()
    #elif (event.keycode == <Print>):  #doesn't work
        #print("Print")
    else:
        print ("pressed", repr(event.keysym))
        print ("pressed", repr(event.keycode))


def callback_click(event):
    global v
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    canvas.focus_set()
    #print ("clicked at", event.x, event.y)
    # these will be the same unless the display becomes more complex
    #print ("canvas coords at", x, y)

    v = vertex(x,y)

def callback_motion(event):
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    #print ("motion to", event.x, event.y)
    global v
    #print("vertex ", v)
    if v > 0:
        if v == 1:
            A[0] = x
            A[1] = y
        elif v == 2:
            B[0] = x
            B[1] = y
        elif v == 3:
            C[0] = x
            C[1] = y
        elif v == 4:
            D[0] = x
            D[1] = y
    draw(canvas)

def callback_release(event):
    global v
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    #print ("released at", event.x, event.y)
    #print("vertex ", v)
    x,y = fix_on_circle(x, y)
    #print("fix_on_circle at x={0:.0f}, y={1:.0f}".format(x,y))
    if v > 0:
        if v == 1:
            A[0] = x
            A[1] = y
        elif v == 2:
            B[0] = x
            B[1] = y
        elif v == 3:
            C[0] = x
            C[1] = y
        elif v == 4:
            D[0] = x
            D[1] = y
    draw(canvas)
    is_r = rect(inner_q[0],inner_q[1],inner_q[2], inner_q[3],
                inner_q[4],inner_q[5],inner_q[6], inner_q[7])
    v = 0

#--------------------------------------------------------------------------



def main():
    global root
    root = Tk()
    cf = Frame(root, borderwidth=4, relief=RAISED)
    cf.pack(side =LEFT)
    cf.master.title("Japanese Theorem for a Cyclic Quadrilateral")

    global canvas
    canvas = Canvas(cf, width = CANVASWIDTH, height = CANVASHEIGHT, bg=BGCOLOR)
    canvas.pack()
    canvas.bind("<Key>", key)
    canvas.bind("<Button-1>", callback_click)
    canvas.bind("<B1-Motion>", callback_motion)
    canvas.bind("<ButtonRelease-1>", callback_release)
    draw(canvas)

    root.mainloop()


if __name__ == '__main__':
    main()

