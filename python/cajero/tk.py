import tkinter as tk
from database import CajeroDatabase
from decimal import Decimal

class CajeroInterfaz:
    def __init__(self, ventana):
        self.ventana = ventana
        self.cajero = CajeroDatabase()

        # Configurar el evento de cierre de ventana
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        label_usuario = tk.Label(ventana, text="Usuario:", bg="#E0E0E0", fg="#333333", font=("Arial", 10))
        label_usuario.grid(row=0, column=0, padx=5, pady=5)
        self.entry_usuario = tk.Entry(ventana)
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=5)

        label_contraseña = tk.Label(ventana, text="Contraseña:", bg="#E0E0E0", fg="#333333", font=("Arial", 10))
        label_contraseña.grid(row=1, column=0, padx=5, pady=5)
        self.entry_contraseña = tk.Entry(ventana, show="*")
        self.entry_contraseña.grid(row=1, column=1, padx=5, pady=5)

        self.boton_iniciar_sesion = tk.Button(ventana, text="Iniciar sesión", command=self.iniciar_sesion, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        self.boton_iniciar_sesion.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        label_registro = tk.Label(ventana, text="¿No tienes una cuenta? Regístrate:", bg="#E0E0E0", fg="#333333", font=("Arial", 10))
        label_registro.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.boton_registrarse = tk.Button(ventana, text="Registrarse", command=self.registrarse, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.boton_registrarse.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.label_mensaje = tk.Label(ventana, text="", fg="black", bg="#E0E0E0", font=("Arial", 10))
        self.label_mensaje.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        if usuario and contraseña:
            resultado = self.cajero.iniciar_sesion(usuario, contraseña)
            if resultado:
                self.mostrar_mensaje("Inicio de sesión exitoso", "Inicio de sesión exitoso.")
                self.mostrar_opciones()
            else:
                self.mostrar_mensaje("Error de inicio de sesión", "Nombre de usuario o contraseña incorrectos.")
        else:
            self.mostrar_mensaje("Error", "Por favor ingrese usuario y contraseña.")

    def registrarse(self):
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        if usuario and contraseña:
            resultado = self.cajero.registrarse(usuario, contraseña)
            if resultado:
                self.mostrar_mensaje("Registro exitoso", "Usuario creado con éxito.")
            else:
                self.mostrar_mensaje("Error", "Error al crear el usuario.")
        else:
            self.mostrar_mensaje("Error", "Por favor ingrese usuario y contraseña.")

    def mostrar_opciones(self):
        if self.cajero.usuario_actual:
            if self.cajero.usuario_actual.id_usuario:
                self.ventana_opciones = tk.Toplevel(self.ventana)
                self.ventana_opciones.title("Opciones")
                self.ventana_opciones.configure(bg="#E0E0E0")
                
                self.label_saldo = tk.Label(self.ventana_opciones, text=f"Saldo actual: ${self.cajero.obtener_saldo()}", bg="#E0E0E0", fg="#333333", font=("Arial", 12, "bold"))
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
            self.mostrar_mensaje("Error", "Por favor inicie sesión primero.")

    def depositar_monto(self):
        cantidad = Decimal(self.entry_monto.get())
        self.cajero.depositar(cantidad)
        self.mostrar_mensaje("Depósito exitoso", "Depósito realizado con éxito.")

    def retirar_monto(self):
        cantidad = Decimal(self.entry_monto.get())
        saldo_actual = self.cajero.obtener_saldo()
        if saldo_actual is not None:
            if cantidad <= saldo_actual:
                self.cajero.retirar(cantidad)
                self.mostrar_mensaje("Retiro exitoso", "Retiro realizado con éxito.")
            else:
                self.mostrar_mensaje("Error", "No tiene suficiente saldo para realizar este retiro.")
        else:
            self.mostrar_mensaje("Error", "No se pudo obtener el saldo.")

    def mostrar_mensaje(self, titulo, mensaje):
        self.label_mensaje.config(text=f"{titulo}: {mensaje}", fg="black")

    def cerrar_aplicacion(self):
        # Cerrar la ventana principal (y la aplicación)
        self.ventana.destroy()

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Cajero Automático")
ventana.configure(bg="#E0E0E0")

cajero_interfaz = CajeroInterfaz(ventana)

ventana.mainloop()
