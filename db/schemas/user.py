### SCHEMA USERS API ###


#Se recibe un objeto de tipo usuario y se devuelve un diccionario
def schema_user(user) -> dict:
    return {
        "id": str(user["_id"]), 
        "userName": user["userName"],
        "email": user["email"]
    }

def schema_users(users) -> list:
    return [schema_user(user) for user in users]
        