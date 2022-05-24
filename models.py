
from pydantic import BaseModel
from database import Base
from sqlalchemy import Column, ForeignKey, Identity,Integer,String,DateTime
from sqlalchemy.sql import func


class Producto(Base):
    __tablename__= 'producto'
    id= Column(Integer, primary_key=True, index=True)
    nombre=Column(String(250))
    precio=Column(Integer)
    url=Column(String(250))


class Sucursal(Base):
    __tablename__='sucursal'
    id= Column(Integer, primary_key=True, index=True)
    nombre=Column(String(250))


class ProductoSucursal(Base):
    __tablename__='productosucursal'
    idProducto=Column(Integer ,ForeignKey("producto.id"),primary_key=True)
    idSucursal=Column(Integer ,ForeignKey("sucursal.id"),primary_key=True)
    stockActual=Column(Integer)
    stockVendido=Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())



