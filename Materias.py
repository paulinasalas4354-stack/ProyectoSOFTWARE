class Materias:
    def __init__(self, codigo=None, id=None, asignatura="", creditos=0, semestre=0, carrera=""):
        self.codigo = codigo
        self.id = id
        self.asignatura = asignatura
        self.creditos = creditos
        self.semestre = semestre
        self.carrera = carrera

    def getCodigo(self):
        return self.codigo
    
    def getId(self):
        return self.id
    
    def getAsignatura(self):
        return self.asignatura
    
    def getCreditos(self):
        return self.creditos
    
    def getSemestre(self):
        return self.semestre
    
    def getCarrera(self):
        return self.carrera

    def setCodigo(self, codigo):
        self.codigo = codigo
    
    def setId(self, id):
        self.id = id

    def setAsignatura(self, asignatura):
        self.asignatura = asignatura

    def setCreditos(self, creditos):
        self.creditos = creditos

    def setSemestre(self, semestre):
        self.semestre = semestre

    def setCarrera(self, carrera):
        self.carrera = carrera    