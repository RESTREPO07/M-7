import tkinter as tk
import mysql.connector

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
        query = "INSERT INTO usuario (Usuario, Contraseña) VALUES (%s, %s)"
        values = (usuario, contraseña)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            print(f"Error al crear la cuenta: {error}")
            return False

    def iniciar_sesion(self, usuario, contraseña):
        query = "SELECT Saldo FROM usuario WHERE Usuario = %s AND Contraseña = %s"
        values = (usuario, contraseña)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result[0] if result else None  # Retorna el saldo si la sesión es exitosa

    def depositar_dinero(self, usuario, cantidad):
        query = "UPDATE usuario SET Saldo = Saldo + %s WHERE Usuario = %s"
        values = (cantidad, usuario)
        self.cursor.execute(query, values)
        self.connection.commit()

    def retirar_dinero(self, usuario, cantidad):
        query = "UPDATE usuario SET Saldo = Saldo - %s WHERE Usuario = %s"
        values = (cantidad, usuario)
        self.cursor.execute(query, values)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

# Función para manejar el evento de iniciar sesión
def iniciar_sesion():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    db = Database()
    saldo = db.iniciar_sesion(usuario, contraseña)
    if saldo is not None:
        print("Inicio de sesión exitoso.")
        mostrar_opciones(db, usuario, saldo)
    else:
        print("Error: Nombre de usuario o contraseña incorrectos.")

# Función para mostrar opciones después del inicio de sesión
def mostrar_opciones(db, usuario, saldo):
    saldo_label.config(text=f"Saldo actual: ${saldo}")
    saldo_label.pack()

    # Botón para depositar dinero
    boton_depositar = tk.Button(ventana, text="Depositar", command=lambda: depositar_dinero(db, usuario))
    boton_depositar.pack()

    # Botón para retirar dinero
    boton_retirar = tk.Button(ventana, text="Retirar", command=lambda: retirar_dinero(db, usuario))
    boton_retirar.pack()

# Función para manejar el evento de depositar dinero
def depositar_dinero(db, usuario):
    cantidad = float(entry_cantidad.get())
    db.depositar_dinero(usuario, cantidad)
    print("Depósito realizado con éxito.")
    mostrar_saldo_actual(db, usuario)

# Función para manejar el evento de retirar dinero
def retirar_dinero(db, usuario):
    cantidad = float(entry_cantidad.get())
    db.retirar_dinero(usuario, cantidad)
    print("Retiro realizado con éxito.")
    mostrar_saldo_actual(db, usuario)

# Función para mostrar el saldo actualizado después de depositar o retirar dinero
def mostrar_saldo_actual(db, usuario):
    saldo = db.iniciar_sesion(usuario, entry_contraseña.get())
    saldo_label.config(text=f"Saldo actual: ${saldo}")

# Función para manejar el evento de crear cuenta
def crear_cuenta():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    if usuario and contraseña:  
        db = Database()
        if db.crear_cuenta(usuario, contraseña):
            print("Cuenta creada con éxito.")
        else:
            print("Error: El nombre de usuario ya existe. Por favor, elija otro.")
    else:
        print("Error: Por favor, ingrese un nombre de usuario y una contraseña.")

# Crear una instancia de la ventana principal
ventana = tk.Tk()

# Configurar las dimensiones de la ventana
ventana.geometry("400x250")

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
entry_contraseña = tk.Entry(ventana, show="*")  
entry_contraseña.pack()

# Campo de entrada para la cantidad de dinero
label_cantidad = tk.Label(ventana, text="Cantidad:")
label_cantidad.pack()
entry_cantidad = tk.Entry(ventana)
entry_cantidad.pack()

# Etiqueta para mostrar el saldo actual
saldo_label = tk.Label(ventana, text="")

# Botón para iniciar sesión
boton_iniciar_sesion = tk.Button(ventana, text="Iniciar sesión", command=iniciar_sesion)
boton_iniciar_sesion.pack()

# Botón para crear una cuenta
boton_crear_cuenta = tk.Button(ventana, text="Crear cuenta", command=crear_cuenta)
boton_crear_cuenta.pack()

# Ejecutar el bucle principal de la aplicación
ventana.mainloop()
