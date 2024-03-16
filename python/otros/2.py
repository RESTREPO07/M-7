# database.py

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
        self.cursor.execute(query, values)
        self.connection.commit()

    def iniciar_sesion(self, usuario, contraseña):
        query = "SELECT * FROM usuario WHERE Usuario = %s AND Contraseña = %s"
        values = (usuario, contraseña)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result is not None

    def close(self):
        self.cursor.close()
        self.connection.close()
