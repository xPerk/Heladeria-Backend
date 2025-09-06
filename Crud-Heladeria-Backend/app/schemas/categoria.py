from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# Esquema base para categoría
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True

# Esquema para crear categoría
class CategoriaCreate(CategoriaBase):
    pass

# Esquema para actualizar categoría
class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

# Esquema para respuesta de categoría
class CategoriaResponse(CategoriaBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    fecha_creacion: datetime

# Esquema para categoría con productos
class CategoriaWithProductos(CategoriaResponse):
    productos: List['ProductoResponse'] = []

# Importar después para evitar importación circular
from .producto import ProductoResponse
CategoriaWithProductos.model_rebuild()