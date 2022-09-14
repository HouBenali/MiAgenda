import tkinter
from tkinter import *
import sqlite3
from sqlite3 import Error


# ----------------------------------------------------------------------

class SearchBar:

    def __init__(self, root):
        frame = Frame(root, width=500, height=500)
        # root.minsize(300,300)
        frame.pack()

        # here we make  text input field

        self.E1 = Entry(frame, bd=2)
        self.E1.pack(side=TOP)

        # here the list generated from entry but covering it completely is bad ??

        self.Lb1 = Listbox(frame, bd=2)
        self.Lb2 = Listbox(frame, bd=4)
        # Lb1.pack(side=BOTTOM)

        root.bind("<Key>", self.clickme)

        # open database (only once) at start program
        self.db = sqlite3.connect('../DB/agenda.db')

    # -------------------

    def __del__(self):
        # close database on exit
        self.db.close()

    # -------------------

    def clickme(self, x):

        txt = self.E1.get()

        self.Lb1.delete(0, END)  # delete all on list

        if txt == '':
            self.Lb1.pack_forget()  # hide list
        else:
            self.Lb1.pack(side=BOTTOM)  # show list

            txt_for_query = txt + "%"

            cursor = self.db.cursor()

            cursor.execute("SELECT * FROM customers WHERE name LIKE '%s'" % txt_for_query)

            res = cursor.fetchall()
            print(res, "jaja")
            for line in res:
                print(line, "xd")
                self.Lb1.insert(END, line[0])  # append list
                self.Lb2.insert(END, line[1])  # append list
                for i in range(len(line)):
                    self.Lb1.insert(END, line[i])  # append list

            cursor.close()


# ----------------------------------------------------------------------

root = Tk()
SearchBar(root)
root.mainloop()
