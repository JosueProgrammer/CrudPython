import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk


class ClienteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clientes")
        self.root.configure(background='light blue')
        
        icon_path = "User2.png"
        icon = Image.open(icon_path)
        icon_tk = ImageTk.PhotoImage(icon)
        root.iconphoto(True, icon_tk)

        # Marco principal
        self.frame = ttk.Frame(self.root, width=400)
        self.frame.grid(row=0, column=0, padx=15, pady=15)

        # Título y línea horizontal
        self.label_titulo = ttk.Label(self.frame, text="Datos del Cliente", font=("Helvetica", 14, "bold"))
        self.label_titulo.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        self.linea_horizontal = ttk.Separator(self.frame, orient="horizontal")
        self.linea_horizontal.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))

        # Campos de entrada
        self.label_nombre = ttk.Label(self.frame, text="Nombre del cliente:")
        self.label_nombre.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry = ttk.Entry(self.frame)
        self.nombre_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.label_apellido = ttk.Label(self.frame, text="Apellido del cliente:")
        self.label_apellido.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.apellido_entry = ttk.Entry(self.frame)
        self.apellido_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.label_direccion = ttk.Label(self.frame, text="Dirección del cliente:")
        self.label_direccion.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.direccion_entry = ttk.Entry(self.frame)
        self.direccion_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Botones
        self.btn_guardar = ttk.Button(self.frame, text="Guardar", command=self.guardar_cliente)
        self.btn_guardar.grid(row=5, column=0, padx=5, pady=5, sticky="we")

        self.btn_actualizar = ttk.Button(self.frame, text="Actualizar", command=self.abrir_ventana_actualizar)
        self.btn_actualizar.grid(row=5, column=1, padx=5, pady=5, sticky="we")

        self.btn_eliminar = ttk.Button(self.frame, text="Eliminar", command=self.eliminar_cliente)
        self.btn_eliminar.grid(row=5, column=2, padx=5, pady=5, sticky="we")

        # Tabla de clientes
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre", "Apellido", "Dirección"), show="headings")
        self.tree.heading("ID", text="ID del cliente", anchor=tk.CENTER)
        self.tree.heading("Nombre", text="Nombre del cliente", anchor=tk.CENTER)
        self.tree.heading("Apellido", text="Apellido del cliente", anchor=tk.CENTER)
        self.tree.heading("Dirección", text="Dirección del cliente", anchor=tk.CENTER)

        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Nombre", width=150, anchor=tk.CENTER)
        self.tree.column("Apellido", width=150, anchor=tk.CENTER)
        self.tree.column("Dirección", width=200, anchor=tk.CENTER)

        self.tree.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="ew")



        self.cargar_clientes()

    def ejecutar_consulta(self, query, parametros=(), fetchall=False):
        conexion = sqlite3.connect("clientes.db")
        cursor = conexion.cursor()
        resultado = cursor.execute(query, parametros)
        if fetchall:
            resultado = resultado.fetchall()
        else:
            conexion.commit()
        conexion.close()
        return resultado

    def cargar_clientes(self):
        self.tree.delete(*self.tree.get_children())
        query = "SELECT * FROM clientes"
        clientes = self.ejecutar_consulta(query, fetchall=True)
        for cliente in clientes:
            self.tree.insert("", "end", values=cliente)

    def guardar_cliente(self):
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        direccion = self.direccion_entry.get()
        if nombre and apellido and direccion:
            query = "INSERT INTO clientes VALUES (NULL, ?, ?, ?)"
            self.ejecutar_consulta(query, (nombre, apellido, direccion))
            self.nombre_entry.delete(0, tk.END)
            self.apellido_entry.delete(0, tk.END)
            self.direccion_entry.delete(0, tk.END)
            self.cargar_clientes()
            messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    def abrir_ventana_actualizar(self):
        item = self.tree.selection()
        if item:
            cliente_seleccionado = self.tree.item(item, "values")
            VentanaActualizar(self.root, cliente_seleccionado, self)
        else:
            messagebox.showerror("Error", "Por favor, seleccione un cliente para actualizar.")

    def actualizar_cliente(self, id_cliente, nombre, apellido, direccion):
        query = "UPDATE clientes SET nombre=?, apellido=?, direccion=? WHERE id=?"
        self.ejecutar_consulta(query, (nombre, apellido, direccion, id_cliente))
        self.cargar_clientes()
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")

    def eliminar_cliente(self):
        item = self.tree.selection()
        if item:
            id_cliente = self.tree.item(item, "values")[0]
            query = "DELETE FROM clientes WHERE id=?"
            self.ejecutar_consulta(query, (id_cliente,))
            self.cargar_clientes()
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un cliente para eliminar.")


class VentanaActualizar(tk.Toplevel):
    def __init__(self, parent, cliente_seleccionado, cliente_app):
        super().__init__(parent)
        self.title("Actualizar Cliente")
        self.cliente_app = cliente_app

        # Campos de entrada con los datos del cliente seleccionado
        self.label_nombre = ttk.Label(self, text="Nombre del cliente:")
        self.label_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry = ttk.Entry(self)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.nombre_entry.insert(0, cliente_seleccionado[1])

        self.label_apellido = ttk.Label(self, text="Apellido del cliente:")
        self.label_apellido.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.apellido_entry = ttk.Entry(self)
        self.apellido_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.apellido_entry.insert(0, cliente_seleccionado[2])

        self.label_direccion = ttk.Label(self, text="Dirección del cliente:")
        self.label_direccion.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.direccion_entry = ttk.Entry(self)
        self.direccion_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.direccion_entry.insert(0, cliente_seleccionado[3])

        # Botón para guardar los cambios
        self.btn_guardar = ttk.Button(self, text="Guardar", command=self.guardar_cambios)
        self.btn_guardar.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    def guardar_cambios(self):
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        direccion = self.direccion_entry.get()
        id_cliente = self.cliente_app.tree.item(self.cliente_app.tree.selection(), "values")[0]
        self.cliente_app.actualizar_cliente(id_cliente, nombre, apellido, direccion)
        self.destroy()


if __name__ == "__main__":
    conexion = sqlite3.connect("clientes.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            direccion TEXT
        )
    """)
    conexion.commit()
    conexion.close()

    root = tk.Tk()
    app = ClienteApp(root)
    root.mainloop()
