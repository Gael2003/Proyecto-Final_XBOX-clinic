-- schema.sql

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT NOT NULL,
    contrasena TEXT NOT NULL,
    nombre_usuario TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS comentarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    comentario TEXT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);
