-- Script para agregar la tabla de usuarios a la base de datos existente
-- Ejecutar este script después de la implementación de autenticación

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_usuarios_username ON usuarios(username);
CREATE INDEX IF NOT EXISTS idx_usuarios_active ON usuarios(is_active);

-- Insertar usuario administrador por defecto (contraseña: admin123)
-- NOTA: Cambiar esta contraseña en producción
INSERT INTO usuarios (username, hashed_password, is_active) 
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3L3jzjvQSG', TRUE)
ON CONFLICT (username) DO NOTHING;

-- Comentarios:
-- El hash corresponde a la contraseña 'admin123'
-- Se recomienda cambiar esta contraseña después de la primera configuración
-- Para generar un nuevo hash, usar la función hash_password() del sistema