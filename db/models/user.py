from typing import Optional
from pydantic import BaseModel

#MondoDB usa identificadores de cadena de textos
#Hacer opcional el id para que MongoDB genere el suyo
class ModelUser(BaseModel):
    id: Optional[str]
    userName: str
    email: str