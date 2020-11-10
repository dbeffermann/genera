from tkinter import ttk
from tkinter import *
import generacom
import os
import pandas as pd

import sqlite3

base_dir = os.getcwd()
class Product:
    # connection dir property
    db_propiedad = 'database.db'

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


        ttk.Button(text = 'MATCHES', command = self.matches).grid(row = 7, column = 1, sticky = W + E)

        frame_db = ttk.Frame(self.wind)
        frame_db.grid()
        frame_db.lift()

    # Recives an url and returns a dataframe.
    def api(self):

            self.ventana = Toplevel()
            self.ventana.title("API")
            Label(self.ventana, text = 'Ingrese una url').grid(row = 0, column = 0)
            self.url = ttk.Entry(self.ventana, font="Calibri 15")
            self.url.grid(row = 1, column = 0, sticky = W + E)
            self.url.focus()
            api_btn = ttk.Button(self.ventana, text = 'Buscar', command = lambda: self.api_search())
            api_btn.grid(row = 3, column = 0, sticky = W + E)

    def db(self):

            self.ventana_db = Toplevel()
            self.ventana_db.title("Base de datos")
            frame = LabelFrame(self.ventana_db, text = 'Base de Datos')
            frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        

            # propiedad Input
            Label(frame, text = 'Propiedad: ').grid(row = 1, column = 0)
            self.search_rol = ttk.Entry(frame)
            self.search_rol.grid(row = 1, column = 1)
            self.search_btn = ttk.Button(frame, text = 'Buscar', command = lambda: self.search_db())
            self.search_btn.grid(row = 1, column = 2)

            
            
            # Table for database.
            self.tree_ = ttk.Treeview(self.ventana_db, height = 35, columns=("#0","#1"))
            self.tree_.grid(row = 4, column = 0, columnspan = 1)
            self.tree_.heading('#0', text = 'Scan', anchor = CENTER)
            self.tree_.column('#0', width = 700)
            self.tree_.heading('#1', text = 'Link', anchor = CENTER)
            self.tree_.column('#1', width = 600)

            self.acum = []

            self.matches = []

            self.get_db()
        

    def matches(self):
        
        self.ventana_matches = Toplevel()
        self.ventana_matches.title("Matches")
        frame = LabelFrame(self.ventana_matches, text = 'Acciones')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        self.export_btn = ttk.Button(frame, text = 'Exportar a Excel', command = lambda: self.export_xls())
        self.export_btn.grid(row = 1, column = 2)

        # Table for matches.
        self.tree_matches = ttk.Treeview(self.ventana_matches, height = 35, columns=("#0","#1"))
        self.tree_matches.grid(row = 4, column = 0, columnspan = 1)
        self.tree_matches.heading('#0', text = 'Scan', anchor = CENTER)
        self.tree_matches.column('#0', width = 600)
        self.tree_matches.heading('#1', text = 'Link', anchor = CENTER)
        self.tree_matches.column('#1', width = 600)

        self.get_matches()

    def export_xls(self):

        x = self.object
        
        df = pd.DataFrame(x)

        df.columns = ['Link', 'Scan', 'Section', 'Active']

        #df.to_excel(f'{base_dir}/export/matches.xlsx', index = False)



    def get_matches(self):

        query_db = 'SELECT rol from product'
        db_rol   = self.run_query(query_db)
        db_rol_lista    = list(map(lambda x: x[0], list(db_rol)))

        acum = []
        for i in db_rol_lista:

            query = f"""SELECT * from database WHERE scan like "%%'{i}'%%" """
            result = self.run_query(query)
            
            acum.append(list(result))

        self.object = [i[0] for i in acum if len(i)>0]
        #print([i for i in acum if len(i)>0])
        for row in self.object:
            self.tree_matches.insert('', 0, text = row[1], values = row[0])
        
        
        

    def get_db(self):
        # cleaning Table 
        records = self.tree_.get_children()
        for element in records:
            self.tree_.delete(element)
        # getting data
        query = 'SELECT * FROM database'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree_.insert('', 0, text = row[1], values = row[0])
            
    
    def search_db(self):
        
        # cleaning Table 
        records = self.tree_.get_children()
        for element in records:
            self.tree_.delete(element)
        # getting data
        rol = str(self.search_rol.get())
        #print(f"El rol es: {rol}")
        query = f"""SELECT * FROM database where scan like "%%'{rol}'%%" """
        #print(f"La query es: {query}")
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree_.insert('', 0, text = row[1], values = row[0])
            self.acum.append(list(row))
        
           
    def api_search(self):

        url = self.url.get()

        df = generacom.pjud(url)

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_propiedad) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get Products from Database
    def get_products(self):
        # cleaning Table 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM product ORDER BY comuna DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    # User Input Validation
    def validation(self):
        return len(self.propiedad.get()) != 0 and len(self.rol.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters =  (self.propiedad.get(), self.rol.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Propiedad {} guardada Exitosamente'.format(self.propiedad.get())
            self.propiedad.delete(0, END)
            self.rol.delete(0, END)
        else:
            self.message['text'] = 'Debes ingresar propiedad y rol'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor Seleccione una Propiedad'
            return
        self.message['text'] = ''
        comuna = self.tree.item(self.tree.selection())['text']
        rol = self.tree.item(self.tree.selection())
        
        try:
            rol = rol['values'][0]
            query = 'DELETE FROM product WHERE comuna = ? and rol = ?' #aqui bug corregido.
            self.run_query(query, (comuna, (rol)))
        except:

            rol = rol['values']
            query = 'Delete FROM product WHERE comuna = ?' #aqui bug corregido.
            self.run_query(query, (comuna, ))
        
        
        self.message['text'] = 'Rol {} eliminada Exitosamente'.format((rol))
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor, seleccione una Propiedad'
            return
        propiedad = self.tree.item(self.tree.selection())['text']
        old_rol = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Propiedad'
        # Old propiedad
        Label(self.edit_wind, text = 'Propiedad:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = propiedad), state = 'readonly').grid(row = 0, column = 2)
        # New propiedad
        Label(self.edit_wind, text = 'Nuevo Rol:').grid(row = 1, column = 1)
        new_rol = Entry(self.edit_wind)
        new_rol.grid(row = 1, column = 2)

        # Old rol 
        Label(self.edit_wind, text = 'Rol:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_rol), state = 'readonly').grid(row = 2, column = 2)
        # New rol
        Label(self.edit_wind, text = 'Nueva Propiedad:').grid(row = 3, column = 1)
        new_propiedad = Entry(self.edit_wind)
        new_propiedad.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(new_propiedad.get(), propiedad, new_rol.get(), old_rol)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_propiedad, propiedad, new_rol, old_rol):
        query = 'UPDATE product SET comuna = ?, rol = ? WHERE comuna = ? AND rol = ?'

        if len(new_rol) < 2:

            new_rol = old_rol

        if len(new_propiedad) < 2:

            new_propiedad = propiedad
        parameters = (new_propiedad, new_rol, propiedad, old_rol)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(propiedad)
        self.get_products()

    
    #def find_matches aqui.

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
    