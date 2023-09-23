from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str   
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "Teren" : {
        "username": "Teren",
        "full_name": "Teren Stardust",
        "email": "Teren@Hotmail.com",
        "disabled": False,
        "password": "1234"
    },
    "JC" : {
        "username": "JC",
        "full_name": "JC Chosi",
        "email": "JC@Hotmail.com",
        "disabled": True,
        "password": "4321"
    }
}

async def get_current_user(token: str = Depends(oauth2)):
    user = search_userDB(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid authentication credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Inactive user")
    return user

#Busca el usuario directamente en la clase UserDB
def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) #** es para pasar un diccionario como parámetro
    else:
        return None

def search_userDB(username: str):
    if username in users_db:
        return User(**users_db[username]) #** es para pasar un diccionario como parámetro
    else:
        return None

#Recupera el usuario actual
@router.get("/users/me")
async def current_user(user: User = Depends(get_current_user)): 
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    
    user = search_user(form.username)

    if form.password != user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    
    return {"access_token": user.username, "token_type": "bearer"}



