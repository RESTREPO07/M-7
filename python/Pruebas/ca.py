import tkinter as tk
import mysql.connector
from decimal import Decimal

class Usuario:
    def __init__(self, id_usuario, usuario, contraseña):
        self.id_usuario = id_usuario
        self.usuario = usuario
        self.contraseña = contraseña

class Cajero:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cajero2"
        )
        self.cursor = self.conexion.cursor()
        self.usuario_actual = None
        self.ventana_opciones = None
        self.label_mensaje = None

    def crear_usuario(self, usuario, contraseña):
        query_usuario = "INSERT INTO usuario (Usuario, Contraseña) VALUES (%s, %s)"
        values_usuario = (usuario, contraseña)
        query_cuenta = "INSERT INTO Cuenta (Saldo, ID_usuario) VALUES (%s, %s)"
        try:
            self.cursor.execute(query_usuario, values_usuario)
            self.conexion.commit()
            id_usuario = self.cursor.lastrowid
            self.cursor.execute(query_cuenta, (0, id_usuario))
            self.conexion.commit()
            self.mostrar_mensaje("Registro exitoso", "Usuario creado con éxito.", color="green")
        except mysql.connector.Error as error:
            self.mostrar_mensaje("Error", f"Error al crear el usuario: {error}", color="red")

    def iniciar_sesion(self, usuario, contraseña):
        query = "SELECT * FROM usuario WHERE Usuario = %s AND Contraseña = %s"
        values = (usuario, contraseña)
        self.cursor.execute(query, values)
        usuario = self.cursor.fetchone()
        if usuario:
            self.usuario_actual = Usuario(usuario[0], usuario[1], usuario[2])
            self.mostrar_opciones()
            self.mostrar_mensaje("Inicio de sesión exitoso", "Inicio de sesión exitoso.", color="green")
        else:
            self.mostrar_mensaje("Error de inicio de sesión", "Nombre de usuario o contraseña incorrectos.", color="red")

    def obtener_saldo(self):
        query = "SELECT Saldo FROM Cuenta WHERE ID_usuario = %s"
        self.cursor.execute(query, (self.usuario_actual.id_usuario,))
        resultado = self.cursor.fetchone()
        if resultado:
            saldo = resultado[0]
            return saldo
        else:
            self.mostrar_mensaje("Error", "No se encontró información de saldo para este usuario.", color="red")
            return None

    def depositar(self, cantidad):
        saldo_actual = self.obtener_saldo()
        if saldo_actual is not None:
            nuevo_saldo = saldo_actual + cantidad
            query = "UPDATE Cuenta SET Saldo = %s WHERE ID_usuario = %s"
            values = (nuevo_saldo, self.usuario_actual.id_usuario)
            self.cursor.execute(query, values)
            self.conexion.commit()
            self.label_saldo.config(text=f"Saldo actual: ${nuevo_saldo}")
            self.mostrar_mensaje("Depósito exitoso", "Depósito realizado con éxito.", color="green")

    def retirar(self, cantidad):
        saldo_actual = self.obtener_saldo()
        if saldo_actual is not None:
            if cantidad > saldo_actual:
                self.mostrar_mensaje("Error", "No tiene suficiente saldo para realizar este retiro.", color="red")
            else:
                nuevo_saldo = saldo_actual - cantidad
                query = "UPDATE Cuenta SET Saldo = %s WHERE ID_usuario = %s"
                values = (nuevo_saldo, self.usuario_actual.id_usuario)
                self.cursor.execute(query, values)
                self.conexion.commit()
                self.label_saldo.config(text=f"Saldo actual: ${nuevo_saldo}")
                self.mostrar_mensaje("Retiro exitoso", "Retiro realizado con éxito.", color="green")

    def mostrar_opciones(self):
        if self.ventana_opciones is None:
            self.ventana_opciones = tk.Toplevel()
            self.ventana_opciones.title("Opciones")
            self.ventana_opciones.configure(bg="#E0E0E0")
            
            self.label_saldo = tk.Label(self.ventana_opciones, text=f"Saldo actual: ${self.obtener_saldo()}", bg="#E0E0E0", fg="#333333", font=("Arial", 12, "bold"))
            self.label_saldo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            label_monto = tk.Label(self.ventana_opciones, text="Monto:", bg="#E0E0E0", fg="#333333", font=("Arial", 10))
            label_monto.grid(row=1, column=0, padx=5, pady=5)
            self.entry_monto = tk.Entry(self.ventana_opciones)
            self.entry_monto.grid(row=1, column=1, padx=5, pady=5)

            boton_depositar = tk.Button(self.ventana_opciones, text="Depositar", command=self.depositar_monto, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
            boton_depositar.grid(row=2, column=0, padx=5, pady=5)

            boton_retirar = tk.Button(self.ventana_opciones, text="Retirar", command=self.retirar_monto, bg="#f44336", fg="white", font=("Arial", 10, "bold"))
            boton_retirar.grid(row=2, column=1, padx=5, pady=5)
        else:
            self.label_saldo.config(text=f"Saldo actual: ${self.obtener_saldo()}")

    def depositar_monto(self):
        cantidad = Decimal(self.entry_monto.get())
        self.depositar(cantidad)

    def retirar_monto(self):
        cantidad = Decimal(self.entry_monto.get())
        self.retirar(cantidad)

    def mostrar_mensaje(self, titulo, mensaje, color):
        if self.label_mensaje:
            self.label_mensaje.destroy()
        self.label_mensaje = tk.Label(self.ventana_opciones if self.ventana_opciones else ventana, text=f"{titulo}: {mensaje}", fg=color, bg="#E0E0E0", font=("Arial", 10))
        self.label_mensaje.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

cajero = Cajero()

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Cajero Automático")
ventana.configure(bg="#E0E0E0")

label_usuario = tk.Label(ventana, text="Usuario:", bg="#E0E0E0", fg="#333333", font=("Arial", 10))
label_usuario.grid(row=0, column=0, padx=5, pady=5)
entry_usuario = tk.Entry(ventana)
entry_usuario.grid(row=0, column=1, padx=5, pady=5)

label_contraseña = tk.Label(ventana, text="Contraseña:", bg="#E0E0E0", fg="#333333", font=("Arial", 10))
label_contraseña.grid(row=1, column=0, padx=5, pady=5)
entry_contraseña = tk.Entry(ventana, show="*")
entry_contraseña.grid(row=1, column=1, padx=5, pady=5)

boton_iniciar_sesion = tk.Button(ventana, text="Iniciar sesión", command=lambda: cajero.iniciar_sesion(entry_usuario.get(), entry_contraseña.get()), bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
boton_iniciar_sesion.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

label_registro = tk.Label(ventana, text="¿No tienes una cuenta? Regístrate:", bg="#E0E0E0", fg="#333333", font=("Arial", 10))
label_registro.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

boton_registrarse = tk.Button(ventana, text="Registrarse", command=lambda: cajero.crear_usuario(entry_usuario.get(), entry_contraseña.get()), bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
boton_registrarse.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

ventana.mainloop()
