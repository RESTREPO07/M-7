import mysql.connector
from decimal import Decimal

class Usuario:
    def __init__(self, id_usuario, usuario, contraseña):
        self.id_usuario = id_usuario
        self.usuario = usuario
        self.contraseña = contraseña

class CajeroDatabase:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cajero2"
        )
        self.cursor = self.conexion.cursor()
        self.usuario_actual = None

    def iniciar_sesion(self, usuario, contraseña):
        query = "SELECT * FROM usuario WHERE Usuario = %s AND Contraseña = %s"
        values = (usuario, contraseña)
        self.cursor.execute(query, values)
        usuario = self.cursor.fetchone()
        if usuario:
            self.usuario_actual = Usuario(usuario[0], usuario[1], usuario[2])
            return True
        else:
            return False

    def registrarse(self, usuario, contraseña):
        query_usuario = "INSERT INTO usuario (Usuario, Contraseña) VALUES (%s, %s)"
        values_usuario = (usuario, contraseña)
        query_cuenta = "INSERT INTO Cuenta (Saldo, ID_usuario) VALUES (%s, %s)"
        try:
            self.cursor.execute(query_usuario, values_usuario)
            self.conexion.commit()
            id_usuario = self.cursor.lastrowid
            self.cursor.execute(query_cuenta, (0, id_usuario))
            self.conexion.commit()
            return True
        except mysql.connector.Error as error:
            return False

    def obtener_saldo(self):
        if self.usuario_actual:
            query = "SELECT Saldo FROM Cuenta WHERE ID_usuario = %s"
            self.cursor.execute(query, (self.usuario_actual.id_usuario,))
            resultado = self.cursor.fetchone()
            if resultado:
                saldo = resultado[0]
                return saldo
        return None

    def depositar(self, cantidad):
        saldo_actual = self.obtener_saldo()
        if saldo_actual is not None:
            nuevo_saldo = saldo_actual + cantidad
            query = "UPDATE Cuenta SET Saldo = %s WHERE ID_usuario = %s"
            values = (nuevo_saldo, self.usuario_actual.id_usuario)
            self.cursor.execute(query, values)
            self.conexion.commit()
            return True
        return False

    def retirar(self, cantidad):
        saldo_actual = self.obtener_saldo()
        if saldo_actual is not None:
            if cantidad > saldo_actual:
                return False
            else:
                nuevo_saldo = saldo_actual - cantidad
                query = "UPDATE Cuenta SET Saldo = %s WHERE ID_usuario = %s"
                values = (nuevo_saldo, self.usuario_actual.id_usuario)
                self.cursor.execute(query, values)
                self.conexion.commit()
                return True
        return False
