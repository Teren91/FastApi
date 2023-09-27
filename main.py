from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles


#Inicializar el servidor virtual - uvicorn main:app --reload

app = FastAPI(title="FastAPI - Curso", description="API de ejemplo", version="1.0.0"
              ,openapi_tags=[{"name":"users","description":"Operaciones con usuarios"},
                             {"name":"products","description":"Operaciones con productos"},
                            ])
#Inicial el servidor virtual - uvicorn main:app --reload

#Routers
app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

app.include_router(users_db.router)

#Exponer recursos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get("/") #Raíz de la IP donde se despliega la API
async def root():
    return "¡Hola FastApi!"

@app.get("/url")
async def url():
    return {"url_curso":"http://127.0.0.1:8000/"}
        
@app.get("/items/{item_id}")
async def read_item(item_id: int ):
    return {"item_id": item_id}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


    