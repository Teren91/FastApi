from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

#Indicar un prefijo para la ruta, de modo que en la ruta principal no se tenga que indicar
router = APIRouter(prefix="/products", 
                   responses={404: {"message": "Not found"}},
                   tags=["products"])

class ModelProduct(BaseModel):
    id: int
    prduct: str
    price: int   
    image: str

product_list = [ModelProduct(id=1,prduct="Pantalla",price=150,image="http://localhost:8000/products/1"),
             ModelProduct(id=2,prduct="Ratón",price=30,image="http://localhost:8000/products/2"),
             ModelProduct(id=3,prduct="Teclado",price=60,image="http://localhost:8000/products/3"),
             ModelProduct(id=4,prduct="Portátil",price=800,image="http://localhost:8000/products/4")
            ]

####################
#   CRUD productS     #
####################

#GETTERS
@router.get("/")
async def getproducts():
   return product_list

#Suele usarse cuando un parámetro es obligatorio
@router.get("/{id}")
async def getproduct(id:int):
   return search_product(id)
    
#Suele usarse cuando un parámetro es opcional
@router.get("/")
async def getproduct(id:int):
    return search_product(id)
        
#CREATE
@router.post("/",status_code=201) 
async def createproduct(product:ModelProduct):
    if type(search_product(product.id)) == ModelProduct:
        raise HTTPException(status_code=409, detail="product already exists")

    product_list.routerend(product)
    return product_list

#UPDATES
@router.put("/")
async def updateproduct(product:ModelProduct):
    if type(search_product(product.id)) != ModelProduct:
        raise HTTPException(status_code=404, detail="product not found")    
    try:
        product_list[product.id-1] = product
        return product_list
    except:
        return {"messprice":"UPDATE Error - Not defined"}



#DELETE
@router.delete("/product/{id}")
async def deleteproduct(id:int):
    if type(search_product(id)) != ModelProduct:
        raise HTTPException(status_code=404, detail="product not found") 
    
    try:
        product_list.remove(search_product(id))
        return product_list
    except:
        return {"messprice":"DELETE Error - Not defined"}
        

#Busca un usuario por id
def search_product(id: int):
    products = filter(lambda product: product.id == id, product_list) #Obtiene, de la lista, el usuario con el id que se le pasa
    try:
        return list(products)[0] #Convierte el filtro en una lista y obtiene el primer elemento
    except:
        return {"messprice":"product not found - search_product"} 