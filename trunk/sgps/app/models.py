from django.db import models
from django.contrib.auth.models import User

TIPO_ROL = (
          ('S', 'Sistema'),
          ('P', 'Proyecto'),
          )
ESTADO = (
          ('N', 'Nuevo'),
          ('I', 'Implementando'),
          ('T', 'Terminado'),
          ('A', 'Aprobado'),
          ('D', 'Desaprobado')
          )
ETAPA = (
              ('E', 'Especificacion de Requerimientos'),
              ('D', 'Analisis y Disenho'),
              ('I', 'Implementacion'),
              )
PRIORIDAD = (
             ('B', 'Baja'),
             ('U', 'Urgente'),
             ('A', 'Alta'),
             ('M', 'Media'),
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
    user = models.ForeignKey(User, unique=True)
    direccion = models.CharField(max_length=500, blank=True)

class Proyecto(models.Model):
    Usuario = models.ForeignKey(User)
    Nombre = models.CharField(max_length=40)
    Fecha = models.DateField(auto_now_add=True)
    Descripcion = models.TextField()
    def __unicode__(self):
        return self.Nombre

class Privilegio(models.Model):
    Nombre = models.CharField(unique=True, max_length=40)
    Descripcion = models.TextField(null=True)
    def __unicode__(self):
        return u'%s' % (self.Nombre)
   
class Permiso(models.Model):
    Nombre = models.CharField(unique=True, max_length=40)
    Descripcion = models.TextField(null=True)
    Tipo = models.CharField(max_length=1, choices=TIPO_ROL)
    privilegios = models.ManyToManyField(Privilegio)
    def __unicode__(self):
        return u'%s' % (self.Nombre)

 

class Rol(models.Model):
    Nombre = models.CharField(unique=True, max_length=40)
    Descripcion = models.TextField(null=True)
    Tipo = models.CharField(max_length=1, choices=TIPO_ROL)
    permisos = models.ManyToManyField(Permiso)
    def __unicode__(self):
        return u'%s' % (self.Nombre)


class Fase(models.Model):
    Estado = models.CharField(max_length=1, choices=ESTADO)
    Etapa = models.CharField(max_length=1, choices=ETAPA)
    def __unicode__(self):
        return self.Estado

class Tipo_Artefacto(models.Model):
    Nombre = models.CharField(max_length=100)
    Fase = models.CharField(max_length=2, choices=ETAPA)
    def __unicode__(self):
        return self.Nombre

#class Numeracion(models.Model):
#    Proyecto = models.ForeignKey(Proyecto)
#    Tipo_Artefacto = models.ForeignKey(Tipo_Artefacto)
#    Ultimo_nro = models.IntegerField()
class Numeracion(models.Model):
    Proyecto = models.ForeignKey(Proyecto)
    Tipo_Artefacto = models.ForeignKey(Tipo_Artefacto)
    Ultimo_nro = models.IntegerField(null=True)

class Artefacto(models.Model):
    Nombre=models.CharField(max_length=40)
    Tipo_Artefacto = models.ForeignKey(Tipo_Artefacto)
    Proyecto = models.ForeignKey(Proyecto)
    #Fase = models.CharField(max_length=1, choices=ETAPA)
    #Fase = models.ForeignKey(Fase)
    #Numero = Numeracion()
    Prioridad = models.CharField(max_length=1)
    Complejidad = models.CharField(max_length=1, choices=COMPLEJIDAD)
    Estado = models.CharField(max_length=1, choices=ESTADO)
    Activo = models.BooleanField(default = True)
    
class RelacionArtefacto(models.Model):
 
    artefactoPadre = models.ForeignKey(Artefacto, related_name='padre')
    artefactoHijo = models.ForeignKey(Artefacto, related_name='hijo')
    Activo = models.BooleanField(default = True)

    class Meta:
        unique_together = [("artefactoPadre", "artefactoHijo")]


class UsuarioRolProyecto(models.Model):   
    usuario = models.ForeignKey(User)
    rol = models.ForeignKey(Rol, null=True)
    proyecto = models.ForeignKey(Proyecto)

    class Meta:
        unique_together = [("usuario", "rol", "proyecto")]
        
class UsuarioRolSistema(models.Model):
    usuario = models.ForeignKey(User)
    rol = models.ForeignKey(Rol)
    
    class Meta:
        unique_together = [("usuario", "rol")]
class Linea_Base(models.Model):
    Proyecto = models.ForeignKey(Proyecto)
    Fase = models.CharField(max_length=2, choices=ETAPA)

class Detalle_Linea_Base(models.Model):
    Linea_Base = models.ForeignKey(Linea_Base)
    Artefacto = models.ManyToManyField(Artefacto)

  #  def AutoNum(self):
  #     self.Numero.Proyecto = self.Proyecto
  #      self.Numero.Tipo_Artefacto = self.Tipo_Artefacto
  #      self.Numero.Ultimo_nro = self.Numero.Ultimo_nro + 1

class ArchivosAdjuntos(models.Model):
    Artefacto = models.ForeignKey(Artefacto)
    Nom_Archivo = models.CharField(max_length=50)
    Contenido = models.TextField()
    Tamano = models.IntegerField()
    TipoContenido = models.TextField()
    Activo = models.BooleanField(default = True)

    class Meta:
        db_table = 'ArchivosAdjuntos'

class Historial(models.Model):
    Artefacto = models.ForeignKey(Artefacto)
    Version = models.IntegerField()
    Usuario = models.ForeignKey(User)
    Fecha_modificado = models.DateField()
    Descripcion = models.TextField()