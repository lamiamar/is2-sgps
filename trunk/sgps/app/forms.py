import re
from django import forms
from django.contrib.auth.models import User
from app.models import *

"""
    Modulo de definicion de formularios utilizados en el sistema.
"""
############################ Control de Usuarios#################################
class AgregarUsuarioForm(forms.Form):
    """
        Formulario para agregar usuarios.
    """
    
    username = forms.CharField(label=u'Nombre de usuario', max_length=20)
    nombre = forms.CharField(label=u'Nombre', max_length=40)
    apellido = forms.CharField(label=u'Apellido', max_length=40)
    email = forms.EmailField(label=u'Email', required=False)
    direccion = forms.CharField(label=u'Direccion', max_length=300, required=False)
    password1 = forms.CharField(label=u'Contrasena', widget=forms.PasswordInput())
    password2 = forms.CharField(label=u'Confirmar Contrasena', widget=forms.PasswordInput())

    def clean_password2(self):
        """
            Funcion que comprueba que las contrasenhas coincidan.
        """
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Las contrasenas no coinciden, vueva a ingresar la contrasenha')

    def clean_username(self):
        """
            Funcion que verifica que se escriba un nombre valido.
        """
        
        usu = self.cleaned_data['username']
        if not re.search(r'^\w+$', usu):
            raise forms.ValidationError('El nombre de usuario solo puede contener  letras de [aA..Zz] y numeros')
        if 'username' in self.cleaned_data:
			usuarios = User.objects.all()
			usu = self.cleaned_data['username']
			for us in usuarios:
				if us.username == usu:
					raise forms.ValidationError('El nombre de Usuario no esta disponible. Inserte otro.')

        return usu
  
class ModificarUsuarioForm(forms.Form):
    """
        Formulario para modificar datos de usuario.
    """

    nombre = forms.CharField(label=u'Nombre', max_length=40)
    apellido = forms.CharField(label=u'Apellido', max_length=40)
    email = forms.EmailField(label=u'Email', required=False)
    direccion = forms.CharField(label=u'Direccion', max_length=300, required=False)

class ModificarContrasenaForm(forms.Form):
    """
        Formulario para modificar contrasenha.
    """

    username = forms.CharField(label=u'Nombre de usuario', max_length=30)
    password = forms.CharField(label=u'Contrasena', widget=forms.PasswordInput())
    passNueva = forms.CharField(label=u'Nueva Contrasena', widget=forms.PasswordInput())
    confirmacion = forms.CharField(label=u'Confirmar Contrasena', widget=forms.PasswordInput())
    

    def clean_password(self):
        """
            Funcion para verificar contrasenha valida.
        """
        if 'password' in self.cleaned_data:
            user = User.objects.get(username=self.cleaned_data['username'])
            password = self.cleaned_data['password']
            if user.check_password(password):
                return password
        raise forms.ValidationError('Su contrasenha actual no es valida')

    def clean_password2(self):
        """
            Funcion que comprueba que las contrasenhas coincidan.
        """
        if 'password1' in self.cleaned_data:
            pass1 = self.cleaned_data['passNueva']
            pass2 = self.cleaned_data['confirmacion']
            if pass1 == pass2:
                return pass2
        raise forms.ValidationError('Las contrasenas ingresadas no coinciden')
class RolSistemaForm(forms.Form):
    """
        Formulario para presentar opcion rol de sistema. 
    """

    roles = forms.ModelMultipleChoiceField(queryset=Rol.objects.filter(Tipo='S'),
                                           widget=forms.CheckboxSelectMultiple, required=False)
class RolSistemasuperForm(forms.Form):
    """
        Formulario para presentar opcion rol de sistema para el super usuario. 
    """

    roles = forms.ModelMultipleChoiceField(queryset=Rol.objects.filter(Tipo='S').exclude(Nombre= 'Aministrador del Sistema'),
                                           widget=forms.CheckboxSelectMultiple, required=False)
class AsignarRolProyectoForm(forms.Form):
    """
        Formulario para la asignacion de roles a usuarios.
    """

    roles = forms.ModelMultipleChoiceField(queryset=Rol.objects.filter(Tipo='P').exclude(Nombre= 'Lider de Proyecto'),
                                           widget=forms.CheckboxSelectMultiple, required=False)    
############################# Contro de Roles #############################

class RolForm(forms.Form):
    """
        Formulario para crear roles.
    """

    Nombre = forms.CharField(label=u'Nombre de rol', max_length=30)
    Descripcion = forms.CharField(widget=forms.Textarea(), required=False, label=u'Descripcion')
    
    def clean_Nombre(self):
       nombre = self.cleaned_data['Nombre']
       if 'Nombre' in self.cleaned_data:
            roles = Rol.objects.all()
            for rol in roles:
                if rol.Nombre == nombre:
                    raise forms.ValidationError('El nombre ya existe. Inserte otro.')

       return nombre
   
class ModificarRolForm(forms.Form):
    """
        Formulario para modificar datos de roles.
    """
    Descripcion = forms.CharField(widget=forms.Textarea(), required=False, label=u'Descripcion')

class PermisoProyectoForm(forms.Form):
    """
        Formulario para permisos de proyecto.
    """

    Permisos = forms.ModelMultipleChoiceField(queryset=Permiso.objects.filter(Tipo='P'),
                                           widget=forms.CheckboxSelectMultiple, required=False)


class PermisoSistemaForm(forms.Form):
    """
        Formulario para permisos de sistema.
    """

    Permisos = forms.ModelMultipleChoiceField(queryset=Permiso.objects.filter(Tipo='S'),
                                           widget=forms.CheckboxSelectMultiple, required=False)

#class PrivilegioForm(forms.Form):

#    Privilegios = forms.ModelMultipleChoiceField(queryset=Privilegio.objects.all(),
#                                           widget=forms.CheckboxSelectMultiple, required=False)
    
##########################################Control de proyecto#######################################
class ProyectoForm(forms.Form):
    """
        Formulario para agregar nuevo proyecto.
    """

    Nombre = forms.CharField(label=u'Nombre del Proyecto', max_length=20)
    Descripcion = forms.CharField(widget=forms.Textarea(), required=False, label=u'Descripcion')
    Usuario = forms.ModelChoiceField(queryset=User.objects.all(), label=u'Lider')
    def clean_Nombre(self):
       nombre = self.cleaned_data['Nombre']
       if 'Nombre' in self.cleaned_data:
            proyectos = Proyecto.objects.all()
            for p in proyectos:
                if p.Nombre == nombre:
                    raise forms.ValidationError('El nombre ya existe. Inserte otro.')

       return nombre
   
class ModificarProyectoForm(forms.Form):
    """
        Formulario para modificar datos de proyecto.
    """

    Descripcion = forms.CharField(widget=forms.Textarea(), required=False, label=u'Descripcion')
    Usuario = forms.ModelChoiceField(queryset=User.objects.all(), label=u'Lider')

class ProyectoEditarForm(forms.Form):
    """
        Formulario para editar descripcion de proyecto.
    """
    Descripcion = forms.CharField(widget=forms.Textarea(), required=False, label=u'Descripcion')
    
class UsuarioProyectoForm(forms.Form):
    """
        Formulario para asignar usuarios al proyecto.
    """
    usuario = forms.ModelChoiceField(queryset=User.objects.all())
    rol = forms.ModelMultipleChoiceField(queryset=Rol.objects.filter(Tipo='P').exclude(Nombre= 'Lider de Proyecto'),
                                          widget=forms.CheckboxSelectMultiple, required=False)
    
    def __init__(self, Miembros, *args, **kwargs):
        super(UsuarioProyectoForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.exclude(id__in=Miembros)
        
    

##################################CONTROL DE ARTEFACTO#################################

class ArtefactoForm(forms.Form):
    """
        Formulario para agregar nuevo artefacto.
    """

    Tipo_Artefacto = forms.ModelChoiceField(queryset=None, label='Tipo Artefacto')
    Prioridad = forms.CharField(max_length=1, widget=forms.Select(choices=PRIORIDAD), label=u'Prioridad')
    Complejidad = forms.CharField(max_length=2, widget=forms.Select(choices=COMPLEJIDAD), label=u'Complejidad')
    DescripcionCorta = forms.CharField(widget=forms.Textarea(), label='Descripcion Corta')
    DescripcionLarga = forms.CharField(widget=forms.Textarea(), required=False, label='Descripcion Larga')
     
    def __init__(self, id, fase, *args, **kwargs):
        super(ArtefactoForm, self).__init__(*args, **kwargs)
        self.fields['Tipo_Artefacto'].queryset = Tipo_Artefacto_Proyecto.objects.filter(Fase = fase, Proyecto = id)
        
class ModificarArtefactoForm(forms.Form):
    """
        Formulario para modificar datos de artefacto.
    """
    Prioridad = forms.CharField(max_length=1, widget=forms.Select(choices=PRIORIDAD), label=u'Prioridad')
    Complejidad = forms.CharField(max_length=2, widget=forms.Select(choices=COMPLEJIDAD), label=u'Complejidad')
    
    DescripcionCorta = forms.CharField(widget=forms.Textarea(), required=False, label='Descripcion Corta')
    DescripcionLarga = forms.CharField(widget=forms.Textarea(), required=False, label='Descripcion Larga')

class Tipo_ArtefactoForm(forms.Form): 
    """
        Formulario para agregar nuevo tipo de artefacto.
    """
    Nombre = forms.CharField(max_length=100, label=u'Nombre')
    Codigo = forms.CharField(max_length=10, label=u'Codigo')
    Descripcion = forms.CharField(widget=forms.Textarea(), required=False, label=u'Descripcion')
    Fase = forms.CharField(max_length=1, widget=forms.Select(choices=ETAPA), label=u'ETAPA')
    
    def clean_Codigo(self):
        """
            Funcion para validar el codigo del tipo de artefacto.
        """
        codigo = self.cleaned_data['Codigo']
        if 'Codigo' in self.cleaned_data:
            tiposArtefacto = Tipo_Artefacto.objects.all()
            for ar in tiposArtefacto:
                if ar.Codigo == codigo:
                    raise forms.ValidationError('El Codigo ya existe. Inserte otro.')

        return codigo
    
    def clean_Nombre(self):
        """
            Funcion para validar el nombre del tipo de artefacto.
        """
        nombre = self.cleaned_data['Nombre']
        if 'Nombre' in self.cleaned_data:
            tiposArtefacto = Tipo_Artefacto.objects.all()
            for ar in tiposArtefacto:
                if ar.Nombre == nombre:
                    raise forms.ValidationError('El nombre ya existe. Inserte otro.')

        return nombre
   


class Mod_Tipo_ArtefactoForm(forms.Form):
    """
        Formulario para modificar tipo de artefacto.
    """
    Fase = forms.CharField(max_length=1, widget=forms.Select(choices=ETAPA), label=u'ETAPA')
    Descripcion = forms.CharField(widget=forms.Textarea(), required=False, label=u'Descripcion')
    
class Edi_Tipo_Artefacto_ProyectoForm(forms.Form):
    """
        Formulario para editar datos (fase, descripcion) de tipo de artefacto.
    """
    Fase = forms.CharField(max_length=1, widget=forms.Select(choices=ETAPA), label=u'ETAPA')
    Descripcion = forms.CharField(widget=forms.Textarea(), required=False, label=u'Descripcion')

    
class Tipo_Artefacto_ProyectoForm(forms.Form): 
    """
        Formulario para agregar tipo de artefacto especifico de proyecto.
    """
    Nombre = forms.CharField(max_length=100, label=u'Nombre')
    Codigo = forms.CharField(max_length=10, label=u'Codigo')
    Descripcion = forms.CharField(widget=forms.Textarea(), required=False, label=u'Descripcion')
    Fase = forms.CharField(max_length=1, widget=forms.Select(choices=ETAPA), label=u'ETAPA')
    

class Edi_Tipo_Artefacto_Proyecto_ReqForm(forms.Form):
    """
        Formulario para editar tipo de artefacto especifico de requerimientos.
    """
    Fase = forms.CharField(max_length=1, widget=forms.Select(choices=ETAPA), label=u'ETAPA')
    Descripcion = forms.CharField(widget=forms.Textarea(), required=False, label=u'Descripcion')
    
    def clean_Fase(self):
        """
            Funcion que verifica si se pueden realizar los cambios.
        """
        fase1 = 'E'
        print fase1
        fase2 = self.cleaned_data['Fase']
        print fase2
        if fase1 == fase2:
            return fase1
        raise forms.ValidationError('No puede cambiar la fase, esta siendo utilizada por un Artefacto')
 
class Edi_Tipo_Artefacto_Proyecto_DisForm(forms.Form):
    """
        Formulario para editar tipo de artefacto especifico de disenho.
    """
    Fase = forms.CharField(max_length=1, widget=forms.Select(choices=ETAPA), label=u'ETAPA')
    Descripcion = forms.CharField(widget=forms.Textarea(), required=False, label=u'Descripcion')
    
    def clean_Fase(self):
        """
            Funcion que verifica si se pueden realizar los cambios.
        """
        fase1 = 'D'
        print fase1
        fase2 = self.cleaned_data['Fase']
        print fase2
        if fase1 == fase2:
            return fase1
        raise forms.ValidationError('No puede cambiar la fase, esta siendo utilizada por un Artefacto')
    
class Edi_Tipo_Artefacto_Proyecto_ImpForm(forms.Form):
    """
        Formulario para editar tipo de artefacto especifico de implementacion.
    """
    Fase = forms.CharField(max_length=1, widget=forms.Select(choices=ETAPA), label=u'ETAPA')
    Descripcion = forms.CharField(widget=forms.Textarea(), required=False, label=u'Descripcion')
    
    def clean_Fase(self):
        """
            Funcion que verifica si se pueden realizar los cambios.
        """
        fase1 = 'I'
        print fase1
        fase2 = self.cleaned_data['Fase']
        print fase2
        if fase1 == fase2:
            return fase1
        raise forms.ValidationError('No puede cambiar la fase, esta siendo utilizada por un Artefacto')    
class ArchivosAdjuntosForm(forms.Form):
    """
        Formulario para adjuntar archivos a los artefactos.
    """
    archivo = forms.FileField(label=u'Adjuntar archivo')
 
    
    
    
    
