from django.conf.urls.defaults import *
from app.views import *
from django.views.generic.create_update import *
from django.contrib.auth.models import User
import os.path
from django.contrib import admin
admin.autodiscover()
site_media = os.path.join(os.path.dirname(__file__), 'site_media')
urlpatterns = patterns('',
    
    (r'^admin/', include(admin.site.urls)),
    (r'^$', pagina_principal),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),
    
    # Contro de usuarios.......................
    (r'^administracion/usuarios/$', administrar_usuarios),
    (r'^administracion/usuarios/registrar/$', agregarUsuario),
    (r'^administracion/usuarios/editar/(\d+)/$', editarUsuario),
    (r'^administracion/usuarios/cambiar_contrasena/(\d+)$', ModificarContrasena),
    (r'^administracion/usuarios/eliminar/(\d+)$', eliminarUsuario),
    (r'^administracion/usuarios/asignar_rol&id=(?P<usuario_id>\d+)/$', asignarRolesSistema),
    
    # Control de proyectos.............

    (r'^proyectos/(?P<id>\d+)/$', proyecto),
    (r'^administracion/proyectos/$', administrar_proyectos),
    (r'^administracion/proyectos/nuevo/$', nuevo_proyecto),
    (r'^administracion/proyectos/eliminar/(.*)$', eliminar_proyecto),
    
    (r'^administracion/proyectos/editar&id=(?P<id>\d+)/$', modificarProyecto),
    (r'^proyectos/(?P<id>\d+)/editar/$', editar_proyecto),
    (r'^proyecto/(\d+)/lineaBase/(\w+)/generarLB/$', GenerarLineaBase),
    (r'^proyecto/(\d+)/lineaBase/$', LineaBase),
    (r'^proyecto/(\d+)/tipoArtefacto/$', TipoArtefactosProyecto),
    (r'^proyecto/(\d+)/tipoArtefacto/crearTipoArtefacto/$', crearTipoArtefactosProyecto),
    (r'^proyecto/(\d+)/tipoArtefacto/editarTipoArtefacto/(\d+)/$', editarTipoArtefactosProyecto),
    (r'^proyecto/(\d+)/tipoArtefacto/eliminarTipoArtefacto/(\d+)/$', eliminarTipoArtefactosProyecto),
    (r'^proyecto/(?P<id>\d+)/usuarios_miembros/$', usuariosMiembros),
    (r'^proyecto/(?P<id>\d+)/usuarios_miembros/agregar_usuario/$', agregar_miembros),
    (r'^proyecto/(?P<id>\d+)/usuarios_miembros/asignar_rol/(?P<id_us>\d+)/$', asignarRolProyecto),
    (r'^proyecto/(?P<id>\d+)/usuarios_miembros/remover_miembro/(?P<id_us>\d+)/$', removerMiembro),

    
    
    (r'^proyecto/(?P<id>\d+)/requerimientos/$', FaseERequerimientos),
    (r'^proyecto/(?P<id>\d+)/diseno/$', FaseDiseno),
    (r'^proyecto/(?P<id>\d+)/implementacion/$', FaseImplementacion),
    (r'^administracion/artefactos/$', administrar_artefactos),
    (r'^proyecto/(\d+)/fase/(\w+)/nuevo/$', agregarArtefacto),
    (r'^proyecto/(\d+)/fase/(\w+)/eliminar/(\d+)/$', eliminarArtefacto),
    (r'^proyecto/(\d+)/fase/(\w+)/editar/(\d+)/$', modificarArtefacto),

    (r'^proyectos/(?P<p_id>\d+)/fase/artefactos/relaciones/(?P<a_id>\d+)/$', AdministrarRelacionArtefacto),
    (r'^proyectos/(?P<p_id>\d+)/fase/artefactos/relaciones/(?P<a_id>\d+)/listarArtefactos/$',listarArtefactoRelacionables),
    (r'^proyectos/(?P<p_id>\d+)/fase/artefactos/relaciones/(?P<arPadre_id>\d+)/crearRelacion/(?P<arHijo_id>\d+)/$',crearRelacionArtefacto),
    (r'^proyectos/(?P<p_id>\d+)/fase/artefactos/relaciones/(?P<arPadre_id>\d+)/eliminarRelacion/(?P<arHijo_id>\d+)/$', eliminarRelacion),
    (r'^proyectos/(\d+)/fase/artefactos/aprobar/(\d+)/(\w+)/$', aprobarArtefacto),
    (r'^proyecto/(\d+)/impacto/(\d+)/$', Calculo_Impacto),
   
    
    #Control de roles..............
    (r'^administracion/roles/$', administrar_roles),
    (r'^administracion/roles/(\w+)/$', administrar_rolesTipo),
    (r'^administracion/roles/nuevo/(\w+)/$', crearRoles),
    (r'^administracion/roles/editar/(\d+)/(\w+)/$', modificarRol),
    (r'^administracion/roles/eliminar/(\d+)/(\w+)/$', eliminarRoles),
    (r'^administracion/roles/permisos/(\d+)/(\w+)/$', GestionarPermisos),
    (r'^administracion/roles/permisos/(\d+)/agregar$', agregar_permisos),
    #(r'^administracion/roles/privilegio/(\d+)/(\d+)/$', GestionarPrivilegios),    
    #Control de Tipo de Artefacto..........

    (r'^administracion/tipo_artefacto/$', TipoArtefactos),
    (r'^administracion/tipo_artefacto/nuevo/$', Agregar_tipo_artefacto),
    (r'^administracion/tipo_artefacto/eliminar&id=(?P<id>\d+)/$', eliminar_tipo_artefacto),
    (r'^administracion/tipo_artefacto/editar&id=(?P<id>\d+)/$', modificar_tipo_artefacto),
    
   # (r'^proyecto/(?P<id>\d+)/TipoArtefactos/$', Listar_tipo_artefacto_Proyecto),
   # (r'^proyecto/(?P<id>\d+)/TipoArtefactos/crear/$', Agregar_tipo_artefacto_Proyecto),
    
    ####### ARCHIVO ###########
    (r'^proyecto/(\d+)/fase/(\d+)/editar/adjuntar/$', guardarArchivo),
    (r'^proyecto/(\d+)/fase/(\d+)/editar/adjuntar/(\d+)/$', obtenerArchivo),
    (r'^proyecto/(\d+)/fase/(\d+)/editar/eliminar_adjunto/(\d+)/$', eliminar_adjunto), 

    ########## HISTORIAL #########
    (r'^proyecto/(\d+)/fase/(\w+)/historiales/(\d+)/$', menuHistorial),
    (r'^proyecto/(\d+)/fase/(\w+)/historial_art/(\d+)/$', verHistorialArt),
    (r'^proyecto/(\d+)/fase/(\w+)/historial_rel/(\d+)/$', verHistorialRel),
    (r'^proyecto/(\d+)/fase/(\w+)/historial_adj/(\d+)/$', verHistorialAdj),

)
