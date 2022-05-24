from pydantic import BaseModel

class ProductoSchemas(BaseModel):
    
    nombre:str
    precio:int
    url:str

class SucursalSchemas(BaseModel):
    nombre:str


class ProductoSucursalSchemas(BaseModel):
    idProducto:int
    idSucursal:int
    stockActual:int
    stockVendido:int