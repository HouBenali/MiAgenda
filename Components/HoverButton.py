import tkinter as tk
import constant


class HoverButton(tk.Button):

    def __init__(self, master, labels, **kw):
        super().__init__(master=master, **kw)
        self.labels = labels
        self.row_number = 0
        self.col_number = 0
        self.precolor = "lightblue"
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_enter(self, e):
        for b in self.labels[self.row_number]:
            self.precolor = b['background']
            b['background'] = self['activebackground']

    def on_click(self, e):
        constant.this_row = self.row_number
        print(constant.this_row, "+++++++++++++")

    def on_leave(self, e):
        for b in self.labels[self.row_number]:
            b['background'] = self.precolor
