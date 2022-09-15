import csv
import sqlite3

import constant
import pyautogui
import tkinter as tk
from datetime import datetime
from sqlite3 import Error
from tkinter import *
from tkinter import ttk, font, filedialog
from tkcalendar import DateEntry
from Components.Table import Table
from tkinter.messagebox import showinfo, showwarning, askyesno


class Agenda:
    ventana = 0
    posx_y = 0
    width, height = pyautogui.size()
    lenPhone = 10

    def __init__(self):
        self.myTable = None
        self.SearchBar = None
        self.menu = Tk()
        self.menu.resizable(0, 0)  # Estableix que no es pot canviar el tamany de la finestra
        self.menu.title("Agenda")
        self.menu['bg'] = '#3090C7'
        self.font1 = font.Font(weight='bold')
        x = (Agenda.width // 4)
        y = (Agenda.height // 20)
        self.menu.geometry('{}x{}+{}+{}'.format(700, 700, x, y))

        self.btnAlta = ttk.Button(self.menu, text='Alta Clientes', command=self.ventanaAltaCliente)
        self.btnBaja = ttk.Button(self.menu, text='Gestionar Clientes', command=self.gestionarClientes)
        self.btnImport = ttk.Button(self.menu, text='Importar Clientes en CSV', command=self.importar)
        self.btnExport = ttk.Button(self.menu, text='Exportar Clientes en CSV ', command=self.exportar)
        self.btnExit = ttk.Button(self.menu, text='Salir', command=self.salir)

        self.btnAlta.place(x=100, y=50, width=500, height=100)
        self.btnBaja.place(x=100, y=170, width=500, height=100)
        self.btnImport.place(x=100, y=290, width=500, height=100)
        self.btnExport.place(x=100, y=410, width=500, height=100)
        self.btnExit.place(x=100, y=530, width=500, height=100)
        mainloop()

    def ventanaAltaCliente(self):
        # Construimos una ventana "Dialog"
        self.dialeg = Toplevel()
        self.centrar_ventana(self.dialeg)
        Agenda.ventana += 1
        Agenda.posx_y += 50
        self.dialeg.geometry("500x500")
        self.dialeg.resizable(0, 0)
        self.dialeg.title("Registrar Cliente")
        self.dialeg['bg'] = '#B22222'

        # Etiquetas/Labels
        self.nameLabel = Label(self.dialeg, text="Nombre:", bg="#B22222", fg="white", font=self.font1)

        self.surnameLabel = Label(self.dialeg, text="Apellidos:", bg="#B22222", fg="white", font=self.font1)
        self.phoneLabel = Label(self.dialeg, text="Telefono:", bg="#B22222", fg="white", font=self.font1)
        self.birthDateLabel = Label(self.dialeg, text="Fecha Nacimiento: ", bg="#B22222", fg="white", font=self.font1)

        self.nameLabel.place(x=50, y=25)
        self.surnameLabel.place(x=50, y=100)
        self.phoneLabel.place(x=50, y=175)
        self.birthDateLabel.place(x=50, y=250)

        # Inputs
        vcmd = (self.menu.register(self.validateString))
        self.name = ttk.Entry(self.dialeg, textvariable="", width=25, font='Georgia 14', justify='center',
                              validate="all", validatecommand=(vcmd, '%P'))
        self.surname = ttk.Entry(self.dialeg, textvariable="", width=12, font='Georgia 14', justify='center',
                                 validate="all", validatecommand=(vcmd, '%P'))
        self.surname2 = ttk.Entry(self.dialeg, textvariable="", width=12, font='Georgia 14', justify='center',
                                  validate="all", validatecommand=(vcmd, '%P'))

        vcmd = (self.menu.register(self.validateNumbers))
        self.phone = ttk.Entry(self.dialeg, textvariable="", width=25, font='Georgia 14', justify='center',
                               validate="all", validatecommand=(vcmd, '%P', self.lenPhone))

        self.birthDate = DateEntry(self.dialeg, locale='es', date_pattern='dd/mm/y', year=2000, month=1, day=1,
                                   font='Georgia 14', justify='center')

        self.name.place(x=50, y=50, width=400, height=30)
        self.surname.place(x=50, y=125, width=195, height=30)
        self.surname2.place(x=255, y=125, width=195, height=30)
        self.phone.place(x=50, y=200, width=400, height=30)
        self.birthDate.place(x=50, y=275, width=400, height=30)

        # Botones
        AddBtn = ttk.Button(self.dialeg, text='Añadir', command=self.alta)
        AddBtn.place(x=50, y=350, width=400, height=50)

        closeBtn = ttk.Button(self.dialeg, text='Volver', command=self.dialeg.destroy)
        closeBtn.place(x=50, y=420, width=400, height=50)

        self.dialeg.transient(master=self.menu)
        self.dialeg.grab_set()
        self.menu.wait_window(self.dialeg)

    def alta(self):
        self.message = StringVar()
        if self.name.get() == "" or len(self.name.get()) < 3 or self.surname.get() == "" or len(
                self.surname.get()) < 3 or self.phone.get() == "" or len(
            self.phone.get()) != 9 or self.birthDate.get() == "":
            showwarning(
                title='Error',
                message="Llena todos los campos!\n\n Nombre: Mínimo 3 letras\n Apellido: Mínimo 3 letras \n Telefono: 9 "
                        "números \n Fecha: dd/mm/yyyy"
            )

        else:
            if self.surname2.get() == "":
                surnames = self.surname.get()
            else:
                surnames = self.surname.get() + " " + self.surname2.get()

            # INSERT customers.
            self.insertCustomer(self.name.get(), surnames, self.phone.get(), self.birthDate.get(), "ALTA")

    def gestionarClientes(self):

        self.dialogo = Toplevel()
        self.centrar_ventana(self.dialogo)
        Agenda.ventana += 1
        Agenda.posx_y += 50
        self.dialogo.geometry("800x600")
        self.dialogo.resizable(0, 0)
        mycolor = "#C2C2C2"
        self.dialogo['bg'] = mycolor
        self.dialogo.title("Gestionar Clientes")

        registros = self.getAllCustomers()
        # print(self.getAllCustomers())
        self.registroZero = ("ID", "Name", "Surnames", "Phone", "Birthdate", "Status")
        registros.insert(0, self.registroZero)

        LabelSBr = Label(self.dialogo, text="Search:", font='Georgia 14', justify='center', bd=2, bg=mycolor)
        LabelSBr.place(x=62, y=35, width=100, height=20)
        self.SearchBar = Entry(self.dialogo, bd=2, width=50)
        self.SearchBar.place(x=155, y=35, width=200, height=20)
        self.dialogo.bind("<Key>", self.inputData)

        self.value = tk.IntVar()
        self.value.set(1)
        radioBtn1 = tk.Radiobutton(self.dialogo, text="Name", padx=20, command=self.SelectedChoice,
                                   variable=self.value,
                                   value=1, bg=mycolor, activebackground=mycolor)
        radioBtn1.place(x=155, y=60, height=20)

        radioBtn2 = tk.Radiobutton(self.dialogo, text="Phone", padx=20, command=self.SelectedChoice,
                                   variable=self.value,
                                   value=2, bg=mycolor, activebackground=mycolor)
        radioBtn2.place(x=250, y=60, width=105, height=20)

        self.myTable = self.scrollableTable(self.dialogo, registros)
        self.myTable.place()
        self.fillTable(self.myTable, registros)
        self.dialogo.transient(master=self.menu)
        self.dialogo.grab_set()
        self.menu.wait_window(self.dialogo)

    def SelectedChoice(self):
        print(self.value.get())
        self.SearchBar.delete(0, END)
        self.SearchBar.insert(0, "")


    def fillTable(self, table, myList):
        for i in range(len(myList)):
            for j in range(len(myList[i])):
                table.set(i, j, myList[i][j])
        return table

    def scrollableTable(self, frame, registros):
        tableFrame = Frame(frame)
        tableFrame.grid(padx=80, pady=100)

        # Add a canvas in that frame
        canvas = tk.Canvas(tableFrame, width=610, height=425)
        canvas.grid()

        lenRows = len(registros)
        lenColumns = len(registros[0]) + 1

        self.myTable = Table(tableFrame, lenRows, lenColumns)
        self.myTable.grid(row=0, column=0, pady=30)

        # Creacion del Frame que va a contener la tabla
        frame_buttons = tk.Frame(self.myTable)
        # Enlaza el scrollbar con el canvas
        vsb = tk.Scrollbar(tableFrame, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=5, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)
        canvas.create_window((0, 0), window=self.myTable, anchor='ne')

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        frame_buttons.update_idletasks()

        canvas.config(scrollregion=canvas.bbox("all"))

        return self.myTable

    def inputData(self, event):

        txt = self.SearchBar.get()
        txt_for_query = txt + "%"

        cursor = self.dbConnect()
        if self.value.get() == 1:
            cursor.execute("SELECT * FROM customers WHERE name LIKE '%s'" % txt_for_query)
        else:
            cursor.execute("SELECT * FROM customers WHERE phone LIKE '%s'" % txt_for_query)
        res = cursor.fetchall()

        res.insert(0, self.registroZero)
        registros = self.getAllCustomers()
        registros.insert(0, self.registroZero)

        for i in range(len(registros)):
            for j in range(len(registros[i]) + 1):
                self.myTable.set(i, j, " ")
        for i in range(len(res)):
            for j in range(len(res[i])):
                self.myTable.set(i, j, res[i][j])
                if j == 5:
                    self.myTable.set(i, 6, "Del")

        cursor.close()

    def insertCustomer(self, name, surnames, phone, birthDate, status):
        try:
            conn = sqlite3.connect('DB/agenda.db')
        except Error as e:
            print(e)
        cursor = conn.cursor()
        try:
            cursor.execute("insert into customers (name, surname, phone, birthdate, status) values (?, ?, ?, ?, ?)",
                           (name, surnames, phone, birthDate, status))
            conn.commit()
            showinfo(
                title='Cliente añadido',
                message="Cliente añadido!"
            )
            self.dialeg.destroy()
        except Error as err:
            thisError = str(err).split(': ')
            if thisError[1] == "CUSTOMERS.PHONE":
                showwarning(message="El telefono introducido se encuentra asignado a otro cliente")
            else:
                showwarning(message=err)
    def insertMultiCustomers(self, name, surnames, phone, birthDate, status):
        try:
            conn = sqlite3.connect('DB/agenda.db')
        except Error as e:
            print(e)
        cursor = conn.cursor()
        try:
            cursor.execute("insert into customers (name, surname, phone, birthdate, status) values (?, ?, ?, ?, ?)",
                           (name, surnames, phone, birthDate, status))
            conn.commit()
        except Error as err:
            thisError = str(err).split(': ')
            if thisError[1] == "CUSTOMERS.PHONE":
                showwarning(message="El telefono introducido se encuentra asignado a otro cliente")
            else:
                showwarning(message=err)
    def dbConnect(self):
        try:
            conn = sqlite3.connect('DB/agenda.db')
        except Error as e:
            print(e)
        cursor = conn.cursor()
        return cursor

    def getAllCustomers(self):

        cursor = self.dbConnect()
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        return rows

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir="./",
                                              title="Select a File",
                                              filetypes=(("csv files",
                                                          "*.csv*"),
                                                         ("all files",
                                                          "*.*")))
        return filename

    def importar(self):
        respuesta = askyesno(title="Confirmación", message="Estas seguro que quieres importar una lista de clientes?")
        listaExist = []
        if respuesta:
            file = self.browseFiles()
            with open(file, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                num = 0
                for row in reader:
                    if num == 0:
                        print(row)
                    else:
                        cursor = self.dbConnect()
                        cursor.execute("SELECT * FROM customers WHERE phone LIKE '%s'" % row[2])
                        res = cursor.fetchall()
                        if len(res) > 0:
                            listaExist.append(row[2])
                            print(listaExist)
                            print('Ya existe telefono')
                        else:
                            self.insertMultiCustomers(row[0], row[1], row[2], row[3], row[4])
                    num += 1
                showinfo(message="¡Importación completada!")

            if len(listaExist) > 0:
                print(listaExist, '---------')
                text = ""
                for i in range(len(listaExist)):
                    if i !=len(listaExist)-1:
                        text += listaExist[i] + ", "
                    else:
                        text += listaExist[i]
                showinfo(message="Los clientes con los siguientes telefonos no se han añadido debido a que estos ya estan asignados: "
                                     "\n\n"+text)
        else:
            print("No")

    def exportar(self):
        respuesta = askyesno(title="Confirmación", message="Estas seguro que quieres exportar la lista de clientes?")
        if respuesta:
            now = datetime.now()
            dt_string = now.strftime("%d%m%Y_%H_%M_%S")
            filename = 'customers_' + dt_string + '.csv'

            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['ID', 'Name', 'Surnames', 'Phone', 'Birthdate', 'Status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                rows = self.getAllCustomers()
                for i in range(len(rows)):
                    writer.writerow(
                        {'ID': rows[i][0],
                         'Name': rows[i][1],
                         'Surnames': rows[i][2],
                         'Phone': rows[i][3],
                         'Birthdate': rows[i][4],
                         'Status': rows[i][5],
                         })
                csvfile.close()
                showinfo(message="¡Exportación completada!")

    def centrar_ventana(self, dialeg):
        self.menu.update_idletasks()  # Add this line
        width, height = pyautogui.size()
        x = width // 3
        y = (height // 5)
        # print(height,width)
        # print(x)
        # print(y)
        dialeg.geometry('{}x{}+{}+{}'.format(width, height, x, y))

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

    def salir(self):
        self.menu.destroy()


def main():
    mi_app = Agenda()
    return 0


if __name__ == '__main__':
    main()
