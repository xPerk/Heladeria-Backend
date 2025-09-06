from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Importar routers
from app.routers import categorias, productos, auth

# Importar modelos para crear las tablas
from app.models import categoria, producto, usuario
from app.database.database import engine, Base

# Cargar variables de entorno
load_dotenv()

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title=os.getenv("APP_NAME", "Heladeria API"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="API REST para gestión de heladería con sistema de precios mayoristas",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(categorias.router, prefix="/api/v1")
app.include_router(productos.router, prefix="/api/v1")


# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor",
            "message": str(exc) if os.getenv("DEBUG", "False").lower() == "true" else "Error interno"
        }
    )


# Endpoint de salud
@app.get("/health")
def health_check():
    """Endpoint para verificar el estado de la API"""
    return {
        "status": "healthy",
        "message": "API funcionando correctamente",
        "version": os.getenv("APP_VERSION", "1.0.0")
    }


# Endpoint raíz
@app.get("/")
def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Bienvenido a la API de Heladería",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# Endpoint de información de la API
@app.get("/api/v1/info")
def api_info():
    """Información detallada de la API"""
    return {
        "name": os.getenv("APP_NAME", "Heladeria API"),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "description": "API REST para gestión de heladería con sistema de precios mayoristas",
        "endpoints": {
            "categorias": "/api/v1/categorias",
            "productos": "/api/v1/productos",
            "productos_mayorista": "/api/v1/productos/mayorista/disponibles"
        },
        "features": [
            "CRUD completo para categorías",
            "CRUD completo para productos",
            "Sistema de precios mayoristas",
            "Cálculo automático de precios por cantidad",
            "Gestión de stock",
            "Filtros y paginación",
            "Soft delete (eliminación lógica)"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )