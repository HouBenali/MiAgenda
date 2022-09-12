import tkinter as tk
from HoverButton import HoverButton


class Table(tk.Frame):
    def __init__(self, parent, rows, columns):
        self.n = rows
        self.m = columns
        # use black background so it "peeks through" to 
        # form grid lines
        self.labels = []
        tk.Frame.__init__(self, parent, background="black")
        print(rows)
        if rows <= 10:
            rows = 10

        for row in range(rows):
            current_row = []
            fg = "black"
            width = 10
            cursor = "hand2"
            # self.print()
            if row % 2:
                bg = "lightgrey"
            else:
                bg = "white"
            for column in range(columns):
                # print(columns)
                if column == 0:
                    width = 5
                elif column == 1:
                    width = 15
                elif column == 2:
                    width = 30
                elif column == 3:
                    width = 10
                elif column == 4:
                    width = 10
                elif column == 5:
                    width = 5
                elif column == 6:
                    width = 4

                mylabel = HoverButton(self, self.labels, text=" ", borderwidth=0, width=width, height=2, bg=bg, fg=fg,
                                      activebackground="yellow", cursor=cursor)
                mylabel.row_number = row
                mylabel.col_number = column
                mylabel.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                if row != 0 and column == self.m - 1 and row <= self.n - 1:
                    mylabel.config(text="Edit")
                elif row == 0:
                    bg = "#B22222"
                    fg = "white"
                    cursor = "arrow"
                    mylabel = tk.Label(self, text=" ", borderwidth=0, width=width, height=2, bg=bg, fg=fg,
                                       cursor=cursor)
                    mylabel.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                else:
                    mylabel.config(text=column)

                current_row.append(mylabel)
            self.labels.append(current_row)

    def set(self, row, column, value):
        widget = self.labels[row][column]
        try:
            widget.config(text=value)
        except:
            print("An exception occurred")

    def get(self, i, j):
        return self.labels[i][j]

    def print(self):
        for i in range(len(self.labels)):
            print()
            for j in range(len(self.labels[i])):
                print(self.get(i, j).cget("text"), end='')
                print('      ', end='')
        print()


class ExampleApp(tk.Tk):
    def __init__(self):
        n = 5
        m = 5
        tk.Tk.__init__(self)
        t = Table(self, n, m)
        t.pack(side="top")
        t.set(2, 0, "Hello")
        t.set(0, 1, "Bye")
        t.print()


if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()
