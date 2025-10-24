from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Comercio(Base):
    __tablename__ = "comercios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    tipo = Column(String)
    direccion = Column(String)
    latitud = Column(Float)
    longitud = Column(Float)
    telefono = Column(String)
    email = Column(String)
    horario = Column(String)
    
    promociones = relationship("Promocion", back_populates="comercio", cascade="all, delete-orphan")

class Promocion(Base):
    __tablename__ = "promociones"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    precio = Column(Float)
    categoria = Column(String)
    comercio_id = Column(Integer, ForeignKey("comercios.id"))
    
    comercio = relationship("Comercio", back_populates="promociones")
