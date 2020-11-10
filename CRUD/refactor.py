from tkinter import ttk
from tkinter import *
import generacom

import sqlite3

class Main:
    # connection dir property
    db_propiedad = 'refactor.db'

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('Monitoreo de Propiedades')

        img = Image("photo", file="genera.png")
        self.wind.iconphoto(True, img)

         # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Registrar nuevas propiedades')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # propiedad Input
        Label(frame, text = 'Propiedad: ').grid(row = 1, column = 0)
        self.propiedad = Entry(frame, font = "Calibri 15")
        self.propiedad.focus()
        self.propiedad.grid(row = 1, column = 1)

        # rol Input
        Label(frame, text = 'Rol: ').grid(row = 2, column = 0)
        self.rol = Entry(frame, font = "Calibri 15")
        self.rol.grid(row = 2, column = 1)

        # Button Add Product 
        ttk.Button(frame, text = 'Guardar Propiedad', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'green')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 30, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Comuna', anchor = CENTER)
        self.tree.heading('#1', text = 'Rol', anchor = CENTER)

        # Buttons
        ttk.Button(text = 'DELETE', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'EDIT', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)

        # Filling the Rows
        self.get_products()

        
        # Popup window, for running API functionalities.
        ttk.Button(text = 'API', command = self.api).grid(row = 6, column = 1, sticky = W + E)
        ttk.Button(text = 'DATABASE', command = self.db).grid(row = 6, column = 0, sticky = W + E)

        frame_db = ttk.Frame(self.wind)
        frame_db.grid()
        frame_db.lift()

        def run_query(self, query, parameters = ()):
            with sqlite3.connect(self.db_propiedad) as conn:
                cursor = conn.cursor()
                result = cursor.execute(query, parameters)
                conn.commit()
            return result

        self.get_propiedades()
        # Obtener propiedades desde la bbdd.
    def get_propiedades(self):
        # Limpiar la tabla 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Obtener datos.
        query = 'SELECT * FROM propiedades ORDER BY comuna DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])


        

if __name__ == '__main__':
    window = Tk()
    application = Main(window)
    window.mainloop()