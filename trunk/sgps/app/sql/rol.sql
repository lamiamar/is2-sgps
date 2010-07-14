INSERT INTO app_rol ( "Nombre", "Descripcion", "Tipo" )
VALUES ('Aministrador del Sistema', 'Rol predeterminado para Administrar el Sistema', 'S' ),
       ('Lider de Proyecto', 'Rol predeterminado para el Lider de Proyecto', 'P' );

INSERT INTO app_rol_permisos ( rol_id, permiso_id )
VALUES( 1, 1 ),( 1, 2 ),( 1, 3 ),( 1, 4 ),( 1, 5 ),( 1, 6 ),( 1, 7 ),( 1, 8 ),
( 1, 9 ),( 1, 10 ),( 1, 11 ),( 1, 12 ),( 1, 13 ),( 1, 14 ),( 1, 15 ),( 1, 16 ),
( 1, 17 ),( 1, 18 ),( 2, 19 ),( 2, 20 ),( 2, 21 ),( 2, 22 ),( 2, 23 ),( 2, 24 ),
( 2, 25 ),( 2, 26 ),( 2, 27 ),( 2, 28 ),( 2, 29 ),( 2, 30 ),( 2, 31 ),( 2, 32 ),
( 2, 33 ),( 2, 34 ),( 2, 35 ),( 2, 36 ),( 2, 37 ),( 2, 38 ),( 2, 39 ),( 2, 40 ),
( 2, 41 );

INSERT INTO app_usuariorolsistema (usuario_id, rol_id) VALUES (1, 1);

INSERT INTO app_usuariorolproyecto (usuario_id, rol_id, proyecto_id) VALUES (1, 2, 1);