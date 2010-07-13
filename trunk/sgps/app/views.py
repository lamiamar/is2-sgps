import base64
import datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import Context
from django.contrib.auth import logout
from django.template import RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from sgps.app.models import *
from sgps.app.forms import *

#################### funciones auxiliares para historial ###########################

def registrarHistorialArt(artefacto):
    registroHistorial = HistorialArt(                                     
                                     Artefacto = artefacto,
                                     Nombre = artefacto.Nombre,
                                     Tipo_Artefacto = artefacto.Tipo_Artefacto,
                                     DescripcionCorta = artefacto.DescripcionCorta,
                                     DescripcionLarga = artefacto.DescripcionLarga,
                                     Proyecto = artefacto.Proyecto,
                                     Prioridad = artefacto.Prioridad,
                                     Version = artefacto.Version,
                                     Complejidad = artefacto.Complejidad,
                                     Usuario = artefacto.Usuario,
                                     Estado = artefacto.Estado,
                                     Activo = artefacto.Activo,
                                     Actual = True,
                                     Fecha_mod = datetime.date.today(),
                                     )
    
    registroHistorial.save(force_insert=True)
    
    files = ArchivosAdjuntos.objects.filter(Artefacto=artefacto, Activo=True)
    for archivo in files:
        historialAdj = HistorialAdj(
                                        Artefacto = registroHistorial,
                                        Archivo = archivo,
                                        )
        historialAdj.save()
    
def registrarHistorialRel(relacion_artefacto):
    historialRelaciones = HistorialRel(
                                      artefactoPadre=relacion_artefacto.artefactoPadre,
                                      padreVersion=relacion_artefacto.artefactoPadre.Version, 
                                      artefactoHijo=relacion_artefacto.artefactoHijo,
                                      Activo = relacion_artefacto.Activo,
                                      Fecha_mod = datetime.date.today(),
                                      )
    historialRelaciones.save()

###################################### SISTEMA ##################################################

@login_required
def pagina_principal(request):
    user = User.objects.get(username=request.user.username)
    usrolpros= UsuarioRolProyecto.objects.filter(usuario = user).values_list('proyecto', flat=True).distinct()
    proyectoUser=Proyecto.objects.filter(id__in=usrolpros).order_by('Nombre')
    usrolsis= UsuarioRolSistema.objects.filter(usuario = user)
    Usuarios = False
    Proyectos = False
    Roles = False
    Tipo_Artefactos = False
    for urs in usrolsis:
        permi = urs.rol.permisos.all()
        for per in permi:
            if per.Nombre =='CrearProyectos' or per.Nombre =='EditarProyectos' or per.Nombre == 'EliminarProyectos' or per.Nombre == 'VerProyectos':
                Proyectos = True
            if per.Nombre =='CrearUsuarios' or per.Nombre =='EditarUsuarios' or per.Nombre == 'EliminarUsuarios' or per.Nombre == 'AsignarRolSistema' or per.Nombre == 'VerUsuarios':
                Usuarios = True
            if per.Nombre =='CrearRoles' or per.Nombre =='EditarRoles' or per.Nombre == 'EliminarRoles' or per.Nombre == 'ConfigurarPermisos' or per.Nombre == 'VerRoles':
                Roles = True              
            if per.Nombre =='CrearTipoDeArtefacto' or per.Nombre =='EditarTipoDeArtefacto' or per.Nombre == 'EliminarTipoDeArtefacto' or per.Nombre == 'VerArtefactos':
                Tipo_Artefactos = True
    contexto = RequestContext(request, {
                'proyectoUser': proyectoUser,
                'usrolpros': usrolpros,
                'Usuarios':Usuarios, 
                'Proyectos':Proyectos,
                'Roles':Roles,
                'Tipo_Artefactos':Tipo_Artefactos,
                })
    return render_to_response('pagina_principal.html', contexto)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

#############################Control de usuario###########################

@login_required
def administrar_usuarios(request):
    user = User.objects.get(username=request.user.username)
    usuarios = User.objects.all().order_by('username')
    usrolsis= UsuarioRolSistema.objects.filter(usuario = user)
    CrearUsuarios = None
    EditarUsuarios = None
    EliminarUsuarios = None
    asignarrol= None
    for urs in usrolsis:
        CrearUsuarios = urs.rol.permisos.filter(Nombre = 'CrearUsuarios')
        EditarUsuarios = urs.rol.permisos.filter(Nombre = 'EditarUsuarios')
        EliminarUsuarios = urs.rol.permisos.filter(Nombre = 'EliminarUsuarios')
        asignarrol = urs.rol.permisos.filter(Nombre = 'AsignarRolSistema')
    return render_to_response('admin/Usuario/administrar_usuarios.html',{'user': user, 'usuarios': usuarios,'EditarUsuarios':EditarUsuarios,'EliminarUsuarios':EliminarUsuarios,'CrearUsuarios':CrearUsuarios,'asignarrol':asignarrol})


@login_required
def agregarUsuario(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = AgregarUsuarioForm(request.POST)
        if form.is_valid():
            usuarionuevo = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            usuarionuevo.first_name=form.cleaned_data['nombre']
            usuarionuevo.last_name=form.cleaned_data['apellido']
            UsuarioNuevo = ProfileUsuario(user=usuarionuevo,
                                      direccion=form.cleaned_data['direccion'],
                                      )
            usuarionuevo.save()
            UsuarioNuevo.save()
            return HttpResponseRedirect('/administracion/usuarios/')
    else:
        form = AgregarUsuarioForm()
    return render_to_response('admin/Usuario/registrar_usuario.html', {'user': user,'form': form })



@login_required
def editarUsuario(request, id_user):
    user = User.objects.get(username=request.user.username)
    usuario = get_object_or_404(User, id=id_user)    
    if request.method == 'POST':
        form = ModificarUsuarioForm(request.POST)
        if form.is_valid():
            Usuario= usuario.get_profile()
            usuario.first_name=form.cleaned_data['nombre']
            usuario.last_name=form.cleaned_data['apellido']
            usuario.email=form.cleaned_data['email']
            Usuario.direccion=form.cleaned_data['direccion']
            usuario.save()
            Usuario.save()
            
            return HttpResponseRedirect('/administracion/usuarios/')
    else:
        form = ModificarUsuarioForm({'nombre': usuario.first_name, 'apellido': usuario.last_name,'direccion': usuario.get_profile().direccion, 'email': usuario.email, })
    return render_to_response('admin/Usuario/editarUsuario.html', {'user': user,'form': form, 'usuario': usuario,})




@login_required
def ModificarContrasena(request, id_user):
    user = User.objects.get(username=request.user.username)
    usuario = get_object_or_404(User, pk=id_user)
    if request.method == 'POST':
        form = ModificarContrasenaForm(request.POST)
        if form.is_valid():
            usuario.set_password(form.cleaned_data['passNueva'])
            usuario.save()
            return HttpResponseRedirect('/administracion/usuarios/')
    else:
        form = ModificarContrasenaForm()
    return render_to_response('admin/Usuario/cambiarContrasena.html', {'user': user,'form': form, 'usuario': usuario,})

@login_required
def eliminarUsuario(request, id_user):
    user = User.objects.get(username=request.user.username)
    usuario = User.objects.get(pk=id_user)
    proyectos = Proyecto.objects.all()
    usuarioprohibido = False
    mensaje=None
    for proyecto in proyectos:
        if proyecto.Usuario.username == usuario.username:
            mensaje="Este usuaruo es lider de algun Proyecto, no se puede eliminar"
    if usuario.id == 1:
        mensaje= "Este usuario es el Administrador del sistema no se puede Eliminar"
    if request.method == 'POST':
        usuario.delete()
        return HttpResponseRedirect('/administracion/usuarios/')
    return render_to_response('admin/Usuario/eliminarUsuario.html', {'user': user,'usuario': usuario,'usuarioprohibido': usuarioprohibido, 'mensaje': mensaje,})

@login_required
def asignarRolesSistema(request, usuario_id):
    
    user = User.objects.get(username=request.user.username)
    usuario = get_object_or_404(User, id=usuario_id)
    rol = Rol.objects.get(Nombre = 'Aministrador del Sistema')
#    if user.id == 1:
#        rolesUsuario = UsuarioRolSistema.objects.filter(usuario = usuario).exclude(rol=rol)
#    else:
#        rolesUsuario = UsuarioRolSistema.objects.filter(usuario = usuario)
    rolesUsuario = UsuarioRolSistema.objects.filter(usuario = usuario)
    if request.method == 'POST':
#        if user.id == 1:
#            form = RolSistemasuperForm(request.POST)
#        else:
#            form = RolSistemaForm(request.POST)
        form = RolSistemaForm(request.POST)
        if form.is_valid():
            seleccionado = form.cleaned_data['roles']
            for rol in rolesUsuario:
                rol.delete()
            for rol in seleccionado:
                
                userRolSistema = UsuarioRolSistema(
                usuario=usuario,
                rol=rol,
                )
                userRolSistema.save()
                
            return HttpResponseRedirect('/administracion/usuarios/')
    else:
        dict = {}
        for usuarioRol in rolesUsuario:
            dict[usuarioRol.rol.id] = True
#        if user.id == 1:
#            form = RolSistemasuperForm(initial={'roles': dict})
#        else:
#            form = RolSistemaForm(initial={'roles': dict})
        form = RolSistemaForm(initial={'roles': dict})
    return render_to_response("admin/Usuario/asignarRolesSistema.html", {'form':form, 'usuario':usuario, 'user':user})




##################################### Control de Proyecto ###################################


@login_required
def administrar_proyectos(request):
    proyectos = Proyecto.objects.all().order_by('Nombre')
    user = User.objects.get(username=request.user.username)
    usrolsis= UsuarioRolSistema.objects.filter(usuario = user)
    for urs in usrolsis:
        CrearProyectos = urs.rol.permisos.filter(Nombre = 'CrearProyectos')
        EditarProyectos = urs.rol.permisos.filter(Nombre = 'EditarProyectos')
        EliminarProyectos = urs.rol.permisos.filter(Nombre = 'EliminarProyectos')
        asignarrol = urs.rol.permisos.filter(Nombre = 'AsignarRolSistema')
    return render_to_response('admin/Proyecto/administrarProyectos.html', {'user': user, 'proyectos': proyectos,'EditarProyectos':EditarProyectos,'EliminarProyectos':EliminarProyectos,'CrearProyectos':CrearProyectos,})

@login_required
def nuevo_proyecto(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = Proyecto(Nombre=form.cleaned_data["Nombre"],
                                Usuario=form.cleaned_data["Usuario"],
                                Descripcion=form.cleaned_data["Descripcion"],
                                )
            proyecto.save()
            rol = Rol.objects.get(Nombre = 'Lider de Proyecto')
            URP = UsuarioRolProyecto.objects.filter(usuario= proyecto.Usuario, proyecto = proyecto, rol = rol )
            if not URP:
                UserRolPro = UsuarioRolProyecto(usuario=proyecto.Usuario,
                             proyecto=proyecto,
                             rol=rol,
                                )
                UserRolPro.save()
            TAP = Tipo_Artefacto.objects.all()
            for tap in TAP:
                ap = Tipo_Artefacto_Proyecto(Nombre=tap.Nombre,
                                             Fase=tap.Fase,
                                             Descripcion=tap.Descripcion,
                                             TipoArtefactoGeneral=tap,
                                             Proyecto=proyecto,
                                             )
                ap.save()
            return HttpResponseRedirect('/administracion/proyectos/')
    else:
        form = ProyectoForm()
    return render_to_response('admin/Proyecto/CrearProyecto.html', {'user': user,'form': form,})


def modificarProyecto(request, id):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        proyecto = Proyecto.objects.get(id=id)
        form = ModificarProyectoForm(request.POST)
        if form.is_valid():
            proyecto.Usuario=form.cleaned_data['Usuario']
            proyecto.Descripcion=form.cleaned_data['Descripcion']
            proyecto.save()
            rol = Rol.objects.get(Nombre = 'Lider de Proyecto')
            urp = UsuarioRolProyecto.objects.filter(proyecto = proyecto, rol = rol )
            if urp:
                usropr =  UsuarioRolProyecto.objects.get(proyecto = proyecto, rol = rol )
                usropr.rol = None
                usropr.save()
            URP = UsuarioRolProyecto.objects.filter(usuario= proyecto.Usuario, proyecto = proyecto, rol = None )
            if not URP:
                UserRolPro = UsuarioRolProyecto(usuario=proyecto.Usuario,
                             proyecto=proyecto,
                             rol=rol,
                                )
                UserRolPro.save()
            else:
                usropr =  UsuarioRolProyecto.objects.get(usuario= proyecto.Usuario, proyecto = proyecto, rol = None )
                usropr.rol = rol
                usropr.save()
            return HttpResponseRedirect('/administracion/proyectos/')
    else:
        
        #id = request.GET['id']
        proyecto = get_object_or_404(Proyecto, id=id)
        form = ModificarProyectoForm(initial={'Nombre': proyecto.Nombre,
                             'Usuario': proyecto.Usuario.id, 'Descripcion': proyecto.Descripcion,})
    return render_to_response('admin/Proyecto/editarProyecto.html', {'user': user, 'form': form, 'proyecto': proyecto,})

def editar_proyecto(request, id):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        proyecto = Proyecto.objects.get(id=id)
        form = ProyectoEditarForm(request.POST)
        if form.is_valid():
            proyecto.Descripcion=form.cleaned_data['Descripcion']
            proyecto.save()
        return HttpResponseRedirect('/proyectos/' + str (id))
    else:
        
        #id = request.GET['id']
        proyecto = get_object_or_404(Proyecto, id=id)
        form = ProyectoEditarForm(initial={'Descripcion': proyecto.Descripcion,})
    return render_to_response('proyec/editar_proyecto.html', {'user': user,'form': form, 'proyecto': proyecto,})

@login_required
def eliminar_proyecto(request, id):
    user = User.objects.get(username=request.user.username)
    proyecto = get_object_or_404(Proyecto, id=id)
    if request.method == 'POST':
        
        proyecto.delete()
        return HttpResponseRedirect('/administracion/proyectos/')
    return render_to_response('admin/Proyecto/eliminarProyecto.html', {'user': user, 'proyecto': proyecto,})

@login_required
def proyecto(request, id):
    
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=id)
    roles = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=proyecto).values_list('rol',flat=True)
    usrolpro= UsuarioRolProyecto.objects.filter(usuario = user, proyecto = proyecto).exclude(rol = None)
    Requerimientos = False
    Diseno = False
    Implementacion = False
    EditarProyecto = False
    AgregarMiembro = False
    GenerarLineaBase = False
    TipoArtefactoEspecifico = False
    for urp in usrolpro:
        permi = urp.rol.permisos.all()
        for per in permi:
            if per.Nombre =='CrearArtefactoReq' or per.Nombre =='EditarArtefactoReq' or per.Nombre == 'EliminarArtefactoReq' or per.Nombre == 'ConfigurarRelaciones' or per.Nombre == 'CalcularImpacto' or per.Nombre == 'VerArtefactosEspecificos' or per.Nombre == 'AprobarArtefacto':
                Requerimientos = True
            if per.Nombre =='CrearArtefactoDis' or per.Nombre =='EditarArtefactoDis' or per.Nombre == 'EliminarArtefactoDis' or per.Nombre == 'ConfigurarRelaciones' or per.Nombre == 'CalcularImpacto' or per.Nombre == 'VerArtefactosEspecificos' or per.Nombre == 'AprobarArtefacto':
                Diseno = True
            if per.Nombre =='CrearArtefactoImp' or per.Nombre =='EditarArtefactoImp' or per.Nombre == 'EliminarArtefactoImp' or per.Nombre == 'ConfigurarRelaciones' or per.Nombre == 'CalcularImpacto' or per.Nombre == 'VerArtefactosEspecificos' or per.Nombre == 'AprobarArtefacto':
                Implementacion = True              
            if per.Nombre =='EditarProyecto':
                EditarProyecto = True
            if per.Nombre =='CrearMiembro' or per.Nombre =='EditarMiembro' or per.Nombre =='EliminarMiembro':
                AgregarMiembro = True
            print AgregarMiembro
            if per.Nombre =='CrearTipoArtefactoEspecifico' or per.Nombre =='EditarTipoArtefactoEspecifico' or per.Nombre =='EliminarTipoArtefactoEspecifico':
                TipoArtefactoEspecifico = True
            if per.Nombre =='GenerarLineaBase':
                GenerarLineaBase = True
        
    return render_to_response('proyec/proyecto.html', {'user': user, 'proyecto': proyecto,'Requerimientos':Requerimientos, 'Diseno':Diseno,'Implementacion':Implementacion,'EditarProyecto':EditarProyecto,'AgregarMiembro':AgregarMiembro,'GenerarLineaBase':GenerarLineaBase,'TipoArtefactoEspecifico':TipoArtefactoEspecifico})

@login_required
def usuariosMiembros(request, id):
    user = User.objects.get(username=request.user.username)
    usuario = user
    proyecto = Proyecto.objects.get(pk = id)
    UsRoPo = UsuarioRolProyecto.objects.filter(proyecto = proyecto)
    miembros = []
    for users in UsRoPo:
        if not users.usuario in miembros:
            miembros.append(users.usuario)
    usrolpro= UsuarioRolProyecto.objects.filter(usuario = usuario).exclude(rol = None)
    for urp in usrolpro:
        CrearMiembro = urp.rol.permisos.filter(Nombre = 'CrearMiembro')
        EditarMiembro= urp.rol.permisos.filter(Nombre = 'EditarMiembro')
        EliminarMiembro = urp.rol.permisos.filter(Nombre = 'EliminarMiembro')
    return render_to_response('admin/Proyecto/administrarMiembros.html',{'user':user, 'proyecto':Proyecto.objects.get(id=id), 'miembros': miembros,'EditarMiembro':EditarMiembro, 'EliminarMiembro':EliminarMiembro, 'CrearMiembro':CrearMiembro,})

@login_required
def agregar_miembros(request, id):
    user = User.objects.get(username=request.user.username)
    proyec= Proyecto.objects.get(id=id)
    miembros=UsuarioRolProyecto.objects.filter(proyecto=proyec)
    Miembros= []
    for m in miembros:
        Miembros.append(m.usuario.id)
    if request.method == 'POST':
        form = UsuarioProyectoForm(Miembros, request.POST)
        if form.is_valid():
            rolesMiembros = form.cleaned_data['rol']
            if  rolesMiembros:
                for rol in rolesMiembros:
                    miembrosRol = UsuarioRolProyecto()
                    miembrosRol.usuario = form.cleaned_data['usuario']
                    miembrosRol.proyecto = Proyecto.objects.get(pk = id)
                    miembrosRol.rol = rol
                    miembrosRol.save()                
                
            else:
                miembrosRol = UsuarioRolProyecto()
                miembrosRol.usuario = form.cleaned_data['usuario']
                miembrosRol.rol = None
                miembrosRol.proyecto = Proyecto.objects.get(pk = id)
                miembrosRol.save()
                
            return HttpResponseRedirect("/proyecto/" + str(id) + "/usuarios_miembros/")
    else:
       
        form = UsuarioProyectoForm(Miembros)
    return render_to_response('admin/Proyecto/agregarMiembro.html', {'form':form, 'user':user,  'proyecto':Proyecto.objects.get(pk=id)})

@login_required
def asignarRolProyecto(request, id, id_us):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk = id)
    usuario = User.objects.get(pk = id_us)
    form = AsignarRolProyectoForm()
    rol = Rol.objects.get(Nombre= 'Lider de Proyecto')
    URP= UsuarioRolProyecto.objects.filter(proyecto = proyecto, usuario = usuario).exclude(rol = rol)
    if request.method == 'POST':
        form = AsignarRolProyectoForm(request.POST)
        if form.is_valid():
            for urp in URP:
                urp.delete()
            URP2 = form.cleaned_data['roles']
            if URP2:
                for urp in URP2:
                    UserRolPro = UsuarioRolProyecto(usuario=usuario,
                                 proyecto=proyecto,
                                 rol=urp,
                                )
                    UserRolPro.save()
            else:
                UserRolPro = UsuarioRolProyecto(usuario=usuario,
                             proyecto=proyecto,
                             rol=None,
                                )
                UserRolPro.save()

            return HttpResponseRedirect("/proyecto/" + str(id) + "/usuarios_miembros/" )
    else:
        if len(URP) == 1 and not URP[0].rol:
            form = AsignarRolProyectoForm()
        else:
            dict = {}
            for urp in URP:
                dict[urp.rol.id] = True
                form = AsignarRolProyectoForm(initial = {'roles':dict})
    return render_to_response("proyec/asignarRolProyecto.html", {'user': user, 'form':form, 'usuario':usuario, 'proyecto': proyecto})


@login_required
def removerMiembro(request, id, id_us):
    user = User.objects.get(username=request.user.username)
    usuario = get_object_or_404(User, pk=id_us)
    proyecto = get_object_or_404(Proyecto, pk=id)
    usuarioprohibido = False
    if proyecto.Usuario.username == usuario.username:
        usuarioprohibido = True
    if request.method == 'POST':
        URP= UsuarioRolProyecto.objects.filter(proyecto = proyecto, usuario = usuario)
        for urp in URP:
            urp.delete()
        return HttpResponseRedirect("/proyecto/" + str(id) + "/usuarios_miembros/")
    else:
        return render_to_response("proyec/remover_miembro.html", {'usuario':usuario, 'proyecto':proyecto, 'user':user,'usuarioprohibido': usuarioprohibido,})

######################################## Control de Rol ##############################

@login_required
def administrar_roles(request):


    roles = Rol.objects.all().order_by('Tipo')
    contexto= RequestContext(request, {
                'roles': roles,
                })
    return render_to_response('admin/Roles/administrar_roles.html', contexto)

@login_required
def administrar_rolesTipo(request, Tipo):
    user = User.objects.get(username=request.user.username)
    roles = Rol.objects.filter(Tipo= Tipo).order_by('Nombre')
    usrolsis= UsuarioRolSistema.objects.filter(usuario = user)
    for urs in usrolsis:
        CrearRoles = urs.rol.permisos.filter(Nombre = 'CrearRoles')
        EditarRoles = urs.rol.permisos.filter(Nombre = 'EditarRoles')
        EliminarRoles = urs.rol.permisos.filter(Nombre = 'EliminarRoles')
        configpermisos = urs.rol.permisos.filter(Nombre = 'ConfigurarPermisos')
    contexto= RequestContext(request, {
                'roles': roles,
                'Tipo': Tipo,
                'EditarRoles':EditarRoles,
                'EliminarRoles':EliminarRoles,
                'CrearRoles':CrearRoles,
                'configpermisos':configpermisos,
                })
    return render_to_response('admin/Roles/Listar_roles.html', contexto)


@login_required
def crearRoles(request, Tipo):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            nuevoRol = Rol(
                      Nombre = form.cleaned_data['Nombre'],
                      Descripcion = form.cleaned_data['Descripcion'],
                      Tipo = Tipo
            )
            nuevoRol.save()
            return HttpResponseRedirect('/administracion/roles/' + Tipo + '/')
    else:
        form = RolForm()
    return render_to_response('admin/Roles/crearRol.html', {'form': form, 'Tipo': Tipo})

@login_required
def modificarRol(request, id, Tipo):
    
    if request.method == 'POST':
        rol = Rol.objects.get(id=id)
        
        form = ModificarRolForm(request.POST)
        if form.is_valid():
            rol.Descripcion=form.cleaned_data['Descripcion']
            rol.save()
            
            return HttpResponseRedirect('/administracion/roles/' + Tipo + '/')
    else:
        #id = request.GET['id']
        rol = get_object_or_404(Rol, id=id)
        form = ModificarRolForm({'Descripcion': rol.Descripcion,})

    return render_to_response('admin/Roles/EditarRol.html', {'form': form, 'rol': rol,'Tipo': Tipo,})
@login_required
def eliminarRoles(request, id, Tipo):

    rol = Rol.objects.get(id=id)
    rolprohibido = False
    if rol.Nombre == 'Lider de Proyecto' or rol.Nombre == 'Aministrador del Sistema':
        rolprohibido = True 
    if request.method == 'POST':
        rol.delete()
        return HttpResponseRedirect('/administracion/roles/' + Tipo +'/')
    return render_to_response('admin/Roles/eliminarRoles.html', {'rol': rol,'Tipo': Tipo,'rolprohibido':rolprohibido})
###########################CONTROL DE PERMISO##############################
@login_required
def GestionarPermisos(request,id,Tipo):
    rol = get_object_or_404(Rol, pk= id)
    permisos = rol.permisos.all().order_by('Nombre')
    contexto= RequestContext(request, {
                'permisos' : permisos,
                'Tipo': Tipo,
                'rol': rol,
                })
    return render_to_response('admin/Permisos/GestionPermisos.html', contexto)


@login_required
def agregar_permisos(request,id):
    rol = Rol.objects.get(id=id)
    if request.method == 'POST':
        
        if rol.Tipo == 'S':
            form = PermisoSistemaForm(request.POST)
        if rol.Tipo == 'P':
            form = PermisoProyectoForm(request.POST)
        if form.is_valid():
            rol.permisos.clear()
            permisos=form.cleaned_data['Permisos']
            for permiso in permisos:
                rol.permisos.add(permiso)
            rol.save()
            return HttpResponseRedirect('/administracion/roles/permisos/' + str(id) +'/' + rol.Tipo + '/')
    else:
        dict = {}
        listapermiso=rol.permisos.filter(Tipo=rol.Tipo)
        for permiso in listapermiso:
            dict[permiso.id] = True
        if rol.Tipo == 'S':
            form = PermisoSistemaForm({'Permisos': dict})
        if rol.Tipo == 'P':
            form = PermisoProyectoForm({'Permisos': dict})
    contexto = RequestContext(request, {'form': form,
                                         'rol': rol,
                                         })
    return render_to_response('admin/Permisos/agregar_permisos.html', contexto)



##########################CONTROL DE PRIVILEGIOS###########################

#@login_required
#def GestionarPrivilegios(request,id,per_id):
#    rol = Rol.objects.get(id=id)
#    permiso = Permiso.objects.get(id=per_id)
#    rolpe = rol.permisos.filter(id = permiso.id)
#    if request.method == 'POST':
#        form = PrivilegioForm(request.POST)
#        if form.is_valid():
#            permiso.privilegios.clear()
#            privilegios=form.cleaned_data['Privilegios']
#            for privilegio in privilegios:
#                permiso.privilegios.add(privilegio)
#            permiso.save()  
#            return HttpResponseRedirect('/administracion/roles/permisos/' + str(id) +'/' + rol.Tipo + '/')
#    else:
#        dict = {}
#        listaprivilegios=permiso.privilegios.all()
#        for privilegio in listaprivilegios:
#            dict[privilegio.id] = True
#        form = PrivilegioForm({'Privilegios': dict})
#    contexto = RequestContext(request, {'form': form,
#                                         'rol': rol,
#                                         'permiso': permiso,
#                                         })
#    return render_to_response('admin/Permisos/GestionPrivilegios.html', contexto)
    

###########################CONTROL DE ARTEFACTOS###########################
@login_required
def administrar_artefactos(request):
 
    user = User.objects.get(username=request.user.username)
    artefactos = Artefacto.objects.filter(Activo=True).order_by('Nombre')
    return render_to_response('admin/artefacto/administrar_artefacto.html', {'user': user, 'artefactos': artefactos,})

def verInformacion_Artefacto(request, pid, id):
    user = User.objects.get(username=request.user.username)
    artefacto = Artefacto.objects.get(pk=id, Activo=True)
    proyecto=Proyecto.objects.get(pk=pid)
    Mispadres = RelacionArtefacto.objects.filter(artefactoHijo=artefacto, Activo=True).values_list('artefactoPadre', flat=True)
    
    Mispadres = Artefacto.objects.filter(id__in=Mispadres).order_by('id')
    antecesores = Mispadres.exclude(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
    Mispadres = Mispadres.filter(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
    Mishijos = RelacionArtefacto.objects.filter(artefactoPadre=artefacto, Activo=True).values_list('artefactoHijo', flat=True)
    Mishijos = Artefacto.objects.filter(id__in=Mishijos).order_by('id')
    
    hijosFaseSigte = Mishijos.exclude(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
    hijosMismaFase = Mishijos.filter(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
     
    archivos = ArchivosAdjuntos.objects.filter(Artefacto=artefacto, Activo=True)
    if artefacto.Estado== 'I':
        estado= "Implementando"
    else:
        estado= "Aprobado"
        
    if artefacto.Prioridad== 'B':
        Prioridad= "Baja"
    if artefacto.Prioridad== 'M':
        Prioridad= "Media"
    if artefacto.Prioridad== 'A':
        Prioridad= "Alta"
    if artefacto.Prioridad== 'U':
        Prioridad= "Urgente"
    
    
    Fase=artefacto.Tipo_Artefacto.Fase
    contexto = RequestContext(request, {'user': user,
                                        'artefacto': artefacto,
                                        'padres':Mispadres ,
                                        'antecesores': antecesores,
                                        'hijosS': hijosFaseSigte,
                                        'hijosF': hijosMismaFase,
                                        'proyecto':proyecto,
                                        'Fase':Fase,
                                        'Estado': estado,
                                        'archivos': archivos,
                                        'Prioridad': Prioridad,
                                        })
    return render_to_response('admin/artefacto/informacion_artefacto.html', contexto )

        
@login_required
def agregarArtefacto(request, id, fase):
    user = User.objects.get(username=request.user.username)
    proyec = Proyecto.objects.get(pk = id),
    if request.method == 'POST':
        form = ArtefactoForm(id, fase, request.POST)
        if form.is_valid():
            artefacto = Artefacto(
                      Tipo_Artefacto = form.cleaned_data['Tipo_Artefacto'],
                      Proyecto = Proyecto.objects.get(pk = id),
                      DescripcionCorta=form.cleaned_data['DescripcionCorta'],
                      DescripcionLarga=form.cleaned_data['DescripcionLarga'],                     
                      Version=1,
                      Prioridad=form.cleaned_data['Prioridad'],
                      Complejidad=form.cleaned_data['Complejidad'],
                      Usuario = request.user,
                      Estado='I',
                      Activo=True,
                      
            )
            
            numero= Numeracion.objects.filter(Proyecto=artefacto.Proyecto, Tipo_Artefacto = artefacto.Tipo_Artefacto)
            if numero:
                numero= Numeracion.objects.get(Proyecto=artefacto.Proyecto, Tipo_Artefacto = artefacto.Tipo_Artefacto)
            
            if numero:
                artefacto.Nombre= artefacto.Tipo_Artefacto.Codigo  +  str(numero.Ultimo_nro)
                numero.Ultimo_nro= numero.Ultimo_nro + 1
                numero.save()
            else:
                artefacto.Nombre= artefacto.Tipo_Artefacto.Codigo +  str(1) 
#                print artefacto.Nombre
                numero=Numeracion(Proyecto=artefacto.Proyecto, Tipo_Artefacto = artefacto.Tipo_Artefacto)   
                numero.Ultimo_nro=2
                numero.save()        
    
            
            artefacto.save()
            
            registrarHistorialArt(artefacto)
            if fase =='E':
                return HttpResponseRedirect("/proyecto/" + str(id) + "/requerimientos/")
            if fase =='D':
                return HttpResponseRedirect("/proyecto/" + str(id) + "/diseno/")
            if fase == 'I':
                return HttpResponseRedirect("/proyecto/" + str(id) + "/implementacion/")
    else:
        form = ArtefactoForm(id, fase)
    return render_to_response('admin/artefacto/crearArtefacto.html', {'user': user,'form': form,  'proyecto': id, 'fase': fase,})


def modificarArtefacto(request, id_p, fase, id_ar):
    user = User.objects.get(username=request.user.username)
    mensaje=None
    artefacto = Artefacto.objects.get(id=id_ar)
    if artefacto.Estado == 'A':
            mensaje="El artefacto ha cambiado de estado Aprobado a Implementando."

    if request.method == 'POST':
        artefacto = Artefacto.objects.get(id=id_ar)
        #actualizar la version a la cual estara apuntando el historial, luego de la modificacion
       ##########aK SALE ERROR CUANDO NO AY HISTORIAL###############
       
        artefacto_hist = HistorialArt.objects.get(Artefacto = artefacto, Version = artefacto.Version)
        
        ################################################################
        form = ModificarArtefactoForm(request.POST)
        if form.is_valid():
            artefacto_hist.Actual = False
            artefacto_hist.save()
            
            artefacto.Estado='I'
            artefacto.DescripcionCorta=form.cleaned_data['DescripcionCorta'],
            artefacto.DescripcionLarga=form.cleaned_data['DescripcionLarga'],
            artefacto.Prioridad=form.cleaned_data['Prioridad']
            artefacto.Complejidad=form.cleaned_data['Complejidad']
            artefacto.Version = artefacto.Version + 1
            artefacto.Usuario = request.user
            artefacto.save()
            
            registrarHistorialArt(artefacto)
            if fase =='E':
                return HttpResponseRedirect("/proyecto/" + str(id_p) + "/requerimientos/")
            if fase =='D':
                return HttpResponseRedirect("/proyecto/" + str(id_p) + "/diseno/")
            if fase == 'I':
                return HttpResponseRedirect("/proyecto/" + str(id_p) + "/implementacion/")
    else:
        artefacto = get_object_or_404(Artefacto, id=id_ar)
        form = ModificarArtefactoForm(initial={
                             'Estado': artefacto.Estado,
                             'Prioridad': artefacto.Prioridad,
                             'Complejidad': artefacto.Complejidad,
                             'DescripcionCorta':artefacto.DescripcionCorta,
                             'DescripcionLarga': artefacto.DescripcionLarga,})
    return render_to_response('admin/artefacto/modificarArtefacto.html', {'user': user,'form': form, 'artefacto': artefacto, 'fase': fase, 'ProyectoId': id_p, 'mensaje':mensaje})

@login_required
def eliminarArtefacto(request, id_p, fase, id_ar):
    user = User.objects.get(username=request.user.username)
    artefacto = get_object_or_404(Artefacto, id=id_ar)
    relacionesPadre = RelacionArtefacto.objects.filter(artefactoPadre = artefacto, Activo=True)
    relacionesHijo = RelacionArtefacto.objects.filter(artefactoHijo = artefacto, Activo=True)
    error= None
    if relacionesPadre:
        error= 'Hay artefacto que dependen de el. No se puede eliminar si existe dependencias'
    if request.method == 'POST':
        artefacto_hist = HistorialArt.objects.get(Artefacto = artefacto, Version = artefacto.Version)
        artefacto_hist.Actual = False
        artefacto_hist.save()
        
        artefacto.Activo=False
        for rel in relacionesHijo:
            rel.Activo = False
            rel.save()
        artefacto.save()
        
        registrarHistorialArt(artefacto)

        if fase =='E':
                return HttpResponseRedirect("/proyecto/" + str(id_p) + "/requerimientos/")
        if fase =='D':
                return HttpResponseRedirect("/proyecto/" + str(id_p) + "/diseno/")
        if fase == 'I':
                return HttpResponseRedirect("/proyecto/" + str(id_p) + "/implementacion/")

    return render_to_response('admin/artefacto/eliminarArtefacto.html', {'user': user, 'artefacto': artefacto, 'fase':fase, 'ProyectoId': id_p, 'mensaje':error,})



def TipoArtefactos(request):

    Tipo = Tipo_Artefacto.objects.all().order_by('Nombre')
    proyectos = Proyecto.objects.all().order_by('Nombre')
    user = User.objects.get(username=request.user.username)
    usrolsis= UsuarioRolSistema.objects.filter(usuario = user)
    for urs in usrolsis:
        CrearTipoDeArtefacto = urs.rol.permisos.filter(Nombre = 'CrearTipoDeArtefacto')
        EditarTipoDeArtefacto = urs.rol.permisos.filter(Nombre = 'EditarTipoDeArtefacto')
        EliminarTipoDeArtefacto = urs.rol.permisos.filter(Nombre = 'EliminarTipoDeArtefacto')
    return render_to_response('admin/Proyecto/TipoArtefacto.html', {'user': user, 'Tipo': Tipo,'EditarTipoDeArtefacto':EditarTipoDeArtefacto, 'EliminarTipoDeArtefacto':EliminarTipoDeArtefacto, 'CrearTipoDeArtefacto':CrearTipoDeArtefacto,})


def Agregar_tipo_artefacto(request):
    user = User.objects.get(username=request.user.username)
    proyectos = Proyecto.objects.all()
    if request.method == 'POST':
        form = Tipo_ArtefactoForm(request.POST)
        if form.is_valid():
            tipo = Tipo_Artefacto(
                      Nombre = form.cleaned_data['Nombre'],
                      Codigo= form.cleaned_data['Codigo'],
                      Fase = form.cleaned_data['Fase'],
                      Descripcion= form.cleaned_data['Descripcion'],
            )
            tipo.save()
            for proyecto in proyectos:
                tipopro = Tipo_Artefacto_Proyecto(
                      Nombre = form.cleaned_data['Nombre'],
                      Fase = form.cleaned_data['Fase'],
                      Descripcion= form.cleaned_data['Descripcion'],
                      TipoArtefactoGeneral = tipo,
                      Proyecto = proyecto
                )
                tipopro.save()
            return HttpResponseRedirect('/administracion/tipo_artefacto/')
    else:
        form = Tipo_ArtefactoForm()
    return render_to_response('admin/Proyecto/agregarTipo_artefacto.html', {'user': user, 'form': form })

def modificar_tipo_artefacto(request, id):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        tipo_artefacto = Tipo_Artefacto.objects.get(id=id)
        form = Mod_Tipo_ArtefactoForm(request.POST)
        if form.is_valid():
            tipo_artefacto.Fase=form.cleaned_data['Fase']
            tipo_artefacto.Descripcion= form.cleaned_data['Descripcion'],
            tipo_artefacto.save()
            return HttpResponseRedirect('/administracion/tipo_artefacto/')
    else:
        tipo_artefacto = get_object_or_404(Tipo_Artefacto, id=id)
        form = Mod_Tipo_ArtefactoForm(initial={
                             'Nombre': tipo_artefacto.Nombre,
                             'Fase': tipo_artefacto.Fase,
                             'Descripcion':tipo_artefacto.Descripcion})



    return render_to_response('admin/artefacto/editarTipo_artefacto.html', {'user': user, 'form': form, 'tipo_artefacto': tipo_artefacto,})


@login_required
def eliminar_tipo_artefacto(request, id):
    user = User.objects.get(username=request.user.username)
    tipo_artefacto = get_object_or_404(Tipo_Artefacto, pk=id)
    artefactos = Artefacto.objects.filter(Activo=True, Tipo_Artefacto=tipo_artefacto)
    eliminar = None
    if artefactos:
        eliminar = True
    if request.method == 'POST':
        tipo_artefacto.delete()
        return HttpResponseRedirect('/administracion/tipo_artefacto/')
    return render_to_response('admin/artefacto/eliminarTipo_artefacto.html', {'user': user,'tipo_artefacto': tipo_artefacto,'eliminar':eliminar,})

##################Falta implementar todaviaaa###################################################

def TipoArtefactosProyecto(request, id_p):
    
    proyecto = Proyecto.objects.get(pk=id_p)
    Tipo = Tipo_Artefacto_Proyecto.objects.filter(Proyecto=proyecto).order_by('Nombre')
    user = User.objects.get(username=request.user.username)
    usrolpro= UsuarioRolProyecto.objects.filter(usuario = user).exclude(rol = None)
    for urp in usrolpro:
        CrearTipoArtefactoEspecifico = urp.rol.permisos.filter(Nombre = 'CrearTipoArtefactoEspecifico')
        EditarTipoArtefactoEspecifico= urp.rol.permisos.filter(Nombre = 'EditarTipoArtefactoEspecifico')
        EliminarTipoArtefactoEspecifico = urp.rol.permisos.filter(Nombre = 'EliminarTipoArtefactoEspecifico')
    return render_to_response('proyec/tipoArtefactosProyecto.html', {'user': user, 'Tipo': Tipo, 'Proyecto':proyecto,'CrearTipoArtefactoEspecifico':CrearTipoArtefactoEspecifico,'EditarTipoArtefactoEspecifico':EditarTipoArtefactoEspecifico,'EliminarTipoArtefactoEspecifico':EliminarTipoArtefactoEspecifico,})



def crearTipoArtefactosProyecto(request, p_id):
    user = User.objects.get(username=request.user.username)
    proyecto=Proyecto.objects.get(pk=p_id)
    if request.method == 'POST':
        form = Tipo_Artefacto_ProyectoForm(request.POST)
        if form.is_valid():
            tipoProyecto = Tipo_Artefacto_Proyecto(
                      Nombre = form.cleaned_data['Nombre'],
                      Codigo= form.cleaned_data['Codigo'],
                      Fase = form.cleaned_data['Fase'],
                      Descripcion= form.cleaned_data['Descripcion'],
                      Proyecto=proyecto
            )
            tipoProyecto.save()
            return HttpResponseRedirect('/proyecto/' + str(proyecto.id) + '/tipoArtefacto/')
    else:
        form = Tipo_Artefacto_ProyectoForm()
    return render_to_response('proyec/crearTipoArtefactosProyecto.html', {'user': user, 'form': form, 'Proyecto': proyecto, })

def editarTipoArtefactosProyecto(request, id, id_ta):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        tipo_artefacto = Tipo_Artefacto_Proyecto.objects.get(id=id_ta)
        artefactos = Artefacto.objects.all()
        ta = False
        for artefacto in artefactos:
            if artefacto.Tipo_Artefacto == tipo_artefacto:
                ta = True
        if ta:
            fase = tipo_artefacto.Fase
            if fase == 'E':
                form = Edi_Tipo_Artefacto_Proyecto_ReqForm(request.POST)
            if fase == 'D':
                form = Edi_Tipo_Artefacto_Proyecto_DisForm(request.POST)
            if fase == 'I':
                form = Edi_Tipo_Artefacto_Proyecto_ImpForm(request.POST)
            if form.is_valid():
                tipo_artefacto.Descripcion= form.cleaned_data['Descripcion'],
                tipo_artefacto.save()
        else:
            form = Edi_Tipo_Artefacto_ProyectoForm(request.POST)
        if form.is_valid():
            tipo_artefacto.Fase=form.cleaned_data['Fase']
            tipo_artefacto.Descripcion= form.cleaned_data['Descripcion'],
            tipo_artefacto.save()
            return HttpResponseRedirect('/proyecto/' + str(id) + '/tipoArtefacto/')
    else:
        tipo_artefacto = get_object_or_404(Tipo_Artefacto_Proyecto, id=id_ta)
        form = Edi_Tipo_Artefacto_ProyectoForm(initial={
                             'Fase': tipo_artefacto.Fase,
                             'Descripcion':tipo_artefacto.Descripcion})



    return render_to_response('proyec/editarTipoArtefactosProyecto.html', {'user': user, 'form': form, 'tipo_artefacto': tipo_artefacto,'proyecto': id})


@login_required
def eliminarTipoArtefactosProyecto(request, id, id_ta):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(id=id)
    tipo_artefacto = get_object_or_404(Tipo_Artefacto_Proyecto, pk=id_ta)
    artefactos = Artefacto.objects.filter(Proyecto=proyecto, Activo=True, Tipo_Artefacto=tipo_artefacto)
    eliminar = None
    if artefactos:
        eliminar = True
    if request.method == 'POST':
        tipo_artefacto.delete()
        return HttpResponseRedirect('/proyecto/' + str(id) + '/tipoArtefacto/')
    return render_to_response('proyec/eliminarTipoArtefactosProyecto.html', {'user': user,'tipo_artefacto': tipo_artefacto,'proyecto':id,'eliminar': eliminar,})

###############################################################################################

@login_required
def FaseERequerimientos(request, id):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(id=id)
    Aprobado=False
    LineaBaseReq= Linea_Base.objects.filter(Proyecto=proyecto, Fase='E')
    if LineaBaseReq:
        Aprobado=True
    tipo_artefacto= Tipo_Artefacto_Proyecto.objects.filter(Fase='E', Proyecto=proyecto)
    artefactos = Artefacto.objects.filter(Proyecto=proyecto, Activo=True, Tipo_Artefacto__in=tipo_artefacto)
    usrolpro= UsuarioRolProyecto.objects.filter(usuario = user)
    for urp in usrolpro:
        AprobarArtefacto = urp.rol.permisos.filter(Nombre = 'AprobarArtefacto')
        CrearArtefactoReq = urp.rol.permisos.filter(Nombre = 'CrearArtefactoReq')
        EditarArtefactoReq = urp.rol.permisos.filter(Nombre = 'EditarArtefactoReq')
        EliminarArtefactoReq = urp.rol.permisos.filter(Nombre = 'EliminarArtefactoReq')
        confrelaciones = urp.rol.permisos.filter(Nombre = 'ConfigurarRelaciones')
        impacto = urp.rol.permisos.filter(Nombre = 'CalcularImpacto')
    contexto = RequestContext(request, {'proyecto': proyecto,
                                         'AprobarArtefacto':AprobarArtefacto,
                                         'artefactos': artefactos,
                                         'Fase':'E',
                                         'EditarArtefactoReq': EditarArtefactoReq,
                                         'EliminarArtefactoReq': EliminarArtefactoReq,
                                         'CrearArtefactoReq': CrearArtefactoReq,
                                         'Aprobado': Aprobado,
                                         'confrelaciones':confrelaciones,
                                         'impacto':impacto,
                                         })
    return render_to_response('admin/artefacto/FaseRequerimiento.html', contexto)



@login_required
def FaseDiseno(request, id):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(id=id)
    
    LineaBaseReq= Linea_Base.objects.filter(Proyecto=proyecto, Fase='E')
    LineaBaseDisenho= Linea_Base.objects.filter(Proyecto=proyecto, Fase='D')
    Paso=False
    if LineaBaseReq:
        Paso=True
        if LineaBaseDisenho:
            Paso=False

    tipo_artefacto= Tipo_Artefacto_Proyecto.objects.filter(Fase='D', Proyecto=proyecto)
    artefactos = Artefacto.objects.filter(Proyecto=proyecto, Activo=True, Tipo_Artefacto__in=tipo_artefacto)
    usrolpro= UsuarioRolProyecto.objects.filter(usuario = user)
    for urp in usrolpro:
        AprobarArtefacto = urp.rol.permisos.filter(Nombre = 'AprobarArtefacto')
        CrearArtefactoDis = urp.rol.permisos.filter(Nombre = 'CrearArtefactoDis')
        EditarArtefactoDis = urp.rol.permisos.filter(Nombre = 'EditarArtefactoDis')
        EliminarArtefactoDis = urp.rol.permisos.filter(Nombre = 'EliminarArtefactoDis')
        confrelaciones = urp.rol.permisos.filter(Nombre = 'ConfigurarRelaciones')
        confrelaciones = urp.rol.permisos.filter(Nombre = 'ConfigurarRelaciones')
        impacto = urp.rol.permisos.filter(Nombre = 'CalcularImpacto')
    contexto = RequestContext(request, {'proyecto': proyecto,
                                         'AprobarArtefacto':AprobarArtefacto,
                                         'artefactos': artefactos,
                                         'Fase':'D',
                                         'Paso': Paso,
                                         'EditarArtefactoDis': EditarArtefactoDis,
                                         'EliminarArtefactoDis': EliminarArtefactoDis,
                                         'CrearArtefactoDis': CrearArtefactoDis,
                                         'confrelaciones':confrelaciones,
                                         'impacto':impacto,
                                         })
    return render_to_response('admin/artefacto/FaseDiseno.html', contexto)


@login_required
def FaseImplementacion(request, id):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(id=id)
    LineaBaseDisenho= Linea_Base.objects.filter(Proyecto=proyecto, Fase='D')
    LineaBaseImplem= Linea_Base.objects.filter(Proyecto=proyecto, Fase='I')
    Paso=False
    if LineaBaseDisenho:
        Paso=True
        if LineaBaseImplem:
            Paso=False
    tipo_artefacto= Tipo_Artefacto_Proyecto.objects.filter(Fase='I', Proyecto=proyecto)
    artefactos = Artefacto.objects.filter(Proyecto=proyecto, Activo=True, Tipo_Artefacto__in=tipo_artefacto)
    usrolpro= UsuarioRolProyecto.objects.filter(usuario = user)
    for urp in usrolpro:
        AprobarArtefacto = urp.rol.permisos.filter(Nombre = 'AprobarArtefacto')
        CrearArtefactoImp = urp.rol.permisos.filter(Nombre = 'CrearArtefactoImp')
        EditarArtefactoImp = urp.rol.permisos.filter(Nombre = 'EditarArtefactoImp')
        EliminarArtefactoImp = urp.rol.permisos.filter(Nombre = 'EliminarArtefactoImp')
        confrelaciones = urp.rol.permisos.filter(Nombre = 'ConfigurarRelaciones')
        impacto = urp.rol.permisos.filter(Nombre = 'CalcularImpacto')
    contexto = RequestContext(request, {'proyecto': proyecto,
                                         'AprobarArtefacto':AprobarArtefacto,
                                         'artefactos': artefactos,
                                         'Fase':'I',
                                         'Paso': Paso,
                                         'EditarArtefactoImp': EditarArtefactoImp,
                                         'EliminarArtefactoImp': EliminarArtefactoImp,
                                         'CrearArtefactoImp': CrearArtefactoImp,
                                         'confrelaciones':confrelaciones,
                                         'impacto':impacto,
                                         })
    return render_to_response('admin/artefacto/FaseImplementacion.html', contexto)


@login_required
def AdministrarRelacionArtefacto(request, p_id, a_id):

    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(id=p_id)
    artefacto = Artefacto.objects.get(id=a_id)

    Mispadres = RelacionArtefacto.objects.filter(artefactoHijo=artefacto, Activo=True).values_list('artefactoPadre', flat=True)
    
    Mispadres = Artefacto.objects.filter(id__in=Mispadres).order_by('id')
    antecesores = Mispadres.exclude(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
    Mispadres = Mispadres.filter(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
    
    Mishijos = RelacionArtefacto.objects.filter(artefactoPadre=artefacto, Activo=True).values_list('artefactoHijo', flat=True)
    Mishijos = Artefacto.objects.filter(id__in=Mishijos).order_by('id')
         

    fase= artefacto.Tipo_Artefacto.Fase

    contexto = RequestContext(request, {'proyecto': proyecto,
                                         'artefacto': artefacto,
                                         'padres': Mispadres,
                                         'hijos': Mishijos,
                                         'antecesores': antecesores,
                                         'fase': fase,
                                         })

    return render_to_response('admin/artefacto/relacionArtefacto.html', contexto)

@login_required
def listarArtefactoRelacionables(request, p_id, a_id):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=p_id)
    artefacto = Artefacto.objects.get(pk=a_id)
    fase=artefacto.Tipo_Artefacto.Fase
    listaArtefactos = Artefacto.objects.filter(Proyecto=proyecto, Activo=True)
    listaArtefactos = listaArtefactos.exclude(id=artefacto.id) 
  
    listaArtefactos= eliminarPadresHijos(listaArtefactos,artefacto)
    listaArtefactos= eliminarDescendientes(listaArtefactos, artefacto)
            
    if artefacto.Tipo_Artefacto.Fase == 'I':
        tipos_req = Tipo_Artefacto_Proyecto.objects.filter(Fase='E', Proyecto=proyecto)
        listaArtefactos = listaArtefactos.exclude(Tipo_Artefacto__in=tipos_req)

    artefactos_ant = listaArtefactos.exclude(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)

    listaArtefactos = listaArtefactos.exclude(id__in=artefactos_ant)
    #### En caso de que solo deba tener un solo pader, no toy segura preguntar###########
    siPadre= RelacionArtefacto.objects.filter(artefactoHijo=artefacto, artefactoPadre__Tipo_Artefacto__Fase=fase, Activo=True)

    if siPadre:
        listaArtefactos = listaArtefactos.exclude(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)

    contexto = RequestContext(request, {
                'proyecto': proyecto,
                'artefacto': artefacto,
                'artefactos': listaArtefactos,
                'artefactos_ant': artefactos_ant,
                })
    return render_to_response('admin/artefacto/listarArtefactosRelacionables.html', contexto)
def eliminarPadresHijos(listaArtefactos, artefacto):
    
    Mispadres = RelacionArtefacto.objects.filter(artefactoHijo=artefacto, Activo=True)
    Mishijos = RelacionArtefacto.objects.filter(artefactoPadre=artefacto, Activo=True)
    if Mispadres:
        for padre in Mispadres:
            listaArtefactos = listaArtefactos.exclude(id=padre.artefactoPadre.id)
    if Mishijos:
        for hijo in Mishijos:
            listaArtefactos = listaArtefactos.exclude(id=hijo.artefactoHijo.id)
    return listaArtefactos

def eliminarDescendientes(artefactos, artefacto):

    hijos = RelacionArtefacto.objects.filter(artefactoPadre=artefacto, Activo=True)
    hijos2= []
    if hijos:
        for hijo in hijos:
                hijos2.append(hijo.artefactoHijo)

    hijos = RelacionArtefacto.objects.filter(artefactoPadre__in=hijos2, Activo=True)
    hijos3= []
    if hijos:
        for hijo in hijos:
                hijos3.append(hijo.artefactoHijo)
    while hijos3:
        for hijo in hijos3:
            artefactos = artefactos.exclude(id=hijo.id)
        hijos = RelacionArtefacto.objects.filter(artefactoPadre__in=hijos3, Activo=True)
        hijos3= []
        if hijos:
             for hijo in hijos:
                 hijos3.append(hijo.artefactoHijo)

    return artefactos 




@login_required
def crearRelacionArtefacto(request, p_id, arPadre_id, arHijo_id):

    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=p_id)
    artefactoPadre = Artefacto.objects.get(id=arPadre_id)
    artefactoHijo = Artefacto.objects.get(id=arHijo_id)
    Relacion_Artefacto = RelacionArtefacto.objects.filter(artefactoPadre = artefactoHijo, artefactoHijo=artefactoPadre)
    if Relacion_Artefacto:
        artefacto_hist = HistorialArt.objects.get(Artefacto=artefactoPadre, Actual=True)
        artefacto_hist.Actual = False
        artefacto_hist.save()
        
        relacion_artefacto=RelacionArtefacto.objects.get(artefactoPadre = artefactoHijo, artefactoHijo=artefactoPadre)
        relacion_artefacto.Activo=True
        relacion_artefacto.save()
        registrarHistorialRel(relacion_artefacto)
        
        artefactoPadre.Version = artefactoPadre.Version + 1
        artefactoPadre.save()
        registrarHistorialArt(artefactoPadre)
        
    else:
        artefacto_hist = HistorialArt.objects.get(Artefacto=artefactoPadre, Actual=True)
        artefacto_hist.Actual = False
        artefacto_hist.save()
        
        relacion_artefacto = RelacionArtefacto(artefactoPadre=artefactoHijo,
                                       artefactoHijo=artefactoPadre, Activo=True)
    
        relacion_artefacto.save()
        registrarHistorialRel(relacion_artefacto)
        
        artefactoPadre.Version = artefactoPadre.Version + 1
        artefactoPadre.save()
        registrarHistorialArt(artefactoPadre)
        
    return HttpResponseRedirect("/proyectos/" + str(proyecto.id) + "/fase/artefactos/relaciones/" + str(arPadre_id) + "/")

@login_required
def eliminarRelacion(request, p_id, arPadre_id, arHijo_id):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=p_id)
    artefactoPadre = Artefacto.objects.get(pk=arPadre_id)
    artefactoHijo = Artefacto.objects.get(pk=arHijo_id)

    if request.method == 'POST':
        artefacto_hist = HistorialArt.objects.get(Artefacto=artefactoPadre, Actual=True)
        artefacto_hist.Actual = False
        artefacto_hist.save()
        
        relacionArtefacto = RelacionArtefacto.objects.get(artefactoPadre = artefactoHijo, artefactoHijo=artefactoPadre)
        relacionArtefacto.Activo=False
        relacionArtefacto.save()
        registrarHistorialRel(relacionArtefacto)
        
        artefactoPadre.Version = artefactoPadre.Version + 1
        artefactoPadre.save()
        registrarHistorialArt(artefactoPadre)
        
        return HttpResponseRedirect("/proyectos/" + str(proyecto.id) + "/fase/artefactos/relaciones/" + str(arPadre_id) + "/")

    contexto = RequestContext(request, {'proyecto': proyecto,
                                         'artefacto': artefactoPadre,
                                         'artefactoH': artefactoHijo,
                                         })
    return render_to_response('admin/artefacto/eliminar_relacion.html', contexto)

@login_required
def aprobarArtefacto(request, p_id, a_id, fase):
   
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=p_id)
    artefacto = Artefacto.objects.get(id=a_id)

    artefacto.Estado = 'A'
    artefacto.save()
    
    #registrarHistorialArt(artefacto)
      
    if fase =='E':
                return HttpResponseRedirect("/proyecto/" + str(proyecto.id) + "/requerimientos/")
    if fase =='D':
                return HttpResponseRedirect("/proyecto/" + str(proyecto.id) + "/diseno/")
    if fase == 'I':
                return HttpResponseRedirect("/proyecto/" + str(proyecto.id) + "/implementacion/")


@login_required
def Calculo_Impacto(request, p_id, artefacto_id):
   
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=p_id)
    artefacto = Artefacto.objects.get(pk=artefacto_id)

    Padres = []
    Hijos = []
    calculoImpactoPadres(Padres, artefacto_id)
    calculoImpactoHijos(Hijos, artefacto_id)
    CalculoPadres=0
    CalculoHijos=0
    CalculoAntecesores=0
    CalculoSucesores=0

    ArtefactosHijos = Artefacto.objects.filter(id__in=Hijos, Activo=True)
    ArtefactosPadres = Artefacto.objects.filter(id__in=Padres, Activo=True)
    ArtefactosAntecesores = ArtefactosPadres.exclude(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
    ArtefactoSucesores = ArtefactosHijos.exclude(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
    ArtefactosHijos = ArtefactosHijos.exclude(id__in=ArtefactoSucesores)
    ArtefactosPadres = ArtefactosPadres.exclude(id__in=ArtefactosAntecesores)
    
    if ArtefactosPadres:
        for Ar in ArtefactosPadres:
            complejidad= int(Ar.Complejidad)
            CalculoPadres = CalculoPadres + complejidad
    if ArtefactosHijos:
        for Ar in ArtefactosHijos:
            complejidad2= int(Ar.Complejidad)
            CalculoHijos= CalculoHijos + complejidad2
    
    if ArtefactosAntecesores:
        for Ar in ArtefactosAntecesores:
            complejidad= int(Ar.Complejidad)
            CalculoAntecesores = CalculoAntecesores + complejidad
    if ArtefactoSucesores:
        for Ar in ArtefactoSucesores:
            complejidad= int(Ar.Complejidad)
            CalculoSucesores = CalculoSucesores + complejidad
    CalculoImpacto = int(artefacto.Complejidad) + CalculoPadres + CalculoHijos + CalculoAntecesores + CalculoSucesores
    
    izquierda= CalculoPadres + CalculoAntecesores
    derecha=CalculoHijos + CalculoSucesores
    contexto = RequestContext(request, {'proyecto': proyecto,
                                         'Fase': artefacto.Tipo_Artefacto.Fase,
                                         'artefacto': artefacto,
                                         'CalculoHijos': CalculoHijos,
                                         'hijos': ArtefactosHijos,
                                         'CalculoPadres': CalculoPadres,
                                         'padres': ArtefactosPadres,
                                         'antesesores': ArtefactosAntecesores,
                                         'izquierda':izquierda,
                                         'derecha':derecha,
                                         'CalculoAntecesores':CalculoAntecesores,
                                         'sucesores':ArtefactoSucesores,
                                         'CalculoSucesores':CalculoSucesores,
                                         'CalculoImpacto': CalculoImpacto,
                                         
                                         })
    return render_to_response('admin/artefacto/CalculoImpacto.html', contexto)

def calculoImpactoHijos(ids, artefacto_id):

    artefacto = Artefacto.objects.get(id=artefacto_id)
    relaciones = RelacionArtefacto.objects.filter(artefactoPadre=artefacto, Activo=True)
    if relaciones:
        for relacion in relaciones:
            if not relacion.artefactoHijo.id in ids:
                ids.append(relacion.artefactoHijo.id)
                calculoImpactoHijos(ids, relacion.artefactoHijo.id)


def calculoImpactoPadres(ids, artefacto_id):

    artefacto = Artefacto.objects.get(id=artefacto_id)
    relaciones = RelacionArtefacto.objects.filter(artefactoHijo=artefacto, Activo=True)
    if relaciones:
        for relacion in relaciones:
            if not relacion.artefactoPadre.id in ids:
                ids.append(relacion.artefactoPadre.id)
                calculoImpactoPadres(ids, relacion.artefactoPadre.id)
                
                
############################### ARCHIVOS ##########################################
@login_required
def guardarArchivo(request, id_p, fase, id_ar):

    proyecto = Proyecto.objects.get(id=id_p)
    if request.method == 'POST':
        form = ArchivosAdjuntosForm(request.POST, request.FILES)
        
        artefacto = Artefacto.objects.get(id=id_ar)
            
        adjunto = request.FILES['archivo']
        artefacto_hist = HistorialArt.objects.get(Artefacto = artefacto, Version = artefacto.Version)
        
        try:
            archivo = ArchivosAdjuntos.objects.get(Artefacto=artefacto,
                                                   Nom_Archivo=adjunto.name,
                                                   Activo=True) 
            archivo.Activo = False
            archivo.save()
            archivo = ArchivosAdjuntos(Artefacto = artefacto,
                                       Nom_Archivo = adjunto.name,
                                       Contenido = base64.b64encode(adjunto.read()),
                                       Tamano = adjunto.size,
                                       TipoContenido = adjunto.content_type,
                                       Activo = True,
                                       )
            archivo.save(force_insert=True)

            artefacto_hist.Actual = False
            artefacto_hist.save()
            
            artefacto.Version = artefacto.Version + 1
            artefacto.save()
            registrarHistorialArt(artefacto)

        except:
            archivo = ArchivosAdjuntos(Artefacto = artefacto,
                                       Nom_Archivo = adjunto.name,
                                       Contenido = base64.b64encode(adjunto.read()),
                                       Tamano = adjunto.size,
                                       TipoContenido = adjunto.content_type,
                                       Activo = True,
                                       )
            archivo.save()
            
            artefacto_hist.Actual = False
            artefacto_hist.save()
            
            artefacto.Version = artefacto.Version + 1
            artefacto.save()
            
            registrarHistorialArt(artefacto)
    
    form = ArchivosAdjuntosForm()    
    artefacto = Artefacto.objects.get(id=id_ar)

    contexto = RequestContext(request, {'proyecto': proyecto,
                                        'Fase': fase,
                                        'form': form,
                                        'artefacto': artefacto,
                                         })
    return render_to_response('admin/artefacto/adjuntar_archivos.html', contexto)

@login_required
def listarArchivo(request, id_p, fase, id_ar):
    proyecto = Proyecto.objects.get(pk=id_p)
    artefacto = Artefacto.objects.get(pk=id_ar)
    
    archivos = ArchivosAdjuntos.objects.filter(Artefacto=artefacto, Activo=True)
    
    contexto = RequestContext(request, {'proyecto': proyecto,
                                        'Fase': fase,
                                        'artefacto': artefacto,
                                        'archivos': archivos,
                                         })
    return render_to_response('admin/artefacto/listar_archivos.html', contexto)

@login_required
def listarArchivoAprobado(request, id_p, fase, id_ar):
    proyecto = Proyecto.objects.get(pk=id_p)
    artefacto = Artefacto.objects.get(pk=id_ar)
    
    archivos = ArchivosAdjuntos.objects.filter(Artefacto=artefacto, Activo=True)
    
    contexto = RequestContext(request, {'proyecto': proyecto,
                                        'Fase': fase,
                                        'artefacto': artefacto,
                                        'archivos': archivos,
                                         })
    return render_to_response('admin/artefacto/listar_archivos_aprobado.html', contexto)


@login_required
def obtenerArchivo(request, id_p, id_ar, archivo_id):
    if request.method == 'GET':
        elArchivo = ArchivosAdjuntos.objects.get(pk=archivo_id)
        response = HttpResponse(base64.b64decode(elArchivo.Contenido), content_type=elArchivo.TipoContenido)
        response['Content-Disposition'] = 'attachment; filename='+elArchivo.Nom_Archivo
        response['Content-Length'] = elArchivo.Tamano
        return response
    return HttpResponse('.')

@login_required
def eliminar_adjunto(request, id_p, fase, id_ar, archivo_id):
    proyecto = Proyecto.objects.get(pk=id_p)
    artefacto = Artefacto.objects.get(pk=id_ar)
    archivo = get_object_or_404(ArchivosAdjuntos, pk=archivo_id)
    artefacto_hist = HistorialArt.objects.get(Artefacto = artefacto, Version = artefacto.Version)
    if request.method == 'POST':
        artefacto_hist.Actual = False

        archivo.Activo = False
        archivo.save()

        artefacto.Version = artefacto.Version + 1
        artefacto.save()
        
        registrarHistorialArt(artefacto)

        return HttpResponseRedirect("/proyecto/" + str(proyecto.id) + "/fase/" + fase + "/adjuntar/" + str(artefacto.id))
    contexto = RequestContext(request, {'proyecto': proyecto,
                                        'Fase': fase,
                                        'artefacto': artefacto,
                                         'archivo': archivo,
                                         })
    return render_to_response('admin/artefacto/eliminar_adjunto.html', contexto)

##################################### HISTORIAL - VERSIONES ##################################################################

@login_required
def menuHistorial(request, p_id, fase, ar_id):
    proyecto = Proyecto.objects.get(pk = p_id)
    artefacto = Artefacto.objects.get(pk = ar_id)

    contexto = RequestContext(request, {'proyecto': proyecto,
                                        'Fase': fase,
                                        'artefacto': artefacto,
                                        })
    return render_to_response('admin/artefacto/historiales.html', contexto)    
    
@login_required
def verHistorialArt(request, id_p, fase, id_ar):
    proyecto = Proyecto.objects.get(pk=id_p)
    artefacto = Artefacto.objects.get(pk=id_ar)
    
    listaHistorialArt = HistorialArt.objects.filter(Artefacto=artefacto)

    contexto = RequestContext(request, {'proyecto': proyecto,
                                        'Fase': fase,
                                        'artefacto': artefacto,
                                        'his_art': listaHistorialArt,
                                        })
    return render_to_response('admin/artefacto/historial_art.html', contexto)

@login_required
def verHistorialRel(request, id_p, fase, id_ar):
    proyecto = Proyecto.objects.get(pk=id_p)
    artefacto = Artefacto.objects.get(pk=id_ar)
    
    listaHistorialRel = HistorialRel.objects.filter(artefactoHijo=artefacto)
    
    contexto = RequestContext(request, {'proyecto': proyecto,
                                        'Fase': fase,
                                        'artefacto': artefacto,
                                        'his_rel': listaHistorialRel,
                                        })
    return render_to_response('admin/artefacto/historial_rel.html', contexto)

@login_required
def verHistorialAdj(request, id_p, fase, id_ar):
    proyecto = Proyecto.objects.get(pk=id_p)
    artefacto = Artefacto.objects.get(pk=id_ar)
    
    listaHistorialArt = HistorialArt.objects.filter(Artefacto=artefacto)
    listaHistorialAdj = HistorialAdj.objects.filter(Artefacto__in=listaHistorialArt)

    contexto = RequestContext(request, {'proyecto': proyecto,
                                        'Fase': fase,
                                        'artefacto': artefacto,
                                        'his_adj': listaHistorialAdj,
                                        })
    return render_to_response('admin/artefacto/historial_adj.html', contexto)

def detallesVersion(request, id_p, fase, id_ar, version):
    proyecto = Proyecto.objects.get(pk=id_p)
    artefacto = Artefacto.objects.get(pk=id_ar)
    
    relaciones = HistorialRel.objects.filter(artefactoHijo=artefacto, Activo=False).values_list('artefactoPadre', flat=True)

    Mispadres = Artefacto.objects.filter(id__in=relaciones, Version=version, Activo=True).order_by('id')
    
    antecesores = Mispadres.exclude(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
    
    Mipadre = Mispadres.filter(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
   
    Mishijos = HistorialRel.objects.filter(artefactoPadre=artefacto).values_list('artefactoHijo', flat=True)
    Mishijos = Mishijos.filter(artefactoHijo__Activo=True)
    Mishijos = Artefacto.objects.filter(id__in=Mishijos, Activo=True).order_by('id')
   

    contexto = RequestContext(request, {'proyecto': proyecto,
                                        'Fase': fase,
                                        'artefacto': artefacto,
                                        'version': version,
                                        'antecesores': antecesores,
                                        'padre': Mipadre,
                                        'hijos': Mishijos,
                                        })

    return render_to_response('admin/artefacto/detalles_version.html', contexto)

def reversionar(request, id_p, fase, id_ar, version):
    proyecto = Proyecto.objects.get(pk=id_p)
    artefacto = Artefacto.objects.get(pk=id_ar)
    
    version_archivos = artefacto.Version
    
    artefacto_hist = HistorialArt.objects.get(Artefacto = artefacto, Version = artefacto.Version)
    artefacto_hist.Actual = False
    artefacto_hist.save()
    
    prev_version = HistorialArt.objects.get(Artefacto=id_ar, Version=version)
    
    anularRelacionesActuales(artefacto)
    
    artefacto.Tipo_Artefacto = prev_version.Tipo_Artefacto
    artefacto.Proyecto = prev_version.Proyecto
    artefacto.DescripcionCorta = prev_version.DescripcionCorta
    artefacto.DescripcionLarga = prev_version.DescripcionLarga                     
    artefacto.Version = artefacto.Version + 1
    artefacto.Prioridad = prev_version.Prioridad
    artefacto.Complejidad = prev_version.Complejidad
    artefacto.Usuario = request.user
    artefacto.Estado = prev_version.Estado
    artefacto.Activo=True
    
    artefacto.save()
    
    registrarHistorialArt(artefacto)
    
    #prev_artefacto = Artefacto.objects.get(id=id_ar, Version=version)    
    relaciones_padres = HistorialRel.objects.filter(artefactoHijo=prev_version).values_list('artefactoPadre', flat=True)
    
    padres_valid = Artefacto.objects.filter(id__in=relaciones_padres, Activo=True).order_by('id')
    padres_invalid = Artefacto.objects.filter(id__in=relaciones_padres, Activo=False).order_by('id')
    
    antecesores_valid = padres_valid.exclude(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
    antecesores_invalid = padres_invalid.exclude(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
    
    Mipadre = padres_valid.filter(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
   
    relaciones_hijos = HistorialRel.objects.filter(artefactoPadre=prev_version).values_list('artefactoHijo', flat=True)
    
    hijos_valid = Artefacto.objects.filter(id__in=relaciones_hijos, Activo=True).order_by('id')
    hijos_invalid = Artefacto.objects.filter(id__in=relaciones_hijos, Activo=False).order_by('id')
    
    activarRelacionesAnteriores(artefacto, padres_valid, antecesores_valid, hijos_valid)

    activarArchivos(artefacto, prev_version.Artefacto.id, version_archivos)
    
    contexto = RequestContext(request, {'proyecto': proyecto,
                                        'Fase': fase,
                                        'artefacto': artefacto,
                                        'version': version,
                                        'antecesores_invalid': antecesores_invalid,
                                        'padres_invalid': padres_invalid,
                                        'hijos_invalid': hijos_invalid,
                                        })

    return render_to_response('admin/artefacto/reversion.html', contexto)
    
    
def activarRelacionesAnteriores(padres_valid, antecesores_valid, hijos_valid):
    
    for padre in padres_valid:
        relacion = RelacionArtefacto.objects.get(artefactoPadre=padre)
        relacion.Activo = True
        relacion.save()
        
    for antecesor in antecesores_valid:
        relacion = RelacionArtefacto.objects.get(artefactoPadre=antecesor)
        relacion.Activo = True
        relacion.save()
        
    for hijo in hijos_valid:
        relacion = RelacionArtefacto.objects.get(artefactoHijo=hijo)
        relacion.Activo = True
        relacion.save()
        
def activarArchivos(artefacto, prev_artefacto_id, version_archivos):
    
    artefacto_anterior = Artefacto.objects.get(pk=prev_artefacto_id)
    archivos_anterior = ArchivosAdjuntos.objects.filter(Artefacto=artefacto_anterior)
    
    artefacto_actual = Artefacto.objects.get(Version=version_archivos)
    archivos_actual = ArchivosAdjuntos.objects.filter(Artefacto=artefacto_actual)
    
    for archivo_ant in archivos_anterior:
        for archivo_act in archivos_actual:
            if archivo_ant.Nom_Archivo != archivo_act.Nom_Archivo:
                archivo_ant.Activo = True
                archivo_ant.Artefacto = artefacto
                archivo_ant.save()
            else:
                archivo_act.Artefacto = artefacto
                archivo_act.save()

#################################################################################################


@login_required
def LineaBase(request, p_id):
    proyecto = Proyecto.objects.get(id=p_id)
    requerimientos= Linea_Base.objects.filter(Proyecto=proyecto, Fase='E')
    fase='E'
    if requerimientos:
        disenho= Linea_Base.objects.filter(Proyecto=proyecto, Fase='D')
        fase= 'D'
        if disenho:
            implementacion= Linea_Base.objects.filter(Proyecto=proyecto, Fase='I')
            fase='I'
            if implementacion:
                fase='T'
    
    contexto = RequestContext(request, {
                'proyecto': proyecto,
                'fase':fase,
                })

    return render_to_response('proyec/lineaBase.html', contexto)

      


@login_required
def GenerarLineaBase(request, p_id, fase):
    
    proyecto = Proyecto.objects.get(id=p_id)
    lista=[]
    error= None
   
    TipoArtefacto = Tipo_Artefacto_Proyecto.objects.filter(Fase=fase, Proyecto=proyecto)
    artefactos = Artefacto.objects.filter(Proyecto=proyecto, Tipo_Artefacto__in=TipoArtefacto, Activo=True)
    
    if artefactos:
        error=comprobarCondiciones(artefactos, lista, fase)
        print error
        if not error:
            if request.method == 'POST':
                LineaBase= Linea_Base(Fase=fase, Proyecto=proyecto)
                LineaBase.save()
                return HttpResponseRedirect('/proyecto/'+ str(proyecto.id) + '/lineaBase/')
    else:
        error= "No existe ningun artefacto en la Fase"
    contexto = RequestContext(request, {
                            'mensaje': error,
                            'artefactos':lista,                        
                            'proyecto': proyecto,
                            'fase': fase,
                            })
    
    return render_to_response('proyec/generarLB.html', contexto)

def comprobarCondiciones(artefactos, lista, fase):
      NoAprobados = artefactos.exclude(Estado='A')
      if  NoAprobados:
          lista.extend(NoAprobados)
          mensaje="Hay artefactos no aprobados aun"
          return mensaje
      else:
          if fase == 'E':
             return None
          else:
               for artefacto in artefactos:
                  relaciones = RelacionArtefacto.objects.filter(artefactoHijo=artefacto, Activo=True)
                  if not relaciones:
                     lista.append(artefacto)
               if lista:
                  mensaje= "Hay artefactos que no estan relacionados con ningun artefacto de la face anterior"
                  return  mensaje
               else: 
                 return None
