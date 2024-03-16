import tkinter as tk
from tk import CajeroInterfaz

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Cajero Automático")
ventana.configure(bg="#E0E0E0")

cajero_interfaz = CajeroInterfaz(ventana)

ventana.mainloop()
