from fastapi import FastAPI
from . import models
from .database import engine,get_db
import mysql.connector
from mysql.connector import errorcode
import time
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

# while True :
#     try :
#         conn= mysql.connector.connect(user="root",password="suman2003",host="localhost",database="todo")
#         cursor=conn.cursor(dictionary=True)
#         print("DATABASE CONNECTION WAS SUCCESSFULL!!")
#         break

#     except mysql.connector.Error as err :
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Something is wrong with your user name or password")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database does not exist")
#         else :
#             print(err)
#         time.sleep(3)
#     else :
#         conn.close()


@app.get("/")
def root() :
    return {"data" : "It is running properly"}