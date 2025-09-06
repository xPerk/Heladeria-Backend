# Base de Datos para Heladería

Este proyecto contiene la estructura de base de datos PostgreSQL para gestionar los productos de una heladería.

## Estructura del Proyecto

### Scripts SQL
- `database_schema.sql` - Script para crear la estructura de la base de datos
- `sample_data.sql` - Datos de ejemplo para poblar la base de datos
- `queries.sql` - Consultas básicas y operaciones CRUD

### Scripts de Configuración
- `setup_database.ps1` - Script PowerShell para configuración automática
- `setup_database.bat` - Script Batch alternativo
- `INSTALACION.md` - Guía detallada de instalación paso a paso

## Requisitos

- PostgreSQL 12 o superior
- Cliente de PostgreSQL (psql, pgAdmin, etc.)
- Windows 10/11 (para scripts de instalación)

## 🚀 Instalación Rápida

### Opción 1: Script Automático (Recomendado)

1. **Instala PostgreSQL** siguiendo la guía en `INSTALACION.md`
2. **Ejecuta el script de configuración:**
   ```powershell
   .\setup_database.ps1
   ```

### Opción 2: Instalación Manual

1. **Consulta la guía detallada:** Ver `INSTALACION.md` para instrucciones paso a paso

2. **Crear la base de datos:**
   ```sql
   psql -U postgres -c "CREATE DATABASE heladeria_db;"
   ```

3. **Ejecutar scripts en orden:**
   ```powershell
   psql -U postgres -d heladeria_db -f database_schema.sql
   psql -U postgres -d heladeria_db -f sample_data.sql
   ```

## Estructura de la Base de Datos

### Tabla `categorias`
- `id` - Identificador único (SERIAL)
- `nombre` - Nombre de la categoría (VARCHAR 50)
- `descripcion` - Descripción de la categoría (TEXT)
- `activo` - Estado activo/inactivo (BOOLEAN)
- `fecha_creacion` - Fecha de creación (TIMESTAMP)

### Tabla `productos`
- `id` - Identificador único (SERIAL)
- `nombre` - Nombre del producto (VARCHAR 100)
- `sabor` - Sabor del helado (VARCHAR 50)
- `descripcion` - Descripción del producto (TEXT)
- `precio` - Precio unitario al por menor (DECIMAL 10,2)
- `precio_mayorista` - Precio unitario al por mayor (DECIMAL 10,2)
- `cantidad_minima_mayorista` - Cantidad mínima para precio mayorista (INTEGER)
- `stock` - Cantidad en inventario (INTEGER)
- `categoria_id` - Referencia a categoría (INTEGER)
- `activo` - Estado activo/inactivo (BOOLEAN)
- `fecha_creacion` - Fecha de creación (TIMESTAMP)
- `fecha_actualizacion` - Fecha de última actualización (TIMESTAMP)

## Categorías Incluidas

1. **Helados Cremosos** - Helados tradicionales con base de crema
2. **Sorbetes** - Helados a base de agua con frutas
3. **Helados Premium** - Helados gourmet con ingredientes especiales
4. **Paletas** - Helados en palito
5. **Postres Helados** - Tortas y postres elaborados

## Consultas Básicas

El archivo `queries.sql` incluye ejemplos de:

- Listar productos por categoría
- Buscar productos por sabor
- Consultar stock bajo
- Filtrar por rango de precios
- Operaciones CRUD completas
- Consultas de inventario
- **Gestión de precios mayoristas**

## Funcionalidades de Precios Mayoristas

La base de datos incluye un sistema completo de precios mayoristas:

### Características:
- **Precio dual**: Cada producto puede tener precio normal y precio mayorista
- **Cantidad mínima**: Se define la cantidad mínima para acceder al precio mayorista
- **Cálculo automático**: Funciones que determinan automáticamente qué precio aplicar
- **Análisis de descuentos**: Consultas para ver el porcentaje de descuento mayorista

### Funciones incluidas:
- `calcular_precio_producto(producto_id, cantidad)` - Calcula el precio según la cantidad
- `calcular_total_compra(productos_ids[], cantidades[])` - Calcula el total de una compra mixta

### Consultas especiales:
- Productos con descuento mayorista disponible
- Productos más rentables para ventas mayoristas
- Productos sin precio mayorista configurado
- Análisis de disponibilidad para ventas mayoristas

## Características Especiales

- **Borrado lógico**: Los productos se marcan como inactivos en lugar de eliminarse
- **Triggers automáticos**: Actualización automática de fecha de modificación
- **Índices optimizados**: Para mejorar el rendimiento de consultas
- **Validaciones**: Restricciones de precio y stock
- **Comentarios**: Documentación en la base de datos

## Uso Básico

```sql
-- Listar todos los productos activos
SELECT p.nombre, p.sabor, p.precio, c.nombre as categoria
FROM productos p
JOIN categorias c ON p.categoria_id = c.id
WHERE p.activo = TRUE;

-- Agregar nuevo producto
INSERT INTO productos (nombre, sabor, precio, stock, categoria_id)
VALUES ('Helado Menta', 'Menta', 2.80, 30, 1);

-- Actualizar stock
UPDATE productos SET stock = stock - 1 WHERE id = 1;
```

## Mantenimiento

- Revisar regularmente productos con stock bajo
- Actualizar precios según sea necesario
- Mantener categorías organizadas
- Hacer respaldos regulares de la base de datos

## Extensiones Futuras

- Tabla de ventas
- Gestión de proveedores
- Control de usuarios
- Historial de precios
- Sistema de descuentos