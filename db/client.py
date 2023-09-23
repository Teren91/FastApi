### MongoDB Client ###
from pymongo import MongoClient

#Conexión localhost:27017
#db_client = MongoClient().local

#BBDD remota
db_client = MongoClient(
    "mongodb+srv://admin:admin@cluster0.2pkcqkl.mongodb.net/?retryWrites=true&w=majority").test

#mongodb+srv://admin:admin@cluster0.2pkcqkl.mongodb.net/admin