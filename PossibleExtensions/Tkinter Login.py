from tkinter import *
from tkinter import ttk, font
from agenda import main

class Aplicacio():

    def __init__(self):
        self.arrel = Tk()
        self.arrel.geometry('400x200')
        self.arrel.resizable(0, 0) # Estableix que no es pot canviar el tamany de la finestra
        self.arrel.title("Login agenda")
        self.font1 = font.Font(weight='bold')
        
        boton = ttk.Button(self.arrel, text='Acceder', command=self.aceptar) # Botó login, si passwd i user son correctes obre l'agenda
        boton.pack(side=BOTTOM, padx=20, pady=20)
        
        self.userLabel = ttk.Label(self.arrel, text="Usuario:", font=self.font1)
        self.passwdLabel = ttk.Label(self.arrel, text="Contraseña:", font=self.font1)

        
        self.message = StringVar()
        self.Usuari = StringVar()
        self.clave = StringVar()
        
        self.etiq3 = ttk.Label(self.arrel, textvariable=self.message, font=self.font1, foreground='blue')
        self.ctext1 = ttk.Entry(self.arrel, textvariable=self.Usuari, width=25)
        self.ctext2 = ttk.Entry(self.arrel, textvariable=self.clave, width=25, show="*")
        
        #Posicionamiento de elementos
        self.userLabel.place(x=30, y=40)
        self.passwdLabel.place(x=30, y=80)
        self.etiq3.place(x=130, y=120)
        self.ctext1.place(x=155, y=38)
        self.ctext2.place(x=155, y=78)
        
        self.ctext2.bind('<Button-1>', self.borrar_message)
        self.arrel.mainloop()
        
    def aceptar(self):
        #Aqui deberia abrir conexion al servidor de la DDBB y
        #comprobar que el ususario y pswd coinciden i luego abrir la ventana de la agenda
        if self.clave.get() == 'tkinter':
            self.arrel.destroy() # close the current window
            self.agenda = main()
        else:
            self.etiq3.configure(foreground='red')
            self.message.set("Acceso denegado")
            
    def borrar_message(self, evento):
        self.clave.set("")
        self.message.set("")
        
def iniciar():
    mi_app = Aplicacio()
    return (0)

if __name__ == '__main__':
    iniciar()