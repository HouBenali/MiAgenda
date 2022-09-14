import tkinter as tk

class HoverButton(tk.Button):

    def __init__(self, master, labels, **kw):
        super().__init__(master=master, **kw)
        self.labels = labels
        self.row_number = 0
        self.col_number = 0
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        # self['background'] = self['activebackground']
        for b in self.labels[self.row_number]:
            b['background'] = self['activebackground']

    def on_leave(self, e):
        # self['background'] = self.defaultBackground
        for b in self.labels[self.row_number]:
            b['background'] = self.defaultBackground
