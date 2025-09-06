from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

# Esquema base para usuario
class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    is_active: bool = True

# Esquema para crear usuario
class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6, max_length=100)

# Esquema para login
class UsuarioLogin(BaseModel):
    username: str
    password: str

# Esquema para respuesta de usuario
class UsuarioResponse(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    fecha_creacion: datetime

# Esquema para actualizar usuario
class UsuarioUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    is_active: Optional[bool] = None