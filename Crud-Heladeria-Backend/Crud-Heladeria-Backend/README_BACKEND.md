# API Backend - Heladería

API REST desarrollada con FastAPI y Python para la gestión de una heladería, incluyendo sistema de precios mayoristas.

## 🚀 Características

- **CRUD completo** para categorías y productos
- **Sistema de precios mayoristas** con cantidades mínimas
- **Cálculo automático de precios** según cantidad
- **Gestión de stock** en tiempo real
- **Filtros y paginación** en consultas
- **Soft delete** (eliminación lógica)
- **Validación de datos** con Pydantic
- **Documentación automática** con Swagger/OpenAPI

## 📋 Requisitos Previos

- Python 3.8+
- PostgreSQL 12+
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
cd Crud-Heladeria-Backend
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

1. Asegúrate de que PostgreSQL esté ejecutándose
2. Crea la base de datos ejecutando los scripts SQL:
   ```bash
   psql -U postgres -c "CREATE DATABASE heladeria_db;"
   psql -U postgres -d heladeria_db -f database_schema.sql
   psql -U postgres -d heladeria_db -f sample_data.sql
   ```

### 5. Configurar variables de entorno

Edita el archivo `.env` con tus credenciales de base de datos:
```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/heladeria_db
APP_NAME=Heladeria API
APP_VERSION=1.0.0
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

## 🚀 Ejecución

### Desarrollo
```bash
python main.py
```

### Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📚 Documentación de la API

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔗 Endpoints Principales

### Categorías
- `GET /api/v1/categorias/` - Listar categorías
- `POST /api/v1/categorias/` - Crear categoría
- `GET /api/v1/categorias/{id}` - Obtener categoría
- `PUT /api/v1/categorias/{id}` - Actualizar categoría
- `DELETE /api/v1/categorias/{id}` - Eliminar categoría
- `PATCH /api/v1/categorias/{id}/activar` - Activar categoría

### Productos
- `GET /api/v1/productos/` - Listar productos
- `POST /api/v1/productos/` - Crear producto
- `GET /api/v1/productos/{id}` - Obtener producto
- `PUT /api/v1/productos/{id}` - Actualizar producto
- `DELETE /api/v1/productos/{id}` - Eliminar producto
- `PATCH /api/v1/productos/{id}/activar` - Activar producto
- `PATCH /api/v1/productos/{id}/stock` - Actualizar stock
- `GET /api/v1/productos/{id}/precio` - Calcular precio por cantidad
- `GET /api/v1/productos/mayorista/disponibles` - Productos con precio mayorista
- `GET /api/v1/productos/categoria/{categoria_id}` - Productos por categoría

## 💰 Sistema de Precios Mayoristas

La API incluye un sistema completo de precios mayoristas:

### Características
- **Precio dual**: precio normal y precio mayorista por producto
- **Cantidad mínima**: cantidad mínima requerida para aplicar precio mayorista
- **Cálculo automático**: la API calcula automáticamente qué precio aplicar

### Ejemplo de uso
```bash
# Calcular precio para 5 unidades del producto ID 1
GET /api/v1/productos/1/precio?cantidad=5

# Respuesta
{
  "producto_id": 1,
  "cantidad": 5,
  "precio_unitario": 15.00,
  "precio_total": 75.00,
  "es_precio_mayorista": false
}
```

## 🗂️ Estructura del Proyecto

```
Crud-Heladeria-Backend/
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py          # Configuración de SQLAlchemy
│   ├── models/
│   │   ├── __init__.py
│   │   ├── categoria.py         # Modelo de categorías
│   │   └── producto.py          # Modelo de productos
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── categorias.py        # Endpoints de categorías
│   │   └── productos.py         # Endpoints de productos
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── categoria.py         # Esquemas Pydantic de categorías
│   │   └── producto.py          # Esquemas Pydantic de productos
│   └── __init__.py
├── .env                         # Variables de entorno
├── main.py                      # Punto de entrada de la aplicación
├── requirements.txt             # Dependencias de Python
├── database_schema.sql          # Estructura de la base de datos
├── sample_data.sql             # Datos de ejemplo
└── README_BACKEND.md           # Este archivo
```

## 🧪 Pruebas

Puedes probar la API usando:

1. **Swagger UI** en http://localhost:8000/docs
2. **curl** o **Postman**
3. **HTTPie**:

```bash
# Listar productos
http GET localhost:8000/api/v1/productos/

# Crear una categoría
http POST localhost:8000/api/v1/categorias/ nombre="Helados Premium" descripcion="Helados de alta calidad"

# Crear un producto
http POST localhost:8000/api/v1/productos/ nombre="Chocolate Belga" precio:=25.50 precio_mayorista:=20.00 cantidad_minima_mayorista:=10 categoria_id:=1
```

## 🔧 Configuración Avanzada

### Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL de conexión a PostgreSQL | `postgresql://postgres:password@localhost:5432/heladeria_db` |
| `APP_NAME` | Nombre de la aplicación | `Heladeria API` |
| `APP_VERSION` | Versión de la aplicación | `1.0.0` |
| `DEBUG` | Modo debug | `True` |
| `HOST` | Host del servidor | `0.0.0.0` |
| `PORT` | Puerto del servidor | `8000` |

### CORS

Por defecto, la API permite todas las origins. En producción, modifica la configuración en `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-frontend.com"],  # Especifica dominios
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## 🐛 Solución de Problemas

### Error de conexión a la base de datos
1. Verifica que PostgreSQL esté ejecutándose
2. Confirma las credenciales en el archivo `.env`
3. Asegúrate de que la base de datos `heladeria_db` exista

### Error de importación de módulos
1. Activa el entorno virtual
2. Instala las dependencias: `pip install -r requirements.txt`

### Puerto en uso
1. Cambia el puerto en `.env`: `PORT=8001`
2. O mata el proceso que usa el puerto 8000

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.