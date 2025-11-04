import mysql.connector
from tkinter import messagebox

class Conexion:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "sistema_de_control_escolar" 
        self.conn = None

    def conectar(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Conexión exitosa a la base de datos.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {err}")
            self.conn = None
    
    def cerrar(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
