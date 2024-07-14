import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import restaurante
from PIL import Image, ImageTk

class RestauranteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Restaurante")
        self.root.configure(background='light blue')
        
        icon_path = "img2.png"
        icon = Image.open(icon_path)
        icon_tk = ImageTk.PhotoImage(icon)
        root.iconphoto(True, icon_tk)

        # Marco principal
        self.frame = ttk.Frame(self.root, width=400)
        self.frame.grid(row=0, column=0, padx=15, pady=15)

        # Título y línea horizontal
        self.label_titulo = ttk.Label(self.frame, text="Gestión de Platos", font=("Helvetica", 14, "bold"))
        self.label_titulo.grid(row=0, column=0, columnspan=5, pady=(0, 10))
        self.linea_horizontal = ttk.Separator(self.frame, orient="horizontal")
        self.linea_horizontal.grid(row=1, column=0, columnspan=5, sticky="ew", pady=(0, 10))

        # Campos de entrada para platos
        self.label_nombre = ttk.Label(self.frame, text="Nombre del plato:")
        self.label_nombre.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry = ttk.Entry(self.frame)
        self.nombre_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.label_categoria = ttk.Label(self.frame, text="Categoría:")
        self.label_categoria.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.categoria_combobox = ttk.Combobox(self.frame, state="readonly")
        self.categoria_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.label_precio = ttk.Label(self.frame, text="Precio del plato:")
        self.label_precio.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.precio_entry = ttk.Entry(self.frame)
        self.precio_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Botones para platos
        self.btn_guardar = ttk.Button(self.frame, text="Guardar", command=self.guardar_plato)
        self.btn_guardar.grid(row=5, column=0, padx=5, pady=5, sticky="we")

        self.btn_actualizar = ttk.Button(self.frame, text="Actualizar", command=self.abrir_ventana_actualizar)
        self.btn_actualizar.grid(row=5, column=1, padx=5, pady=5, sticky="we")

        self.btn_eliminar = ttk.Button(self.frame, text="Eliminar", command=self.eliminar_plato)
        self.btn_eliminar.grid(row=5, column=2, padx=5, pady=5, sticky="we")

        # Campos de entrada para categorías
        self.label_nombre_categoria = ttk.Label(self.frame, text="Nombre de la categoría:")
        self.label_nombre_categoria.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.nombre_categoria_entry = ttk.Entry(self.frame)
        self.nombre_categoria_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Botones para categorías
        self.btn_guardar_categoria = ttk.Button(self.frame, text="Crear Categoría", command=self.guardar_categoria)
        self.btn_guardar_categoria.grid(row=6, column=2, padx=5, pady=5, sticky="we")

        # Botón para mostrar menú
        self.btn_mostrar_menu = ttk.Button(self.frame, text="Mostrar Menú", command=self.mostrar_menu)
        self.btn_mostrar_menu.grid(row=7, column=0, columnspan=4, padx=5, pady=5, sticky="we")

        # Tabla de platos
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre", "Categoría", "Precio"), show="headings")
        self.tree.heading("ID", text="ID del plato", anchor=tk.CENTER)
        self.tree.heading("Nombre", text="Nombre del plato", anchor=tk.CENTER)
        self.tree.heading("Categoría", text="Categoría", anchor=tk.CENTER)
        self.tree.heading("Precio", text="Precio", anchor=tk.CENTER)

        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Nombre", width=150, anchor=tk.CENTER)
        self.tree.column("Categoría", width=150, anchor=tk.CENTER)
        self.tree.column("Precio", width=100, anchor=tk.CENTER)

        self.tree.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="ew")

        self.cargar_categorias()
        self.cargar_platos()

    def ejecutar_consulta(self, query, parametros=(), fetchall=False):
        conn = sqlite3.connect("restaurante.db")
        cursor = conn.cursor()
        resultado = cursor.execute(query, parametros)
        if fetchall:
            resultado = resultado.fetchall()
        else:
            conn.commit()
        conn.close()
        return resultado

    def cargar_categorias(self):
        categorias = restaurante.obtener_categorias()
        # Verificar si la categoría "Postres" está presente
        postres_index = -1
        for i, categoria in enumerate(categorias):
            if categoria[1] == "primero":
                postres_index = i
                break
        # Si "Postres" está presente, moverla al principio de la lista
        if postres_index != -1:
            categorias.insert(0, categorias.pop(postres_index))
        # Cargar las categorías en el Combobox
        self.categoria_combobox['values'] = [categoria[1] for categoria in categorias]


    def cargar_platos(self):
        self.tree.delete(*self.tree.get_children())
        platos = restaurante.obtener_platos()
        for plato in platos:
            self.tree.insert("", "end", values=plato)

    def guardar_plato(self):
        nombre = self.nombre_entry.get()
        categoria_nombre = self.categoria_combobox.get()
        categorias = restaurante.obtener_categorias()
        categoria_id = None
        for categoria in categorias:
            if categoria[1] == categoria_nombre:
                categoria_id = categoria[0]
                break
        precio = self.precio_entry.get()
        try:
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número.")
            return
        if nombre and categoria_id:
            resultado = restaurante.insertar_plato(nombre, categoria_id, precio)
            self.nombre_entry.delete(0, tk.END)
            self.categoria_combobox.set("")
            self.precio_entry.delete(0, tk.END)
            self.cargar_platos()
            messagebox.showinfo("Éxito", resultado)
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    def abrir_ventana_actualizar(self):
        item = self.tree.selection()
        if item:
            plato_seleccionado = self.tree.item(item, "values")
            VentanaActualizar(self.root, plato_seleccionado, self)
        else:
            messagebox.showerror("Error", "Por favor, seleccione un plato para actualizar.")

    def actualizar_plato(self, id_plato, nombre, categoria_id, precio):
        resultado = restaurante.actualizar_plato(id_plato, nombre, categoria_id, precio)
        self.cargar_platos()
        messagebox.showinfo("Éxito", resultado)

    def eliminar_plato(self):
        item = self.tree.selection()
        if item:
            id_plato = self.tree.item(item, "values")[0]
            resultado = restaurante.eliminar_plato(id_plato)
            self.cargar_platos()
            messagebox.showinfo("Éxito", resultado)
        else:
            messagebox.showerror("Error", "Por favor, seleccione un plato para eliminar.")
    def guardar_categoria(self):
        nombre_categoria = self.nombre_categoria_entry.get()
        if nombre_categoria:
            resultado = restaurante.insertar_categoria(nombre_categoria)
            self.nombre_categoria_entry.delete(0, tk.END)
            if resultado.startswith("Éxito"):
                
                categorias = [categoria[0] for categoria in restaurante.obtener_categorias()]

                self.categoria_combobox['values'] = categorias
            messagebox.showinfo("Éxito", resultado)
        else:
            messagebox.showerror("Error", "Por favor, ingrese el nombre de la categoría.")


    def eliminar_categoria(self):
        categoria_seleccionada = self.categoria_combobox.get()
        categorias = restaurante.obtener_categorias()
        id_categoria = None
        for categoria in categorias:
            if categoria[1] == categoria_seleccionada:
                id_categoria = categoria[0]
                break
        if id_categoria:
            resultado = restaurante.eliminar_categoria(id_categoria)
            if resultado.startswith("Éxito"):
                self.cargar_categorias()
                self.categoria_combobox.set("")
            messagebox.showinfo("Éxito", resultado)
        else:
            messagebox.showerror("Error", "Por favor, seleccione una categoría para eliminar.")

    def mostrar_menu(self):
        conn = sqlite3.connect('restaurante.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT categoria.nombre, plato.nombre
        FROM categoria
        LEFT JOIN plato ON categoria.id = plato.categoria_id
        ORDER BY categoria.nombre
        ''')
        
        registros = cursor.fetchall()
        conn.close()
        
        # Crear una nueva ventana
        menu_window = tk.Toplevel()
        menu_window.title("Menú del Restaurante")
        menu_window.geometry("300x300")  # Ancho: 300, Alto: 300
        
        # Crear etiquetas para mostrar las categorías y platos
        current_category = None
        for categoria, plato in registros:
            if categoria != current_category:
                current_category = categoria
                categoria_label = tk.Label(menu_window, text=categoria, font=("Helvetica", 12, "bold"))
                categoria_label.pack(anchor="w", padx=10, pady=5)
            plato_label = tk.Label(menu_window, text=plato if plato else "No hay platos en esta categoría")
            plato_label.pack(anchor="w", padx=20, pady=2)

class VentanaActualizar(tk.Toplevel):
    def __init__(self, parent, plato_seleccionado, main_app):
        super().__init__(parent)
        self.title("Actualizar Plato")
        self.main_app = main_app

        self.label_nombre = ttk.Label(self, text="Nombre del plato:")
        self.label_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry = ttk.Entry(self)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.nombre_entry.insert(0, plato_seleccionado[1])

        self.label_categoria = ttk.Label(self, text="Categoría:")
        self.label_categoria.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.categoria_combobox = ttk.Combobox(self, state="readonly")
        self.categoria_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.categoria_combobox['values'] = [categoria[1] for categoria in restaurante.obtener_categorias()]
        self.categoria_combobox.set(plato_seleccionado[2])

        self.label_precio = ttk.Label(self, text="Precio del plato:")
        self.label_precio.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.precio_entry = ttk.Entry(self)
        self.precio_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.precio_entry.insert(0, plato_seleccionado[3])

        self.btn_guardar = ttk.Button(self, text="Guardar", command=self.guardar_cambios)
        self.btn_guardar.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    def guardar_cambios(self):
        nombre = self.nombre_entry.get()
        categoria_nombre = self.categoria_combobox.get()
        categorias = restaurante.obtener_categorias()
        categoria_id = None
        for categoria in categorias:
            if categoria[1] == categoria_nombre:
                categoria_id = categoria[0]
                break
        precio = self.precio_entry.get()
        try:
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número.")
            return
        id_plato = self.main_app.tree.item(self.main_app.tree.selection(), "values")[0]
        resultado = self.main_app.actualizar_plato(id_plato, nombre, categoria_id, precio)
        self.destroy()

if __name__ == "__main__":
    restaurante.crear_bd()
    root = tk.Tk()
    app = RestauranteApp(root)
    root.mainloop()
