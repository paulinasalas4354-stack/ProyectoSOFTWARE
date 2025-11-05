import mysql.connector
import conexion as con
import Materias as mat

class dbMaterias:

    def salvarMateria(self, materia):
        
        try:
            conexion = con.conexion()
            conn = conexion.open()
            cursor = conn.cursor()
      
            sql = """
                INSERT INTO materias(codigo, id, asignatura, creditos, semestre, carrera)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            datos = (
                materia.getCodigo(),
                materia.getId(),
                materia.getAsignatura(),
                materia.getCreditos(),
                materia.getSemestre(),
                materia.getCarrera()
            )
            cursor.execute(sql, datos)
            conn.commit()
            conn.close()
            return True
        except mysql.connector.Error as err:
            raise err

    def buscarMateriaPorCodigo(self, codigo):
       
        resultado = None
        try:
            conexion = con.conexion()
            conn = conexion.open()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM materias WHERE codigo = %s"
            cursor.execute(sql, (codigo,))
            row = cursor.fetchone()
            
            if row:
                resultado = mat.Materias()
                resultado.setCodigo(row[0])
                resultado.setId(row[1])
                resultado.setAsignatura(row[2])
                resultado.setCreditos(row[3])
                resultado.setSemestre(row[4])
                resultado.setCarrera(row[5])
            
            conn.close()
        except mysql.connector.Error as err:
            raise err
        return resultado

    def buscarMateriaPorId(self, id):
        
        resultado = None
        try:
            conexion = con.conexion()
            conn = conexion.open()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM materias WHERE id = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            
            if row:
                resultado = mat.Materias()
                resultado.setCodigo(row[0])
                resultado.setId(row[1])
                resultado.setAsignatura(row[2])
                resultado.setCreditos(row[3])
                resultado.setSemestre(row[4])
                resultado.setCarrera(row[5])
            
            conn.close()
        except mysql.connector.Error as err:
            raise err
        return resultado

    def actualizarMateria(self, materia):
        
        try:
            conexion = con.conexion()
            conn = conexion.open()
            cursor = conn.cursor()
            
            sql = """
                UPDATE materias 
                SET id = %s, asignatura = %s, creditos = %s, semestre = %s, carrera = %s 
                WHERE codigo = %s
            """
            datos = (
                materia.getId(),
                materia.getAsignatura(),
                materia.getCreditos(),
                materia.getSemestre(),
                materia.getCarrera(),
                materia.getCodigo()
            )
            cursor.execute(sql, datos)
            conn.commit()
            conn.close()
            return True
        except mysql.connector.Error as err:
            raise err

    def eliminarMateria(self, codigo):
        
        try:
            conexion = con.conexion()
            conn = conexion.open()
            cursor = conn.cursor()
            
            sql = "DELETE FROM materias WHERE codigo = %s"
            cursor.execute(sql, (codigo,))
            conn.commit()
            filas_afectadas = cursor.rowcount
            conn.close()
            
            return filas_afectadas > 0
        except mysql.connector.Error as err:
            raise err

    def obtenerTodasMaterias(self):
        
        resultados = []
        try:
            conexion = con.conexion()
            conn = conexion.open()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM materias ORDER BY carrera, semestre, asignatura"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            for row in rows:
                aux = mat.Materias()
                aux.setCodigo(row[0])
                aux.setId(row[1])
                aux.setAsignatura(row[2])
                aux.setCreditos(row[3])
                aux.setSemestre(row[4])
                aux.setCarrera(row[5])
                resultados.append(aux)
            
            conn.close()
        except mysql.connector.Error as err:
            raise err
        return resultados

    def buscarPorAsignatura(self, asignatura):
        
        resultados = []
        try:
            conexion = con.conexion()
            conn = conexion.open()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM materias WHERE asignatura LIKE %s ORDER BY asignatura"
            cursor.execute(sql, (f"%{asignatura}%",))
            rows = cursor.fetchall()
            
            for row in rows:
                aux = mat.Materias()
                aux.setCodigo(row[0])
                aux.setId(row[1])
                aux.setAsignatura(row[2])
                aux.setCreditos(row[3])
                aux.setSemestre(row[4])
                aux.setCarrera(row[5])
                resultados.append(aux)
            
            conn.close()
        except mysql.connector.Error as err:
            raise err
        return resultados

    def buscarPorCarrera(self, carrera):
       
        resultados = []
        try:
            conexion = con.conexion()
            conn = conexion.open()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM materias WHERE carrera = %s ORDER BY semestre, asignatura"
            cursor.execute(sql, (carrera,))
            rows = cursor.fetchall()
            
            for row in rows:
                aux = mat.Materias()
                aux.setCodigo(row[0])
                aux.setId(row[1])
                aux.setAsignatura(row[2])
                aux.setCreditos(row[3])
                aux.setSemestre(row[4])
                aux.setCarrera(row[5])
                resultados.append(aux)
            
            conn.close()
        except mysql.connector.Error as err:
            raise err
        return resultados

    def existeMateria(self, codigo):
        """
        Verifica si existe una materia por código.
        """
        try:
            conexion = con.conexion()
            conn = conexion.open()
            cursor = conn.cursor()
            
            sql = "SELECT COUNT(*) FROM materias WHERE codigo = %s"
            cursor.execute(sql, (codigo,))
            resultado = cursor.fetchone()
            conn.close()
            
            return resultado[0] > 0
        except mysql.connector.Error as err:
            raise err