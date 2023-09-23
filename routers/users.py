from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users",
                   responses={404: {"message": "Not found"}},
                   tags=["users"])

class ModelUser(BaseModel):
    id: int
    name: str
    last_name: str
    age: int   
    email: str

user_list = [ModelUser(id=1,name="Juan",last_name="del",age=30,email="http://localhost:8000/users/1"),
             ModelUser(id=2,name="Carlos",last_name="Agua",age=32,email="http://localhost:8000/users/2"),
             ModelUser(id=3,name="Teren",last_name="Stardust",age=24,email="http://localhost:8000/users/3"),
             ModelUser(id=4,name="Teren",last_name="Chopi",age=24,email="http://localhost:8000/users/4")
            ]

####################
#   CRUD USERS     #
####################

#GETTERS
@router.get("/users")
async def getUsers():
   return user_list

#Suele usarse cuando un parámetro es obligatorio
@router.get("/user/{id}")
async def getUser(id:int):
   return search_user(id)
    
#Suele usarse cuando un parámetro es opcional
@router.get("/user/")
async def getUser(id:int):
    return search_user(id)
        
#CREATE
@router.post("/user/",status_code=201) 
async def createUser(user:ModelUser):
    if type(search_user(user.id)) == ModelUser:
        raise HTTPException(status_code=409, detail="User already exists")

    user_list.routerend(user)
    return user_list

#UPDATES
@router.put("/user/")
async def updateUser(user:ModelUser):
    if type(search_user(user.id)) != ModelUser:
        raise HTTPException(status_code=404, detail="User not found")    
    try:
        user_list[user.id-1] = user
        return user_list
    except:
        return {"message":"UPDATE Error - Not defined"}



#DELETE
@router.delete("/user/{id}")
async def deleteUser(id:int):
    if type(search_user(id)) != ModelUser:
        raise HTTPException(status_code=404, detail="User not found") 
    
    try:
        user_list.remove(search_user(id))
        return user_list
    except:
        return {"message":"DELETE Error - Not defined"}
        

#Busca un usuario por id
def search_user(id: int):
    users = filter(lambda user: user.id == id, user_list) #Obtiene, de la lista, el usuario con el id que se le pasa
    try:
        return list(users)[0] #Convierte el filtro en una lista y obtiene el primer elemento
    except:
        return {"message":"User not found - search_user"} 