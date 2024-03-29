from django.db import models
from django.contrib.auth.models import User

"""
    Modulo que define los modelos de los objetos utilizados en el sistema.
"""

TIPO_ROL = (
          ('S', 'Sistema'),
          ('P', 'Proyecto'),
          )


ESTADO = (
          ('I', 'Implementando'),
          ('A', 'Aprobado'),
          )
ETAPA = (
              ('E', 'Especificacion de Requerimientos'),
              ('D', 'Analisis y Disenho'),
              ('I', 'Implementacion'),
              )
PRIORIDAD = (
             ('B', 'Baja'),
             ('M', 'Media'),
             ('A', 'Alta'),
             ('U', 'Urgente'),
             
             
             )
COMPLEJIDAD = (
                      ('1', '1'),
                      ('2', '2'),
                      ('3', '3'),
                      ('4', '4'),
                      ('5', '5'),
                      ('6', '6'),
                      ('7', '7'),
                      ('8', '8'),
                      ('9', '9'),
                      ('10', '10'),
             )    


class ProfileUsuario(models.Model):
    """
        Modelo para registrar datos de usuario.
    """
    user = models.ForeignKey(User, unique=True)
    direccion = models.CharField(max_length=500, blank=True)

class Proyecto(models.Model):
    """
        Modelo para registrar datos de proyecto.
    """
    Usuario = models.ForeignKey(User)
    Nombre = models.CharField(max_length=40)
    Fecha = models.DateField(auto_now_add=True)
    Descripcion = models.TextField()
    def __unicode__(self):
        return self.Nombre
   
class Permiso(models.Model):
    """
        Modelo para registrar datos de permiso.
    """
    Nombre = models.CharField(unique=True, max_length=40)
    Descripcion = models.TextField(null=True)
    Tipo = models.CharField(max_length=1, choices=TIPO_ROL)

    def __unicode__(self):
        return u'%s' % (self.Nombre)

class Rol(models.Model):
    """
        Modelo para registrar datos de rol.
    """
    Nombre = models.CharField(unique=True, max_length=40)
    Descripcion = models.TextField(null=True)
    Tipo = models.CharField(max_length=1, choices=TIPO_ROL)
    permisos = models.ManyToManyField(Permiso)
    def __unicode__(self):
        return u'%s' % (self.Nombre)


class Fase(models.Model):
    """
        Modelo para registrar datos de fase.
    """
    Estado = models.CharField(max_length=1, choices=ESTADO)
    Etapa = models.CharField(max_length=1, choices=ETAPA)
    def __unicode__(self):
        return self.Estado

class Tipo_Artefacto(models.Model):
    """
        Modelo para registrar datos de tipo de artefacto.
    """
    Nombre = models.CharField(max_length=100)
    Codigo=models.CharField(max_length=10)
    Fase = models.CharField(max_length=2, choices=ETAPA)
    Descripcion = models.TextField(null=True)
    
    def __unicode__(self):
        return self.Nombre
    
class Tipo_Artefacto_Proyecto(models.Model):
    """
        Modelo para registrar tipo de artefacto especifico.
    """
    Nombre = models.CharField(max_length=100)
    Codigo=models.CharField(max_length=10)
    Descripcion = models.TextField(null=True) 
    Fase = models.CharField(max_length=1, choices=ETAPA)
    TipoArtefactoGeneral = models.ForeignKey(Tipo_Artefacto, null=True)
    Proyecto = models.ForeignKey(Proyecto)
    

    def __unicode__(self):
        return self.Nombre

class Numeracion(models.Model):
    """
        Modelo para registrar la numeracion de artefactos por su tipo.
    """
    Proyecto = models.ForeignKey(Proyecto)
    Tipo_Artefacto = models.ForeignKey(Tipo_Artefacto_Proyecto)
    Ultimo_nro = models.IntegerField(null=True)

class Artefacto(models.Model):
    """
        Modelo para registrar datos de artefacto.
    """
    Nombre=models.CharField(max_length=40)
    Tipo_Artefacto = models.ForeignKey(Tipo_Artefacto_Proyecto)
    DescripcionCorta = models.CharField(max_length=650)
    DescripcionLarga = models.TextField(null=True)
    Proyecto = models.ForeignKey(Proyecto)
    Prioridad = models.CharField(max_length=1)
    Version = models.IntegerField()
    Complejidad = models.CharField(max_length=2, choices=COMPLEJIDAD)
    Usuario = models.ForeignKey(User)
    Estado = models.CharField(max_length=1, choices=ESTADO)
    Activo = models.BooleanField(default = True)
    
class RelacionArtefacto(models.Model):
    """
        Modelo para registrar las relaciones de los artefactos.
    """
 
    artefactoPadre = models.ForeignKey(Artefacto, related_name='padre')
    artefactoHijo = models.ForeignKey(Artefacto, related_name='hijo')
    Activo = models.BooleanField(default = True)

    class Meta:
        unique_together = [("artefactoPadre", "artefactoHijo")]


class UsuarioRolProyecto(models.Model):
    """
        Modelo para registrar los usuarios con roles de proyecto.
    """  
    usuario = models.ForeignKey(User)
    rol = models.ForeignKey(Rol, null=True)
    proyecto = models.ForeignKey(Proyecto)

    class Meta:
        unique_together = [("usuario", "rol", "proyecto")]
        
class UsuarioRolSistema(models.Model):
    """
        Modelo para registrar usuarios con roles de sistema.
    """
    usuario = models.ForeignKey(User)
    rol = models.ForeignKey(Rol)
    
    class Meta:
        unique_together = [("usuario", "rol")]
        
class Linea_Base(models.Model):
    """
        Modelo para registrar la linea base.
    """
    Proyecto = models.ForeignKey(Proyecto)
    Fase = models.CharField(max_length=2, choices=ETAPA)

class Detalle_Linea_Base(models.Model):
    """
        Modelo para registrar el detalle de la linea base.
    """
    Linea_Base = models.ForeignKey(Linea_Base)
    Artefacto = models.ManyToManyField(Artefacto)

  #  def AutoNum(self):
  #     self.Numero.Proyecto = self.Proyecto
  #      self.Numero.Tipo_Artefacto = self.Tipo_Artefacto
  #      self.Numero.Ultimo_nro = self.Numero.Ultimo_nro + 1

class ArchivosAdjuntos(models.Model):
    """
        Modelo para registra datos de archivo.
    """
    Artefacto = models.ForeignKey(Artefacto)
    Nom_Archivo = models.CharField(max_length=50)
    Contenido = models.TextField()
    Tamano = models.IntegerField()
    TipoContenido = models.TextField()
    Activo = models.BooleanField(default = True)

    class Meta:
        db_table = 'ArchivosAdjuntos'

class HistorialArt(models.Model):
    """
        Modelo para registrar datos del historial de artefactos.
    """
    Artefacto = models.ForeignKey(Artefacto)
    Nombre=models.CharField(max_length=40)
    Tipo_Artefacto = models.ForeignKey(Tipo_Artefacto_Proyecto)
    DescripcionCorta = models.CharField(max_length=650, null=True)
    DescripcionLarga = models.TextField(null=True)
    Proyecto = models.ForeignKey(Proyecto)
    Prioridad = models.CharField(max_length=1)
    Version = models.IntegerField()
    Complejidad = models.CharField(max_length=2, choices=COMPLEJIDAD)
    Usuario = models.ForeignKey(User)
    Estado = models.CharField(max_length=1, choices=ESTADO)
    Activo = models.BooleanField(default = True)
    Fecha_mod = models.DateTimeField(auto_now =False, auto_now_add=True, editable=False)
    
    class Meta:
        unique_together = [("Artefacto", "Version")]
    
class HistorialRel(models.Model):
    """
        Modelo para registrar datos en el historial de relaciones.
    """
    #artefactoPadre = models.ForeignKey(Artefacto, related_name='artPadre')
    artefactoHijo = models.ForeignKey(HistorialArt)
    artefactoPadre = models.ForeignKey(Artefacto)
    padreVersion = models.IntegerField()
    hijoVersion = models.IntegerField()
    Fecha_mod = models.DateTimeField(auto_now =False, auto_now_add=True, editable=False)
    class Meta:
        unique_together = [("artefactoPadre", "artefactoHijo")]   
    
class HistorialAdj(models.Model):
    """
        Modelo para registrar datos en el historial de archivos.
    """
    Artefacto = models.ForeignKey(HistorialArt)
    Archivo = models.ForeignKey(ArchivosAdjuntos)
    Fecha_mod = models.DateTimeField(auto_now =False, auto_now_add=True, editable=False)
    class Meta:
        unique_together = [("Artefacto", "Archivo")]