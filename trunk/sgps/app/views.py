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



@login_required
def pagina_principal(request):
    user = User.objects.get(username=request.user.username)
    usrolpros= UsuarioRolProyecto.objects.filter(usuario=user)
    proyectoUser=Proyecto.objects.filter(id__in=usrolpros).order_by('Nombre')
    usrolsis= UsuarioRolSistema.objects.filter(usuario = user)
    Usuarios = False
    Proyectos = False
    Roles = False
    Tipo_Artefactos = False
    for urs in usrolsis:
        permi = urs.rol.permisos.all()
        for per in permi:
            if per.Nombre =='AdministrarProyectos':
                Proyectos = True
            if per.Nombre =='AdministrarUsuarios':
                Usuarios = True
            if per.Nombre =='AdministrarRoles':
                Roles = True              
            if per.Nombre =='AdministrarTipoDeArtefacto':
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
    usuarios = User.objects.all()
    usrolsis= UsuarioRolSistema.objects.filter(usuario = user)
    Editar = False
    Eliminar = False
    Escribir = False
    for urs in usrolsis:
        permi = urs.rol.permisos.filter(Nombre = 'AdministrarUsuarios')
        for per in permi:
            privi = per.privilegios.all()
            for pri in privi:
                if pri.Nombre =='Editar':
                    Editar = True
                if pri.Nombre =='Eliminar':
                    Eliminar = True
                if pri.Nombre =='Escribir':
                    Escribir = True
    return render_to_response('admin/Usuario/administrar_usuarios.html', {'username': user.username, 'usuarios': usuarios,'Editar':Editar,'Eliminar':Eliminar,'Escribir':Escribir,})


@login_required
def agregarUsuario(request):
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
    return render_to_response('admin/Usuario/registrar_usuario.html', {'form': form })



@login_required
def editarUsuario(request, id_user):
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
    return render_to_response('admin/Usuario/editarUsuario.html', {'form': form, 'usuario': usuario,})




@login_required
def ModificarContrasena(request, id_user):

    usuario = get_object_or_404(User, pk=id_user)
    if request.method == 'POST':
        form = ModificarContrasenaForm(request.POST)
        if form.is_valid():
            usuario.set_password(form.cleaned_data['passNueva'])
            usuario.save()
            return HttpResponseRedirect('/administracion/usuarios/')
    else:
        form = ModificarContrasenaForm()
    return render_to_response('admin/Usuario/cambiarContrasena.html', {'form': form, 'usuario': usuario,})

@login_required
def eliminarUsuario(request, id_user):

    user = User.objects.get(pk=id_user)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect('/administracion/usuarios/')
    return render_to_response('admin/Usuario/eliminarUsuario.html', {'usuario': user,})

@login_required
def asignarRolesSistema(request, usuario_id):
    
    user = User.objects.get(username=request.user.username)
    usuario = get_object_or_404(User, id=usuario_id)
    rolesUsuario = UsuarioRolSistema.objects.filter(usuario = usuario)
    if request.method == 'POST':
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
        form = RolSistemaForm(initial={'roles': dict})
    return render_to_response("admin/Usuario/asignarRolesSistema.html", {'form':form, 'usuario':usuario, 'user':user})




##################################### Control de Proyecto ###################################


@login_required
def administrar_proyectos(request):
    proyectos = Proyecto.objects.all().order_by('Nombre')
    return render_to_response('admin/Proyecto/administrarProyectos.html', {'proyectos': proyectos,})

@login_required
def nuevo_proyecto(request):
    
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = Proyecto(Nombre=form.cleaned_data["Nombre"],
                                Usuario=form.cleaned_data["Usuario"],
                                Descripcion=form.cleaned_data["Descripcion"],
                                )
            proyecto.save()
            return HttpResponseRedirect('/administracion/proyectos/')
    else:
        form = ProyectoForm()
    return render_to_response('admin/Proyecto/CrearProyecto.html', {'form': form,})


def modificarProyecto(request, id):
    if request.method == 'POST':
        proyecto = Proyecto.objects.get(id=id)
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto.Nombre=form.cleaned_data['Nombre']
            proyecto.Usuario=form.cleaned_data['Usuario']
            proyecto.Descripcion=form.cleaned_data['Descripcion']
            proyecto.save()
            
            return HttpResponseRedirect('/administracion/proyectos/')
    else:
        
        #id = request.GET['id']
        proyecto = get_object_or_404(Proyecto, id=id)
        form = ProyectoForm(initial={'Nombre': proyecto.Nombre,
                             'Usuario': proyecto.Usuario.id, 'Descripcion': proyecto.Descripcion,})
    return render_to_response('admin/Proyecto/editarProyecto.html', {'form': form, 'proyecto': proyecto,})

def editar_proyecto(request, id):
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
    return render_to_response('proyec/editar_proyecto.html', {'form': form, 'proyecto': proyecto,})

@login_required
def eliminar_proyecto(request, id):

    proyecto = get_object_or_404(Proyecto, id=id)
    if request.method == 'POST':
        
        proyecto.delete()
        return HttpResponseRedirect('/administracion/proyectos/')
    return render_to_response('admin/Proyecto/eliminarProyecto.html', {'proyecto': proyecto,})

@login_required
def proyecto(request, id):
    
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=id)
        
    return render_to_response('proyec/proyecto.html', {'proyecto': proyecto})

@login_required
def usuariosMiembros(request, id):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk = id)
    UsRoPo = UsuarioRolProyecto.objects.filter(proyecto = proyecto)
    miembros = []
    for user in UsRoPo:
        if not user.usuario in miembros:
            miembros.append(user.usuario)
    
    return render_to_response('admin/Proyecto/administrarMiembros.html',{'user':user, 'proyecto':Proyecto.objects.get(id=id), 'miembros': miembros})

@login_required
def agregar_miembros(request, id):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = UsuarioProyectoForm(request.POST)
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
       
        form = UsuarioProyectoForm()
    return render_to_response('admin/Proyecto/agregarMiembro.html', {'form':form, 'user':user,  'proyecto':Proyecto.objects.get(pk=id)})

@login_required
def asignarRolProyecto(request, id, id_us):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk = id)
    usuario = User.objects.get(pk = id_us)
    URP= UsuarioRolProyecto.objects.filter(proyecto = proyecto, usuario = usuario)
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
    if request.method == 'POST':
        URP= UsuarioRolProyecto.objects.filter(proyecto = proyecto, usuario = usuario)
        for urp in URP:
            urp.delete()
        return HttpResponseRedirect("/proyecto/" + str(id) + "/usuarios_miembros/")
    else:
        return render_to_response("proyec/remover_miembro.html", {'usuario':usuario, 'proyecto':proyecto, 'user':user})

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

    roles = Rol.objects.filter(Tipo= Tipo).order_by('Nombre')
    contexto= RequestContext(request, {
                'roles': roles,
                'Tipo': Tipo,
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
        
        form = RolForm(request.POST)
        if form.is_valid():
            rol.Nombre=form.cleaned_data['Nombre']
            rol.Descripcion=form.cleaned_data['Descripcion']
            rol.save()
            
            return HttpResponseRedirect('/administracion/roles/' + Tipo + '/')
    else:
        #id = request.GET['id']
        rol = get_object_or_404(Rol, id=id)
        form = RolForm({ 'Nombre': rol.Nombre,
                                 'Descripcion': rol.Descripcion,
                                 'Tipo': rol.Tipo,
                                 })

    return render_to_response('admin/Roles/EditarRol.html', {'form': form, 'rol': rol,'Tipo': Tipo,})
@login_required
def eliminarRoles(request, id, Tipo):

    rol = Rol.objects.get(id=id)
    if request.method == 'POST':
        rol.delete()
        return HttpResponseRedirect('/administracion/roles/' + Tipo +'/')
    return render_to_response('admin/Roles/eliminarRoles.html', {'rol': rol,'Tipo': Tipo,})
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

@login_required
def GestionarPrivilegios(request,id,per_id):
    rol = Rol.objects.get(id=id)
    permiso = Permiso.objects.get(id=per_id)
    if request.method == 'POST':
        form = PrivilegioForm(request.POST)
        if form.is_valid():
            permiso.privilegios.clear()
            privilegios=form.cleaned_data['Privilegios']
            for privilegio in privilegios:
                permiso.privilegios.add(privilegio)
            permiso.save()
            return HttpResponseRedirect('/administracion/roles/permisos/' + str(id) +'/' + rol.Tipo + '/')
    else:
        dict = {}
        listaprivilegios=permiso.privilegios.all()
        for privilegio in listaprivilegios:
            dict[privilegio.id] = True
        form = PrivilegioForm({'Privilegios': dict})
    contexto = RequestContext(request, {'form': form,
                                         'rol': rol,
                                         'permiso': permiso,
                                         })
    return render_to_response('admin/Permisos/GestionPrivilegios.html', contexto)
    

###########################CONTROL DE ARTEFACTOS###########################
@login_required
def administrar_artefactos(request):


    artefactos = Artefacto.objects.all().order_by('Prioridad')
    return render_to_response('admin/artefacto/administrar_artefacto.html', {'artefactos': artefactos,})


@login_required
def agregarArtefacto(request, id, fase):
    if request.method == 'POST':
        form = ArtefactoForm(fase, request.POST)
        if form.is_valid():
            artefacto = Artefacto(
                      Tipo_Artefacto = form.cleaned_data['Tipo_Artefacto'],
                      Proyecto = Proyecto.objects.get(pk = id),
                      # Fase = form.cleaned_data['Fase'],
                      Prioridad=form.cleaned_data['Prioridad'],
                      Complejidad=form.cleaned_data['Complejidad'],
                      Estado='N',
            )
            artefacto.save()
            if fase =='E':
                return HttpResponseRedirect("/proyecto/" + str(id) + "/requerimientos/")
            if fase =='D':
                return HttpResponseRedirect("/proyecto/" + str(id) + "/diseno/")
            if fase == 'I':
                return HttpResponseRedirect("/proyecto/" + str(id) + "/implementacion/")
    else:
        form = ArtefactoForm(fase)
    return render_to_response('admin/artefacto/crearArtefacto.html', {'form': form,  'proyecto': id, 'fase': fase,})


def modificarArtefacto(request, id_p, fase, id_ar):
    if request.method == 'POST':
        artefacto = Artefacto.objects.get(id=id_ar)
        form = ModificarArtefactoForm(request.POST)
        if form.is_valid():
            artefacto.Estado=form.cleaned_data['Estado']
            artefacto.Prioridad=form.cleaned_data['Prioridad']
            artefacto.Complejidad=form.cleaned_data['Complejidad']
            artefacto.save()
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
                             'Complejidad': artefacto.Complejidad,})
    return render_to_response('admin/artefacto/modificarArtefacto.html', {'form': form, 'artefacto': artefacto, 'fase': fase, 'ProyectoId': id_p})

@login_required
def eliminarArtefacto(request, id_p, fase, id_ar):

    artefacto = get_object_or_404(Artefacto, id=id_ar)
    if request.method == 'POST':
        # En este caso si quiero que la eliminacion sea ON CASCADE
       artefacto.delete()
       if fase =='E':
                return HttpResponseRedirect("/proyecto/" + str(id_p) + "/requerimientos/")
       if fase =='D':
                return HttpResponseRedirect("/proyecto/" + str(id_p) + "/diseno/")
       if fase == 'I':
                return HttpResponseRedirect("/proyecto/" + str(id_p) + "/implementacion/")

    return render_to_response('admin/artefacto/eliminarArtefacto.html', {'artefacto': artefacto, 'fase':fase, 'ProyectoId': id_p,})



def TipoArtefactos(request):

    Tipo = Tipo_Artefacto.objects.all()
    return render_to_response('admin/Proyecto/TipoArtefacto.html', {'Tipo': Tipo,})


def Agregar_tipo_artefacto(request):
    if request.method == 'POST':
        form = Tipo_ArtefactoForm(request.POST)
        if form.is_valid():
            tipo = Tipo_Artefacto(
                      Nombre = form.cleaned_data['Nombre'],
                      Fase = form.cleaned_data['Fase'],
            )
            tipo.save()
            return HttpResponseRedirect('/administracion/tipo_artefacto/')
    else:
        form = Tipo_ArtefactoForm()
    return render_to_response('admin/Proyecto/agregarTipo_artefacto.html', {'form': form })

def modificar_tipo_artefacto(request, id):
    if request.method == 'POST':
        tipo_artefacto = Tipo_Artefacto.objects.get(id=id)
        form = Tipo_ArtefactoForm(request.POST)
        if form.is_valid():
            tipo_artefacto.Nombre=form.cleaned_data['Nombre']
            tipo_artefacto.Fase=form.cleaned_data['Fase']
            tipo_artefacto.save()
            return HttpResponseRedirect('/administracion/tipo_artefacto/')
    else:
        tipo_artefacto = get_object_or_404(Tipo_Artefacto, id=id)
        form = Tipo_ArtefactoForm(initial={
                             'Nombre': tipo_artefacto.Nombre,
                             'Fase': tipo_artefacto.Fase,})


    contexto = RequestContext(request, {'form': form, 'tipo_artefacto': tipo_artefacto,})
    return render_to_response('admin/artefacto/editarTipo_artefacto.html', contexto)


@login_required
def eliminar_tipo_artefacto(request, id):
    
    tipo_artefacto = get_object_or_404(Tipo_Artefacto, pk=id)
    if request.method == 'POST':
        tipo_artefacto.delete()
        return HttpResponseRedirect('/administracion/tipo_artefacto/')
    return render_to_response('admin/artefacto/eliminarTipo_artefacto.html', {'tipo_artefacto': tipo_artefacto,})



@login_required
def FaseERequerimientos(request, id):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(id=id)
    tipo_artefacto= Tipo_Artefacto.objects.filter(Fase='E')
    artefactos = Artefacto.objects.filter(Proyecto=proyecto, Tipo_Artefacto__in=tipo_artefacto)
    
    contexto = RequestContext(request, {'proyecto': proyecto,
                                         'artefactos': artefactos,
                                         'Fase':'E',
                                         })
    return render_to_response('admin/artefacto/FaseRequerimiento.html', contexto)



@login_required
def FaseDiseno(request, id):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(id=id)
    tipo_artefacto= Tipo_Artefacto.objects.filter(Fase='D')
    artefactos = Artefacto.objects.filter(Proyecto=proyecto, Tipo_Artefacto__in=tipo_artefacto)
    contexto = RequestContext(request, {'proyecto': proyecto,
                                         'artefactos': artefactos,
                                         'Fase':'D',
                                         })
    return render_to_response('admin/artefacto/FaseDiseno.html', contexto)


@login_required
def FaseImplementacion(request, id):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(id=id)
    tipo_artefacto= Tipo_Artefacto.objects.filter(Fase='I')
    artefactos = Artefacto.objects.filter(Proyecto=proyecto, Tipo_Artefacto__in=tipo_artefacto)
    contexto = RequestContext(request, {'proyecto': proyecto,
                                         'artefactos': artefactos,
                                         'Fase':'I',
                                         })
    return render_to_response('admin/artefacto/FaseImplementacion.html', contexto)


@login_required
def AdministrarRelacionArtefacto(request, p_id, a_id):

    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(id=p_id)
    artefacto = Artefacto.objects.get(id=a_id)

    Mispadres = RelacionArtefacto.objects.filter(artefactoHijo=artefacto).values_list('artefactoPadre', flat=True)
    Mispadres = Artefacto.objects.filter(id__in=Mispadres).order_by('id')
    antecesores = Mispadres.exclude(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
    Mispadres = Mispadres.filter(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)
    Mishijos = RelacionArtefacto.objects.filter(artefactoPadre=artefacto).values_list('artefactoHijo', flat=True)
    

    fase= artefacto.Tipo_Artefacto.Fase

    contexto = RequestContext(request, {'proyecto': proyecto,
                                         'artefacto': artefacto,
                                         'padres': Mispadres,
                                         'antecesores': antecesores,
                                         'fase': fase,
                                         })

    return render_to_response('admin/artefacto/relacionArtefacto.html', contexto)

@login_required
def listarArtefactoRelacionables(request, p_id, a_id):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=p_id)
    artefacto = Artefacto.objects.get(pk=a_id)
    listaArtefactos = Artefacto.objects.filter(Proyecto=proyecto)
    listaArtefactos = listaArtefactos.exclude(id=artefacto.id) 
  
    listaArtefactos= eliminarPadresHijos(listaArtefactos,artefacto)
    listaArtefactos= eliminarDescendientes(listaArtefactos, artefacto)
    if artefacto.Tipo_Artefacto.Fase == 'I':
        tipos_req = Tipo_Artefacto.objects.filter(Fase='E')
        artefactos = artefactos.exclude(Tipo_Artefacto__in=tipos_req)

    artefactos_ant = listaArtefactos.exclude(Tipo_Artefacto__Fase=artefacto.Tipo_Artefacto.Fase)

    listaArtefactos = listaArtefactos.exclude(id__in=artefactos_ant) 

    contexto = RequestContext(request, {
                'proyecto': proyecto,
                'artefacto': artefacto,
                'artefactos': listaArtefactos,
                'artefactos_ant': artefactos_ant,
                })
    return render_to_response('admin/artefacto/listarArtefactosRelacionables.html', contexto)
def eliminarPadresHijos(listaArtefactos, artefacto):
    
    Mispadres = RelacionArtefacto.objects.filter(artefactoHijo=artefacto)
    Mishijos = RelacionArtefacto.objects.filter(artefactoPadre=artefacto)
    if Mispadres:
        for padre in Mispadres:
            listaArtefactos = listaArtefactos.exclude(id=padre.artefactoPadre.id)
    if Mishijos:
        for hijo in Mishijos:
            listaArtefactos = listaArtefactos.exclude(id=hijo.artefactoHijo.id)
    return listaArtefactos

def eliminarDescendientes(artefactos, artefacto):

    hijos = RelacionArtefacto.objects.filter(artefactoPadre=artefacto)
    hijos2= []
    if hijos:
        for hijo in hijos:
                hijos2.append(hijo.artefactoHijo)

    hijos = RelacionArtefacto.objects.filter(artefactoPadre__in=hijos2)
    hijos3= []
    if hijos:
        for hijo in hijos:
                hijos3.append(hijo.artefactoHijo)
    while hijos3:
        for hijo in hijos3:
            artefactos = artefactos.exclude(id=hijo.id)
        hijos = RelacionArtefacto.objects.filter(artefactoPadre__in=hijos3)
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

    relacion_artefacto = RelacionArtefacto(artefactoPadre=artefactoHijo,
                                   artefactoHijo=artefactoPadre)

    relacion_artefacto.save()
    return HttpResponseRedirect("/proyectos/" + str(proyecto.id) + "/fase/artefactos/relaciones/" + str(arPadre_id) + "/")

@login_required
def eliminarRelacion(request, p_id, arPadre_id, arHijo_id):
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=p_id)
    artefactoPadre = Artefacto.objects.get(pk=arPadre_id)
    artefactoHijo = Artefacto.objects.get(pk=arHijo_id)

    if request.method == 'POST':
        relacionArtefacto = RelacionArtefacto.objects.get(artefactoPadre = artefactoHijo, artefactoHijo=artefactoPadre)
        relacionArtefacto.delete()
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

    padresId = []
    hijosId = []
    calculoImpactoPadres(padresId, artefacto_id)
    calculoImpactoHijos(hijosId, artefacto_id)
    CalculoPadres=0
    CalculoHijos=0
    if padresId:
        for item in padresId:
            artefacto2 = Artefacto.objects.get(pk=item)
            complejidad= int(artefacto2.Complejidad)
            CalculoPadres = CalculoPadres + complejidad
    if hijosId:
        for item in hijosId:
            artefacto3 = Artefacto.objects.get(pk=item)
            complejidad2= int(artefacto3.Complejidad)
            CalculoHijos= CalculoHijos + complejidad2

    hijos = Artefacto.objects.filter(id__in=hijosId)
    padres = Artefacto.objects.filter(id__in=padresId)
    CalculoImpacto = int(artefacto.Complejidad) + CalculoPadres + CalculoHijos

    contexto = RequestContext(request, {'proyecto': proyecto,
                                         'Fase': artefacto.Tipo_Artefacto.Fase,
                                         'artefacto': artefacto,
                                         'CalculoHijos': CalculoHijos,
                                         'hijos': hijos,
                                         'CalculoPadres': CalculoPadres,
                                         'padres': padres,
                                         'CalculoImpacto': CalculoImpacto,
                                         
                                         })
    return render_to_response('admin/artefacto/CalculoImpacto.html', contexto)

def calculoImpactoHijos(ids, artefacto_id):

    artefacto = Artefacto.objects.get(id=artefacto_id)
    relaciones = RelacionArtefacto.objects.filter(artefactoPadre=artefacto)
    if relaciones:
        for relacion in relaciones:
            if not relacion.artefactoHijo.id in ids:
                ids.append(relacion.artefactoHijo.id)
                calculoImpactoHijos(ids, relacion.artefactoHijo.id)


def calculoImpactoPadres(ids, artefacto_id):

    artefacto = Artefacto.objects.get(id=artefacto_id)
    relaciones = RelacionArtefacto.objects.filter(artefactoHijo=artefacto)
    if relaciones:
        for relacion in relaciones:
            if not relacion.artefactoPadre.id in ids:
                ids.append(relacion.artefactoPadre.id)
                calculoImpactoPadres(ids, relacion.artefactoPadre.id)
