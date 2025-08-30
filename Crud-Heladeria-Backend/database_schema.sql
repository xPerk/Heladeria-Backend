-- Active: 1756475921663@@127.0.0.1@5432@Heladeria
-- Base de datos para Heladería
-- Script de creación de estructura

-- Crear base de datos (ejecutar como superusuario)
-- CREATE DATABASE heladeria_db;
-- \c heladeria_db;

-- Tabla de categorías
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de productos
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    sabor VARCHAR(50) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
    precio_mayorista DECIMAL(10,2) CHECK (precio_mayorista > 0 AND precio_mayorista <= precio),
    cantidad_minima_mayorista INTEGER DEFAULT 10 CHECK (cantidad_minima_mayorista > 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    categoria_id INTEGER REFERENCES categorias(id),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_productos_categoria ON productos(categoria_id);
CREATE INDEX idx_productos_activo ON productos(activo);
CREATE INDEX idx_productos_nombre ON productos(nombre);

-- Función para actualizar fecha de modificación
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar automáticamente la fecha de modificación
CREATE TRIGGER trigger_actualizar_fecha_productos
    BEFORE UPDATE ON productos
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

-- Comentarios en las tablas
COMMENT ON TABLE categorias IS 'Categorías de productos de la heladería';
COMMENT ON TABLE productos IS 'Productos disponibles en la heladería';
COMMENT ON COLUMN productos.precio IS 'Precio unitario al por menor';
COMMENT ON COLUMN productos.precio_mayorista IS 'Precio unitario al por mayor (debe ser menor o igual al precio normal)';
COMMENT ON COLUMN productos.cantidad_minima_mayorista IS 'Cantidad mínima requerida para aplicar precio mayorista';
COMMENT ON COLUMN productos.stock IS 'Cantidad disponible en inventario';