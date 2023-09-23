from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()

#JWT: JSON Web Token

#Para utilizar el token jwt se necesita instalar lo siguiente:
#pip install python-jose[cryptography]

#Para trabajar con hasehs se necesita instalar lo siguiente:
#pip install passlib[bcrypt]


#Algoritmo de incriptación
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
SECRET_KEY = "cceab5263bcc761ce400f36e126777706beb98c545d624f6657d5150017be846"
#Para obtener un string con la secret key se debe ejecutar lo siguiente:
#openssl rand -hex 32

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        "password": "$2a$12$/QK3OUFcqiQ7Pfd9YFsh.O/xhWcjXQn8iLe6Al0WsQYPb/8Ybimd."
    },
    "JC" : {
        "username": "JC",
        "full_name": "JC Chosi",
        "email": "JC@Hotmail.com",
        "disabled": True,
        "password": "$2a$12$imxqBn4cCFRWz6H3fyucguStfl6wpgtDYb/wi/fOpFXNR7vF/aav."
    }
}

#Búsqueda del usuario sin la contraseña 
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) #** es para pasar un diccionario como parámetro
    else:
        return None
    
#Búsqueda del usuario para el login donde necesaremos la contraseña
def search_userDB(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) #** es para pasar un diccionario como parámetro
    else:
        return None

async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid authentication credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")

        if username is None:
            raise exception
        
    except jwt.JWTError:        
        raise exception 

    return search_user(username)
    

async def get_current_user(user: UserDB = Depends(auth_user)):
    user = search_user(user.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid authentication credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Inactive user")
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    
    user = search_userDB(form.username)

    #Verifica que la contraseña sea correcta
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    
    #Un delta con ACCESS_TOKEN_EXPIRE_MINUTES más del momento actual de acceso
    acces_token = {"sub": user.username, 
                   "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}


    return {"access_token": jwt.encode(acces_token, SECRET_KEY , algorithm=ALGORITHM), 
            "token_type": "bearer"}

#Recupera el usuario actual
@router.get("/users/me")
async def current_user(user: User = Depends(get_current_user)): 
    return user




