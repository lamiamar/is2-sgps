INSERT INTO app_rol ( "Nombre", "Descripcion", "Tipo" )
VALUES ('Aministrador del Sistema', 'Rol predeterminado para Administrar el Sistema', 'S' ),
       ('Lider de Proyecto', 'Rol predeterminado para el Lider de Proyecto', 'P' );

INSERT INTO app_rol_permisos ( rol_id, permiso_id )
VALUES( 1, 1 ),( 1, 2 ),( 1, 3 ),( 1, 4 ),( 2, 6 ),( 2, 7 ),( 2, 8 ),( 2, 9 ),( 2, 13 );

INSERT INTO app_permiso_privilegios ( permiso_id, privilegio_id )
VALUES( 1, 1 ),( 1, 2 ),( 1, 3 ),( 2, 1 ),( 2, 2 ),( 2, 3 ),( 3, 1 ),( 3, 2 ),( 3, 3 ),( 4, 1 ),( 4, 2 ),( 4, 3 ),( 6, 1 ),( 6, 2 ),( 6, 3 ),( 7, 1 ),( 7, 2 ),( 7, 3 ),( 8, 1 ),( 8, 2 ),( 8, 3 ),( 9, 1 ),( 9, 2 ),( 9, 3 ),( 13, 1 ),( 13, 2 ),( 13, 3 );

INSERT INTO app_usuariorolsistema (usuario_id, rol_id) VALUES (1, 1);

INSERT INTO app_usuariorolproyecto (usuario_id, rol_id, proyecto_id) VALUES (1, 2, 1);