import sqlite3
import constant
import pyautogui
import tkinter as tk
from sqlite3 import Error
from tkinter import font
from tkinter.ttk import Label, Entry, Combobox, Button
from tkcalendar import DateEntry
from Components.HoverButton import HoverButton
from tkinter.messagebox import askyesno, showinfo, showwarning


class Table(tk.Frame):
    lenPhone = 10

    def __init__(self, parent, rows, columns):
        self.n = rows
        self.m = columns
        self.labels = []
        self.font1 = None
        self.frame = tk.Frame.__init__(self, parent, background="black")

        # Obtenemos la imagen
        photo = tk.PhotoImage(file="./resources/Edit_icon.png")
        # Escalamos la imagen para que quepa en el boton
        self.photoimage = photo.subsample(60, 60)

        if rows <= 10:
            rows = 11
        for row in range(rows):
            current_row = []
            fg = "black"
            width = 10
            cursor = "hand2"
            # self.print()
            if row % 2:
                bg = "lightblue"
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

                self.mylabel = HoverButton(self, self.labels, text=" ", )
                self.mylabel.config(borderwidth=0, width=width, height=2, bg=bg,
                                    fg=fg,
                                    activebackground="yellow",
                                    cursor=cursor,
                                    command=self.openEditWindow)
                self.mylabel.row_number = row
                self.mylabel.col_number = column
                self.mylabel.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)

                #Creacion de los botones de eliminacion
                if row != 0 and column == self.m - 1 and row <= self.n - 1:
                    #self.mylabel.config(text='',image=self.photoimage, command=self.delCustomer)
                    self.mylabel.config(text='', image=self.photoimage)
                    #self.mylabel.bind("<Double-Button-1>", self.delCustomer)
                #Creacion del header
                elif row == 0:
                    bg = "#B22222"
                    fg = "white"
                    cursor = "arrow"
                    self.mylabel = tk.Label(self, text=" ", borderwidth=0, width=width, height=2, bg=bg, fg=fg,
                                            cursor=cursor)
                    self.mylabel.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                else:
                    self.mylabel.config(text=" ")

                current_row.append(self.mylabel)
            self.labels.append(current_row)

    def getAllCustomers(self):
        try:
            conn = sqlite3.connect('DB/agenda.db')
        except Error as e:
            print(e)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        return rows

    def openEditWindow(self):

        self.font1 = font.Font(weight='bold')
        self.menu = tk.Toplevel()
        self.centrar_ventana(self.menu)
        self.menu.resizable(0, 0)
        self.menu.geometry("600x500")
        mycolor = "#C2C2C2"
        self.menu['bg'] = mycolor
        self.menu.title("Editar Clientes")

        # Etiquetas/Labels
        self.nameLabel = Label(self.menu, text="Nombre:", font=self.font1, background=mycolor)
        self.surnameLabel = Label(self.menu, text="Apellidos:", font=self.font1, background=mycolor)
        self.phoneLabel = Label(self.menu, text="Telefono:", font=self.font1, background=mycolor)
        self.birthDateLabel = Label(self.menu, text="Fecha Nacimiento: ", font=self.font1, background=mycolor)
        self.statusLabel = Label(self.menu, text="Status: ", font=self.font1, background=mycolor)

        self.nameLabel.place(x=250, y=25)
        self.surnameLabel.place(x=250, y=90)
        self.phoneLabel.place(x=250, y=160)
        self.birthDateLabel.place(x=220, y=230)
        self.statusLabel.place(x=260, y=300)

        # Inputs
        vcmd = (self.register(self.validateString))
        self.name = Entry(self.menu, textvariable="", width=25, font='Georgia 14', justify='center',
                          validate="all", validatecommand=(vcmd, '%P'))
        self.surname = Entry(self.menu, textvariable="", width=12, font='Georgia 14', justify='center',
                             validate="all", validatecommand=(vcmd, '%P'))
        self.surname2 = Entry(self.menu, textvariable="", width=12, font='Georgia 14', justify='center',
                              validate="all", validatecommand=(vcmd, '%P'))

        vcmd = (self.register(self.validateNumbers))
        self.phone = Entry(self.menu, textvariable="", width=25, font='Georgia 14', justify='center',
                           validate="all", validatecommand=(vcmd, '%P', self.lenPhone))
        self.birthDate = DateEntry(self.menu, locale='es', date_pattern='dd/mm/y', year=2000, month=1, day=1,
                                   font='Georgia 14', justify='center')
        self.combo = Combobox(self.menu, state="readonly", values=["ALTA", "BAJA"], font='Georgia 14',
                              justify='center')

        self.name.place(x=100, y=50, width=400, height=30)
        self.surname.place(x=100, y=120, width=195, height=30)
        self.surname2.place(x=305, y=120, width=195, height=30)
        self.phone.place(x=100, y=190, width=400, height=30)
        self.birthDate.place(x=100, y=260, width=400, height=30)
        self.combo.place(x=100, y=330, width=400, height=30)

        self.data = self.getCustomerData()

        print(self.name.cget('text'))
        # Botones
        self.ModifyBtn = Button(self.menu, text='Modificar', command=self.estasSeguro, state='disabled')
        self.ModifyBtn.place(x=100, y=400, width=200, height=50)
        self.menu.bind("<Key>", self.toggleButton)

        closeBtn = Button(self.menu, text='Volver', command=self.menu.destroy)
        closeBtn.place(x=305, y=400, width=200, height=50)

        # print(constant.this_row)
        self.menu.transient(master=self)
        self.menu.grab_set()
        self.wait_window(self.menu)

    def toggleButton(self, event):
        name = self.name.get()
        if self.surname2.get() == "":
            surnames = self.surname.get()
        else:
            surnames = self.surname.get() + " " + self.surname2.get()
        phone = self.phone.get()
        birthDate = self.birthDate.get()
        status = self.combo.get()
        self.user = (self.data[0], name, surnames, phone, birthDate, status)
        print(self.data, '***********')
        print(self.user)
        if self.data == self.user:
            self.ModifyBtn.config(state='disabled')
        else:
            self.ModifyBtn.config(state='enabled')

    def getRow(self):
        text = self.get(constant.this_row, 0).cget("text")
        try:
            # conn = sqlite3.connect('../DB/agenda.db')
            conn = sqlite3.connect('DB/agenda.db')
        except Error as e:
            print(e)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE ID == %s" % text)
        res = cursor.fetchall()
        return res

    def getCustomerData(self):
        res = self.getRow()
        # print(res[0])
        self.name.insert(0, res[0][1])
        print(len(res[0][2].split(' ')))
        if len(res[0][2].split(' ')) == 2:
            apellido = res[0][2].split(' ')
            self.surname.insert(0, apellido[0])
            self.surname2.insert(0, apellido[1])
        else:
            self.surname.insert(0, res[0][2])

        self.phone.insert(0, res[0][3])
        self.birthDate.set_date(res[0][4])
        self.combo.set(res[0][5])
        return res[0]

    def estasSeguro(self):
        response = askyesno(message="¿Seguro que quieres modificar este cliente?", title="Título")
        if response:
            self.updateData(self.data)
            showinfo(message="Cliente modificado", title="Título")
            for i in range(self.m - 1):
                self.set(constant.this_row, i, self.user[i])
            self.menu.destroy()
        return response

    def updateData(self, data):
        user = data
        name = self.name.get()
        if self.surname2.get() == "":
            surnames = self.surname.get()
        else:
            surnames = self.surname.get() + " " + self.surname2.get()
        phone = self.phone.get()
        birthDate = self.birthDate.get()
        status = self.combo.get()

        try:
            conn = sqlite3.connect('DB/agenda.db')
        except Error as e:
            print(e)
        cursor = conn.cursor()

        sql_update_query = """UPDATE customers
         set name = ?, surname = ?, phone= ?, birthdate= ?, status= ? where id = ?"""
        data = (name, surnames, phone, birthDate, status, data[0])
        cursor.execute(sql_update_query, data)

        conn.commit()

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

    def validateString(self, entrada):
        # abc=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","ñ","o","p","q","r","s","t","u","v","w","x","y","z","ç"," "]
        num = 15
        # print(len(entrada))
        if str.isalpha(entrada) and len(entrada) < int(num) or entrada == "":
            return True
        else:
            return False

    def validateNumbers(self, entrada, longitud):
        if str.isdigit(entrada) and len(entrada) < int(longitud) or entrada == "":
            return True
        else:
            return False

    def centrar_ventana(self, dialeg):
        self.menu.update_idletasks()  # Add this line
        width, height = pyautogui.size()
        x = width // 3
        y = (height // 5)
        # print(height,width)
        # print(x)
        # print(y)
        dialeg.geometry('{}x{}+{}+{}'.format(width, height, x, y))

"""
    def delRow(self):
        constant.customer=self.getAllCustomers()
        text = self.getRow()
        print(text)
        response = askyesno(icon="warning", message="¿Seguro que quieres eliminar este registro?\n" + str(text[0]))
        if response:
            try:
                conn = sqlite3.connect('DB/agenda.db')
            except Error as e:
                print(e)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE ID == %s" % text[0][0])
            conn.commit()
            print(len(self.getAllCustomers()), "leeeeeeeeen")
            self.refresh(constant.customer, 1)

    def refresh(self, myList, num):
        print(len(myList), '-------------')
        print(num)
        for i in range(len(myList)):
            for j in range(len(myList[i])):
                self.set(i+1, j, " ")
        for i in range(len(myList)-num):
            for j in range(len(myList[i])):
                self.set(i+1, j, myList[i][j])
        return self
"""