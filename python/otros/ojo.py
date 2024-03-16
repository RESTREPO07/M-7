import mysql.connector
import tkinter as tk

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cajero"
        )
        self.cursor = self.connection.cursor()

    def crear_cuenta(self, usuario, contraseña):
        # Verificar si el usuario ya existe
        query = "SELECT * FROM usuario WHERE Usuario = %s"
        values = (usuario,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        if result:
            print("Error: El nombre de usuario ya existe. Por favor, elija otro.")
            return False
        else:
            # Insertar nuevo usuario
            query = "INSERT INTO usuario (Usuario, Contraseña) VALUES (%s, %s)"
            values = (usuario, contraseña)
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Cuenta creada con éxito.")
            return True

    # Otros métodos de la clase Database...

# Función para manejar el evento de crear cuenta
def crear_cuenta():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    if usuario and contraseña:  # Verificar si se ingresaron usuario y contraseña
        db = Database()
        db.crear_cuenta(usuario, contraseña)
    else:
        print("Error: Por favor, ingrese un nombre de usuario y una contraseña.")

# Función para manejar el evento de iniciar sesión (sin cambios)
def iniciar_sesion():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    # Implementación omitida por brevedad

# Crear una instancia de la ventana principal
ventana = tk.Tk()

# Configurar las dimensiones de la ventana
ventana.geometry("400x200")

# Añadir un título a la ventana
ventana.title("Cajero")

# Etiqueta y campo de entrada para el nombre de usuario
label_usuario = tk.Label(ventana, text="Nombre de usuario:")
label_usuario.pack()
entry_usuario = tk.Entry(ventana)
entry_usuario.pack()

# Etiqueta y campo de entrada para la contraseña
label_contraseña = tk.Label(ventana, text="Contraseña:")
label_contraseña.pack()
entry_contraseña = tk.Entry(ventana, show="*")  # Para ocultar la contraseña
entry_contraseña.pack()

# Botón para crear una cuenta
boton_crear_cuenta = tk.Button(ventana, text="Crear cuenta", command=crear_cuenta)
boton_crear_cuenta.pack()

# Botón para iniciar sesión (sin cambios)
boton_iniciar_sesion = tk.Button(ventana, text="Iniciar sesión", command=iniciar_sesion)
boton_iniciar_sesion.pack()

# Ejecutar el bucle principal de la aplicación
ventana.mainloop()
