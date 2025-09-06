from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Producto(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    sabor = Column(String(50), nullable=False)
    descripcion = Column(Text)
    precio = Column(Numeric(10, 2), nullable=False)
    precio_mayorista = Column(Numeric(10, 2))
    cantidad_minima_mayorista = Column(Integer, default=10)
    stock = Column(Integer, default=0, nullable=False)
    imagen_url = Column(String(500), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relación con categoría
    categoria = relationship("Categoria", back_populates="productos")
    
    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio})>"
    
    def calcular_precio(self, cantidad: int) -> float:
        """Calcula el precio basado en la cantidad solicitada"""
        if (self.precio_mayorista and 
            self.cantidad_minima_mayorista and 
            cantidad >= self.cantidad_minima_mayorista):
            return float(self.precio_mayorista)
        return float(self.precio)