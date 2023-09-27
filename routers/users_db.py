### USERS DB API ###
from fastapi import APIRouter, HTTPException, status
from db.models.user import ModelUser
from db.schemas.user import schema_user, schema_users
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
                   tags=["usersdb"])


user_list = []

####################
#   CRUD USERS     #
####################

#GETTERS
@router.get("/", response_model=list[ModelUser])
async def getUsers():
   return schema_users(db_client.users.find())

#Suele usarse cuando un parámetro es obligatorio
@router.get("/{id}")
async def getUser(id:str):
   return search_user("_id", ObjectId(id))
    
#Suele usarse cuando un parámetro es opcional
@router.get("/")
async def getUser(id:str):
    return search_user("_id", ObjectId(id))
        
#CREATE
@router.post("/", response_model=ModelUser, status_code=status.HTTP_201_CREATED,) 
async def createUser(user:ModelUser):
    user_dict = dict(user)
    del user_dict["id"] #Borrar el id para que MongoDB lo genere

    id = db_client.users.insert_one(user_dict).inserted_id

    #MondoDB crea el identificador con _id
    new_user = schema_user(db_client.users.find_one({"_id":id}))

    return ModelUser(**new_user)

#UPDATES
@router.put("/")
async def updateUser(user:ModelUser):
    
    
    # if type(search_user("_id", ObjectId(user.id))) != ModelUser:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail="User not found")    
    
    try:
        id = ModelUser(**schema_user(db_client.users.find_one({"email":user.email}))).id
        user_dict = dict(user)
        #del user_dict["id"]
        db_client.users.find_one_and_replace({"_id":ObjectId(id)}, 
                                                   user_dict)
       
        
        return search_user("_id", ObjectId(user.id))
    except:
        return {"message":"UPDATE Error - Not defined"}


#DELETE
@router.delete("/{id}")
async def deleteUser(id:str, status_code=status.HTTP_204_NO_CONTENT):
    
    try:
        found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})

        if not found:
            return {"message":"User not found"}

    except:
        return {"message":"DELETE Error - Not defined"}
        

#Busca un usuario por id
def search_user(key: str, value: str | ObjectId | int):
    try:
        return ModelUser(**schema_user(db_client.users.find_one({key:value})))
    except:
        return None
    

async def create_user(username: str, email: str):
    try:
        if search_user("email", email) != None:
            return HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                 detail="User already exists")
            # raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            #                     detail="User already exists")
        
        user: ModelUser = get_user(username, email)
        await createUser(user)
    except:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                 detail="Error creating user")
    
async def update_user(username: str, email: str):
    try:
        if search_user("email", email) == None:
            return HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                 detail="User not exists")
        user: ModelUser = get_user(username, email)
        await updateUser(user)
    except:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                 detail="Error updating user")

async def delete_user(username: str):
    try:
        user = search_user("userName", username)
        if user == None:
            return HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                 detail="User not exists")
        await deleteUser(user.id)
    except:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                 detail="Error deleting user")  

def get_user(username: str, email: str):
   return  {"id":0,"userName": username, "email":email}