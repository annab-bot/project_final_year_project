
from fastapi import FastAPI, File, UploadFile,Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image
import numpy as np
import tensorflow as tf
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from flask import Flask, render_template, request
from fastapi import FastAPI, Request, APIRouter,Depends,Form,HTTPException,Response
from connection import Base,engine, sess_db #quary executions 
from sqlalchemy.orm import Session
from scurity import get_password_hash, create_access_token
from scurity import get_password_hash, create_access_token,verify_token,verify_password,COOKIE_NAME
from starlette.responses  import RedirectResponse
from models import UserModel, BoneModel,DoctorModel # Model
from repositoryuser import UserRepository,SendEmailVerify,DoctorRepository  # Repository
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model("pc_models/1")
#endpoint = "http://localhost:8501/v1/models/potatoes_model:predict"

#CLASS_NAMES = ["Alpinia Galanga Rasna", "Amaranthus Viridis Arive Dantu", "Artocarpus Heterophyllus Jackfruit"]
CLASS_NAMES=["HARDDISK", "RAM", "cables", "cases", "keyboard"]


templates= Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory='static'),name='static')

Base.metadata.create_all(bind=engine) #db engin
@app.get("/",response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("dashboard.html",{"request":request})

@app.get("/pred",response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})


@app.get("/login",response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html",{"request":request})

@app.get("/pd",response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("Plant_Details.html",{"request":request})

@app.get("/mu",response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("Caution.html",{"request":request})


@app.get("/signup",response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("signup.html",{"request":request})
@app.get("/signin",response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html",{"request":request})
@app.post("/signinuser",response_class=HTMLResponse) #login Code
def signin_user(request: Request, response:Response,db:Session=Depends(sess_db),username : str = Form(),password:str=Form()):
    print(username)
    print(password)
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_username(username)
    if not db_user:
        return "username or password is not valid"
    
    if verify_password(password,db_user.password):
        token=create_access_token(db_user)
        response.set_cookie(
            key=COOKIE_NAME,
            value=token,
            httponly=True,
            expires=1800
        )
        return templates.TemplateResponse("dashboard.html",{"request":request})
        #response=RedirectResponse(url="/signin")
        return response
        #return {COOKIE_NAME:token}
    
    
@app.post("/signup_insert",response_class=HTMLResponse)
async def signup_insert(db:Session=Depends(sess_db),username: str=Form(),email:str=Form(),password:str=Form()):
    print(username)
    print(email)
    print(password)
    userRepository=UserRepository(db)
    db_user= userRepository.get_user_by_username(username)
    if db_user:
        return "username is Already Taken!"
    
    signup_insert=UserModel(email=email,username=username,password=get_password_hash(password))
    success=userRepository.create_user(signup_insert)
    token=create_access_token(signup_insert)
    SendEmailVerify.sendVerify(token)
    print(token)
    if success:
        return "created  user successfully"
    else:
        raise HTTPException(
            status_code=401, detail="Credentials not correct"
        )


    return "Registerd Successfully!"

@app.get("/doctor",response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("dr_details.html",{"request":request})

    
   

    return "Registerd Successfully!"


@app.get("/bone",response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("bone_info.html",{"request":request})

@app.post("/dr_insert",response_class=HTMLResponse)
async def dr_insert(db:Session=Depends(sess_db),email: str=Form(),username:str=Form(),mobileno:str=Form(),address:str=Form(),hospital_name:str=Form(),qualification:str=Form(), specialization:str=Form(), password:str=Form()):
    print(username)
    print(email)
    print(mobileno)
   
    dr_insert=DoctorModel(email=email,username=username,password=password,mobileno=mobileno,address=address,hospital_name=hospital_name,qualification=qualification,specialization=specialization)
    success=DoctorRepository.create_dr(dr_insert)
    #return "Registerd Successfully!"
    if success:
        return "created  Doctor successfully"
    else:
        return "Something Went Wrong"






@app.get('/verify/{token}')
def verify_user(token,db:Session=Depends(sess_db)):
     userRepository=UserRepository(db)
     payload=verify_token(token)
     username=payload.get("username")
     db_user=userRepository.get_user_by_username(username)
     if not username:
        raise  HTTPException(status_code=401, detail="Credentials not correct")
     if db_user.is_active==True:
         return "your account  has been allready activated"
 
     db_user.is_active=True
     db.commit()
     response=RedirectResponse(url="/signin")
     return response
    #http://127.0.0.1:8000/user/verify/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNseWRleTAxMzEiLCJlbWFpbCI6ImNseWRleUBnbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImFjdGl2ZSI6ZmFsc2V9.BKektCLzr47qn-fRtnGVulSdYlcMdemJQO_p32jWDk0

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict",response_class=HTMLResponse)
async def predict(
    request: Request,
    file: UploadFile = File(...)
):
    
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    
    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    #return HTMLResponse(predicted_class)
    percentage = f"{confidence:.0%}"
    print(img_batch)
    print(percentage)
    print(predicted_class)

    return templates.TemplateResponse("op.html",{"request":request,"a":predicted_class,'b':percentage,'c':img_batch})


    
    
if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8082)

