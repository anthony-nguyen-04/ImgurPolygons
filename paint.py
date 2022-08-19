from tkinter import *
from tkinter.colorchooser import askcolor
import poly_point_isect
from PolygonChecker import checkPolygon

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    stack_of_points = {}
    counter = 0

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)

        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=1, columnspan=5)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button

        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.c.bind('q', self.wipe)
        
    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y
        self.stack_of_points[self.counter] = (self.old_x, self.old_y)
        self.counter = self.counter + 1

        #print("%s %s" % (str(self.old_x), str(self.old_y)))

    def reset(self, event):
        # print(self.stack_of_points)
        # print(len(self.stack_of_points.values()))
        # print(len(set(self.stack_of_points.values())))
        # if (len(self.stack_of_points.values()) != len(set(self.stack_of_points.values()))):
        #     print("overlap")


        isect = poly_point_isect.isect_polygon(list(self.stack_of_points.values()))
        if len(isect) > 0:
            print("INTERSECTION")
            print(isect)
        else:
            last_point = self.stack_of_points[len(self.stack_of_points) - 1]
            first_point = self.stack_of_points[0]
            paint_color = 'white' if self.eraser_on else self.color

            self.c.create_line(first_point[0], first_point[1], last_point[0], last_point[1],
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)

            print(checkPolygon(self.stack_of_points))


        self.stack_of_points.clear()
        self.old_x, self.old_y = None, None
        self.counter = 0

    def wipe(self, event):
        self.c.delete('all')

if __name__ == '__main__':
    Paint()