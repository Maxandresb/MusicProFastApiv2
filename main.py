from fastapi import Depends, FastAPI,HTTPException
from requests import session
from sqlalchemy.orm import Session
import json
import models
from schemas import ProductoSchemas, SucursalSchemas,ProductoSucursalSchemas
from database import engine,SessionLocal
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def obtener_productos( db:Session =Depends(get_db)):
    productos= db.query(models.Producto).all()

    return productos


@app.post('/productos/')
def agregar_producto(producto:ProductoSchemas, db:Session =Depends(get_db)):
    nuevo_producto= models.Producto(nombre=producto.nombre, precio=producto.precio)
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto


@app.post('/sucursales/')
def agregar_sucursal(sucursal:SucursalSchemas, db:Session =Depends(get_db)):
    nuevo_sucursal= models.Sucursal(nombre=sucursal.nombre)
    db.add(nuevo_sucursal)
    db.commit()
    db.refresh(nuevo_sucursal)
    return nuevo_sucursal

@app.post('/stock/')
def agregar_stock(stock:ProductoSucursalSchemas, db:Session =Depends(get_db)):
    nuevo_stock= models.ProductoSucursal(idProducto=stock.idProducto, idSucursal=stock.idSucursal,stockActual=stock.stockActual, stockVendido=stock.stockVendido)
    db.add(nuevo_stock)
    db.commit()
    db.refresh(nuevo_stock)
    return nuevo_stock


@app.get('/productos/{id}')
async def obtener_stock(id:int,  db:Session =Depends(get_db)):
    # producto= db.query(models.Producto).filter(models.Producto.id ==id).first()
    stock= db.query(models.ProductoSucursal).filter(models.ProductoSucursal.idProducto==id).all()
    
    sucursales=[]
    for s in stock:
        sucursal= db.query(models.Sucursal).filter(models.Sucursal.id==s.idSucursal).first()
        # print(sucursal.nombre)
        json={"Sucursal":sucursal.nombre,"Stock":s.stockActual}
        sucursales.append(json)
    return sucursales



@app.put('/productos/')
async def actualizar_stock( stock:ProductoSucursalSchemas, db:Session =Depends(get_db)):
    stockProducto:models.ProductoSucursal=db.query(models.ProductoSucursal).filter(models.ProductoSucursal.idProducto==stock.idProducto, models.ProductoSucursal.idSucursal==stock.idSucursal).first()
    stockProducto.stockActual=stock.stockActual
    stockProducto.stockVendido=stock.stockVendido
    
    db.commit()
    return {"message":"ok"}

    


    