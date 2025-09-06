# Guía de Autenticación - API Heladería

## Configuración Inicial

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Base de Datos
Ejecutar el script SQL para crear la tabla de usuarios:
```bash
# Para PostgreSQL
psql -d tu_base_de_datos -f add_users_table.sql

# Para SQLite (si usas SQLite)
sqlite3 heladeria.db < add_users_table.sql
```

### 3. Variables de Entorno
Asegúrate de que el archivo `.env` contenga:
```
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Uso de la Autenticación

### Usuario por Defecto
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **IMPORTANTE:** Cambiar esta contraseña en producción.

### Endpoints de Autenticación

#### 1. Registro de Usuario
```http
POST /auth/register
Content-Type: application/json

{
    "username": "nuevo_usuario",
    "password": "contraseña_segura"
}
```

#### 2. Login
```http
POST /auth/login
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}
```

#### 3. Información del Usuario Actual
```http
GET /auth/me
Authorization: Basic YWRtaW46YWRtaW4xMjM=
```

#### 4. Listar Usuarios (solo para administradores)
```http
GET /auth/users
Authorization: Basic YWRtaW46YWRtaW4xMjM=
```

### Endpoints Protegidos

Los siguientes endpoints ahora requieren autenticación HTTP Basic:

#### Categorías
- `POST /categorias/` - Crear categoría
- `PUT /categorias/{categoria_id}` - Actualizar categoría
- `DELETE /categorias/{categoria_id}` - Eliminar categoría
- `PATCH /categorias/{categoria_id}/activar` - Activar/desactivar categoría

#### Productos
- `POST /productos/` - Crear producto
- `PUT /productos/{producto_id}` - Actualizar producto
- `DELETE /productos/{producto_id}` - Eliminar producto
- `PATCH /productos/{producto_id}/activar` - Activar/desactivar producto
- `PATCH /productos/{producto_id}/stock` - Actualizar stock

### Cómo Autenticarse

#### Usando curl
```bash
# Crear una nueva categoría
curl -X POST "http://localhost:8000/categorias/" \
  -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Helados Premium",
    "descripcion": "Helados de alta calidad"
  }'
```

#### Usando Python requests
```python
import requests
from requests.auth import HTTPBasicAuth

# Autenticación
auth = HTTPBasicAuth('admin', 'admin123')

# Crear categoría
response = requests.post(
    'http://localhost:8000/categorias/',
    json={
        'nombre': 'Helados Premium',
        'descripcion': 'Helados de alta calidad'
    },
    auth=auth
)
```

#### Usando Postman
1. En la pestaña "Authorization"
2. Seleccionar "Basic Auth"
3. Username: `admin`
4. Password: `admin123`

### Generar Credenciales Base64

Para generar el header Authorization manualmente:
```python
import base64

username = "admin"
password = "admin123"
credentials = f"{username}:{password}"
encoded = base64.b64encode(credentials.encode()).decode()
print(f"Authorization: Basic {encoded}")
# Resultado: Authorization: Basic YWRtaW46YWRtaW4xMjM=
```

## Seguridad

### Mejores Prácticas
1. **Cambiar contraseñas por defecto** antes de producción
2. **Usar HTTPS** en producción
3. **Rotar SECRET_KEY** regularmente
4. **Implementar rate limiting** para endpoints de autenticación
5. **Monitorear intentos de login fallidos**

### Estructura de Contraseñas
- Las contraseñas se almacenan hasheadas usando bcrypt
- Salt rounds: 12 (configurable)
- No se almacenan contraseñas en texto plano

## Troubleshooting

### Error 401 Unauthorized
- Verificar que las credenciales sean correctas
- Asegurar que el header Authorization esté presente
- Verificar que el usuario esté activo (`is_active = true`)

### Error 422 Validation Error
- Verificar el formato del JSON en requests POST/PUT
- Asegurar que todos los campos requeridos estén presentes

### Error 500 Internal Server Error
- Verificar que la base de datos esté corriendo
- Revisar que la tabla `usuarios` exista
- Verificar las variables de entorno

## Desarrollo

### Ejecutar la Aplicación
```bash
uvicorn main:app --reload
```

### Documentación Interactiva
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Testing
```bash
# Instalar dependencias de testing
pip install pytest httpx

# Ejecutar tests
pytest
```