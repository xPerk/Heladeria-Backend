from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.schemas.categoria import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaResponse,
    CategoriaWithProductos
)
from app.auth.dependencies import get_current_active_user

router = APIRouter(
    prefix="/categorias",
    tags=["categorias"]
)


@router.get("/", response_model=List[CategoriaResponse])
def obtener_categorias(
    skip: int = 0,
    limit: int = 100,
    activo: bool = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de categorías con paginación y filtros"""
    query = db.query(Categoria)
    
    if activo is not None:
        query = query.filter(Categoria.activo == activo)
    
    categorias = query.offset(skip).limit(limit).all()
    return categorias


@router.get("/{categoria_id}", response_model=CategoriaWithProductos)
def obtener_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una categoría específica por ID con sus productos"""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    
    return categoria


@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear una nueva categoría"""
    # Verificar si ya existe una categoría con el mismo nombre
    categoria_existente = db.query(Categoria).filter(
        Categoria.nombre == categoria.nombre
    ).first()
    
    if categoria_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una categoría con el nombre '{categoria.nombre}'"
        )
    
    db_categoria = Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    
    return db_categoria


@router.put("/{categoria_id}", response_model=CategoriaResponse)
def actualizar_categoria(
    categoria_id: int,
    categoria_update: CategoriaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar una categoría existente"""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    
    # Verificar nombre único si se está actualizando
    if categoria_update.nombre and categoria_update.nombre != categoria.nombre:
        categoria_existente = db.query(Categoria).filter(
            Categoria.nombre == categoria_update.nombre,
            Categoria.id != categoria_id
        ).first()
        
        if categoria_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una categoría con el nombre '{categoria_update.nombre}'"
            )
    
    # Actualizar campos
    update_data = categoria_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(categoria, field, value)
    
    db.commit()
    db.refresh(categoria)
    
    return categoria


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Eliminar una categoría (soft delete - marcar como inactiva)"""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    
    # Verificar si tiene productos activos
    productos_activos = any(producto.activo for producto in categoria.productos)
    
    if productos_activos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar la categoría porque tiene productos activos asociados"
        )
    
    # Soft delete - marcar como inactiva
    categoria.activo = False
    db.commit()
    
    return None


@router.patch("/{categoria_id}/activar", response_model=CategoriaResponse)
def activar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Activar una categoría inactiva"""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    
    categoria.activo = True
    db.commit()
    db.refresh(categoria)
    
    return categoria