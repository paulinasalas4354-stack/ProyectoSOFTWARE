from tkinter import messagebox
from conexion import Conexion
from usuarios import Usuario
import mysql.connector

class dbUsuario:

    def autentificar(self, username_ingresado, password_ingresado):
        con = Conexion()
        conn = con.abrir()
        if not conn:
            return None
        
        usuario_autenticado = None
        try:
            cursor = conn.cursor()
            sql = "SELECT * FROM usuarios WHERE username = %s"
            cursor.execute(sql, (username_ingresado,))
            fila_usuario = cursor.fetchone()

            if fila_usuario:
                password_bd = fila_usuario[6]
                
                if password_ingresado == password_bd:
                    usuario_autenticado = Usuario()
                    usuario_autenticado.set_usuario_id(fila_usuario[0])
                    usuario_autenticado.set_nombre(fila_usuario[1])
                    usuario_autenticado.set_APaterno(fila_usuario[2])
                    usuario_autenticado.set_AMaterno(fila_usuario[3])
                    usuario_autenticado.set_email(fila_usuario[4])
                    usuario_autenticado.set_username(fila_usuario[5])
                    usuario_autenticado.set_password(fila_usuario[6])
                    usuario_autenticado.set_perfil(fila_usuario[7])
                else:
                    messagebox.showwarning("Acceso Denegado", "La contraseña es incorrecta.")
            else:
                messagebox.showwarning("Acceso Denegado", f"El usuario '{username_ingresado}' no existe.")
        except Exception as e:
            messagebox.showerror("Error en la Consulta", f"Ocurrió un error: {e}")
        finally:
            con.cerrar()
        
        return usuario_autenticado
    
    def username_existe(self, username, excluir_id=None):
        con = Conexion()
        conn = con.abrir()
        if not conn: 
            return False

        existe = False
        try:
            cursor = conn.cursor()
            if excluir_id:
                sql = "SELECT COUNT(*) FROM usuarios WHERE username = %s AND usuario_id != %s"
                cursor.execute(sql, (username, excluir_id))
            else:
                sql = "SELECT COUNT(*) FROM usuarios WHERE username = %s"
                cursor.execute(sql, (username,))
            
            existe = cursor.fetchone()[0] > 0 
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Validación", f"Error al verificar username en BD: {err}")
        except Exception as e:
            messagebox.showerror("Error General", f"Error inesperado al verificar username: {e}")
        finally:
            con.cerrar()
        return existe

    def email_existe(self, email, excluir_id=None):
        """Verifica si el email ya está registrado"""
        con = Conexion()
        conn = con.abrir()
        if not conn: 
            return False

        existe = False
        try:
            cursor = conn.cursor()
            if excluir_id:
                sql = "SELECT COUNT(*) FROM usuarios WHERE email = %s AND usuario_id != %s"
                cursor.execute(sql, (email, excluir_id))
            else:
                sql = "SELECT COUNT(*) FROM usuarios WHERE email = %s"
                cursor.execute(sql, (email,))
            
            existe = cursor.fetchone()[0] > 0 
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Validación", f"Error al verificar email en BD: {err}")
        except Exception as e:
            messagebox.showerror("Error General", f"Error inesperado al verificar email: {e}")
        finally:
            con.cerrar()
        return existe

    def crear_usuario(self, usuario):
        con = Conexion()
        conn = con.abrir()
        if not conn: 
            return False

        try:
            cursor = conn.cursor()
            sql = "INSERT INTO usuarios (nombre, APaterno, AMaterno, email, username, password, perfil) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            
            valores = (
                usuario.get_nombre(),
                usuario.get_APaterno(),
                usuario.get_AMaterno(),
                usuario.get_email(),
                usuario.get_username(),
                usuario.get_password(),
                usuario.get_perfil()
            )
            cursor.execute(sql, valores)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Error al Crear", f"Error en la base de datos al crear usuario: {err}")
        except Exception as e:
            messagebox.showerror("Error General", f"Error inesperado al crear usuario: {e}")
        finally:
            con.cerrar()
        return False

    def editar_usuario(self, usuario):
        con = Conexion()
        conn = con.abrir()
        if not conn: 
            return False

        try:
            cursor = conn.cursor()
            sql = """
                UPDATE usuarios SET 
                nombre = %s, APaterno = %s, AMaterno = %s, email = %s, 
                username = %s, password = %s, perfil = %s 
                WHERE usuario_id = %s
            """
            
            valores = (
                usuario.get_nombre(),
                usuario.get_APaterno(),
                usuario.get_AMaterno(),
                usuario.get_email(),
                usuario.get_username(),
                usuario.get_password(),
                usuario.get_perfil(),
                usuario.get_usuario_id()
            )
            cursor.execute(sql, valores)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Error al Editar", f"Error en la base de datos al editar usuario: {err}")
        except Exception as e:
            messagebox.showerror("Error General", f"Error inesperado al editar usuario: {e}")
        finally:
            con.cerrar()
        return False

    def eliminar_usuario(self, usuario_id):
        con = Conexion()
        conn = con.abrir()
        if not conn: 
            return False

        try:
            cursor = conn.cursor()
            sql = "DELETE FROM usuarios WHERE usuario_id = %s"
            cursor.execute(sql, (usuario_id,))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            if "Foreign key constraint fails" in str(err):
                messagebox.showerror("Error de Eliminación", "No se puede eliminar el usuario porque está asociado a otros registros.")
            else:
                messagebox.showerror("Error al Eliminar", f"Error en la base de datos al eliminar usuario: {err}")
        except Exception as e:
            messagebox.showerror("Error General", f"Error inesperado al eliminar usuario: {e}")
        finally:
            con.cerrar()
        return False

    def buscar_todos(self):
        con = Conexion()
        conn = con.abrir()
        if not conn: 
            return []

        lista_usuarios = []
        try:
            cursor = conn.cursor()
            sql = "SELECT usuario_id, nombre, APaterno, AMaterno, email, username, perfil FROM usuarios"
            cursor.execute(sql)
            resultados = cursor.fetchall()

            for fila in resultados:
                usuario = Usuario()
                usuario.set_usuario_id(fila[0])
                usuario.set_nombre(fila[1])
                usuario.set_APaterno(fila[2])
                usuario.set_AMaterno(fila[3])
                usuario.set_email(fila[4])
                usuario.set_username(fila[5])
                usuario.set_perfil(fila[6]) 
                lista_usuarios.append(usuario)
        except mysql.connector.Error as err:
            messagebox.showerror("Error al Cargar", f"Error en la base de datos al cargar usuarios: {err}")
        except Exception as e:
            messagebox.showerror("Error General", f"Error inesperado al cargar usuarios: {e}")
        finally:
            con.cerrar()
        return lista_usuarios
    
    def buscar_por_id(self, usuario_id):
        con = Conexion()
        conn = con.abrir()
        if not conn: 
            return None

        usuario = None
        try:
            cursor = conn.cursor()
            sql = "SELECT usuario_id, nombre, APaterno, AMaterno, email, username, password, perfil FROM usuarios WHERE usuario_id = %s"
            cursor.execute(sql, (usuario_id,))
            fila_usuario = cursor.fetchone()

            if fila_usuario:
                usuario = Usuario()
                usuario.set_usuario_id(fila_usuario[0])
                usuario.set_nombre(fila_usuario[1])
                usuario.set_APaterno(fila_usuario[2])
                usuario.set_AMaterno(fila_usuario[3])
                usuario.set_email(fila_usuario[4])
                usuario.set_username(fila_usuario[5])
                usuario.set_password(fila_usuario[6])
                usuario.set_perfil(fila_usuario[7])
        except mysql.connector.Error as err:
            messagebox.showerror("Error al Buscar", f"Error en la base de datos al buscar usuario: {err}")
        except Exception as e:
            messagebox.showerror("Error General", f"Error inesperado al buscar usuario: {e}")
        finally:
            con.cerrar()
        return usuario
