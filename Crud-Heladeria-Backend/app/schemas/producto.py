from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

# Esquema base para producto
class ProductoBase(BaseModel):
    nombre: str
    sabor: str
    descripcion: Optional[str] = None
    precio: float = Field(gt=0)
    precio_mayorista: Optional[float] = Field(None, gt=0)
    cantidad_minima_mayorista: Optional[int] = Field(default=10, gt=0)
    stock: int = Field(default=0, ge=0)
    categoria_id: int
    activo: bool = True

# Esquema para crear producto
class ProductoCreate(ProductoBase):
    pass

# Esquema para actualizar producto
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    sabor: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(None, gt=0)
    precio_mayorista: Optional[float] = Field(None, gt=0)
    cantidad_minima_mayorista: Optional[int] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    categoria_id: Optional[int] = None
    activo: Optional[bool] = None

# Esquema para respuesta de producto
class ProductoResponse(ProductoBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

# Esquema para producto con categoría
class ProductoWithCategoria(ProductoResponse):
    categoria: 'CategoriaResponse'


class ProductoPrecioCalculado(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float
    precio_total: float
    es_precio_mayorista: bool


# Importar después para evitar importación circular
from app.schemas.categoria import CategoriaResponse
ProductoWithCategoria.model_rebuild()