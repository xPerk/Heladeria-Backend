from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

from app.database.database import get_db
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.schemas.producto import (
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse,
    ProductoWithCategoria,
    ProductoPrecioCalculado
)
from app.auth.dependencies import get_current_active_user

router = APIRouter(
    prefix="/productos",
    tags=["productos"]
)


@router.get("/", response_model=List[ProductoWithCategoria])
def obtener_productos(
    skip: int = 0,
    limit: int = 100,
    activo: Optional[bool] = None,
    categoria_id: Optional[int] = None,
    con_precio_mayorista: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de productos con filtros y paginación"""
    query = db.query(Producto)
    
    if activo is not None:
        query = query.filter(Producto.activo == activo)
    
    if categoria_id is not None:
        query = query.filter(Producto.categoria_id == categoria_id)
    
    if con_precio_mayorista is not None:
        if con_precio_mayorista:
            query = query.filter(
                Producto.precio_mayorista.isnot(None),
                Producto.cantidad_minima_mayorista.isnot(None)
            )
        else:
            query = query.filter(
                Producto.precio_mayorista.is_(None)
            )
    
    productos = query.offset(skip).limit(limit).all()
    return productos


@router.get("/{producto_id}", response_model=ProductoWithCategoria)
def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un producto específico por ID"""
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    return producto


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear un nuevo producto"""
    # Verificar que la categoría existe
    categoria = db.query(Categoria).filter(Categoria.id == producto.categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Categoría con ID {producto.categoria_id} no encontrada"
        )
    
    # Verificar que la categoría esté activa
    if not categoria.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede crear un producto en una categoría inactiva"
        )
    
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    
    return db_producto


@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int,
    producto_update: ProductoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar un producto existente"""
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    # Verificar categoría si se está actualizando
    if producto_update.categoria_id:
        categoria = db.query(Categoria).filter(
            Categoria.id == producto_update.categoria_id
        ).first()
        
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Categoría con ID {producto_update.categoria_id} no encontrada"
            )
        
        if not categoria.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede asignar el producto a una categoría inactiva"
            )
    
    # Actualizar campos
    update_data = producto_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(producto, field, value)
    
    db.commit()
    db.refresh(producto)
    
    return producto


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Eliminar un producto (soft delete - marcar como inactivo)"""
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    # Soft delete - marcar como inactivo
    producto.activo = False
    db.commit()
    
    return None


@router.patch("/{producto_id}/activar", response_model=ProductoResponse)
def activar_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Activar un producto inactivo"""
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    producto.activo = True
    db.commit()
    db.refresh(producto)
    
    return producto


@router.patch("/{producto_id}/stock", response_model=ProductoResponse)
def actualizar_stock(
    producto_id: int,
    nuevo_stock: int = Query(..., ge=0, description="Nueva cantidad en stock"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar el stock de un producto"""
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    producto.stock = nuevo_stock
    db.commit()
    db.refresh(producto)
    
    return producto


@router.get("/{producto_id}/precio", response_model=ProductoPrecioCalculado)
def calcular_precio_producto(
    producto_id: int,
    cantidad: int = Query(..., gt=0, description="Cantidad a calcular"),
    db: Session = Depends(get_db)
):
    """Calcular el precio de un producto basado en la cantidad"""
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    precio_unitario = Decimal(str(producto.calcular_precio(cantidad)))
    precio_total = precio_unitario * cantidad
    
    es_precio_mayorista = (
        producto.precio_mayorista is not None and
        producto.cantidad_minima_mayorista is not None and
        cantidad >= producto.cantidad_minima_mayorista
    )
    
    return ProductoPrecioCalculado(
        producto_id=producto_id,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        precio_total=precio_total,
        es_precio_mayorista=es_precio_mayorista
    )


@router.get("/mayorista/disponibles", response_model=List[ProductoWithCategoria])
def obtener_productos_mayorista(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener productos que tienen precio mayorista configurado"""
    productos = db.query(Producto).filter(
        Producto.activo == True,
        Producto.precio_mayorista.isnot(None),
        Producto.cantidad_minima_mayorista.isnot(None)
    ).offset(skip).limit(limit).all()
    
    return productos


@router.get("/categoria/{categoria_id}", response_model=List[ProductoResponse])
def obtener_productos_por_categoria(
    categoria_id: int,
    activo: bool = True,
    db: Session = Depends(get_db)
):
    """Obtener todos los productos de una categoría específica"""
    # Verificar que la categoría existe
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    
    query = db.query(Producto).filter(Producto.categoria_id == categoria_id)
    
    if activo is not None:
        query = query.filter(Producto.activo == activo)
    
    productos = query.all()
    return productos