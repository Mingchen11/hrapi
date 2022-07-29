from asyncio.windows_events import NULL
from telnetlib import STATUS
from typing_extensions import Self
from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

class Register(BaseModel):
    User_name: str
    User_email: str
    User_password: str
    User_firstname: str
    User_middlename: str
    User_lastname: str
    User_phone: str

class Signin(BaseModel):
    user_name: str
    user_password: str 

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='hr_login', user='postgres', password='#DbPostgre911&', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)

def email(user_email):
    pass

@app.get("/admin")
def get_admin():
    cursor.execute("""SELECT * FROM admin""")
    admin= cursor.fetchall()
    return {"data": admin}

@app.post("/signup")
def post_admin(admindata: Register):
    cursor.execute("""SELECT user_email, user_name FROM admin""")
    user = cursor.fetchall()

    email(admindata.User_email)

    for i in range(len(user)):
        for j in range(len(user[i])):
            if admindata.User_email in user[i].values() or admindata.User_name in user[i].values():
                return {"Error": "User with this email or user name already exist"}
        

    cursor.execute("""INSERT INTO admin(user_name, user_firstname, user_middlename, user_lastname, user_password, user_email, user_phone) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING * """,(admindata.User_name, admindata.User_firstname, admindata.User_middlename, admindata.User_lastname, admindata.User_password, admindata.User_email, admindata.User_phone))
    admin = cursor.fetchone()

    conn.commit()
    return{"data": admin}
    
    


@app.get("/signin")
def get_admin(admindata: Signin):
    cursor.execute("""SELECT user_password from admin WHERE user_name = %s""", (admindata.user_name,))
    admin= cursor.fetchone()
    print(admin)
    if not admin:
        return {f"account with user name: {admindata.user_name} was not found. Do you want to create an account?"}
       
    
    if admindata.user_password not in admin.values():
        return{"Password Error."}
        
    return {"Login Successful."}
