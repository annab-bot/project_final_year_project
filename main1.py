from fastapi import FastAPI, File, UploadFile,Request
import uvicorn
from io import BytesIO
from PIL import Image
import numpy as np
import tensorflow as tf
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from flask import Flask, render_template, request

app=FastAPI()
app.mount("/static", StaticFiles(directory="static"),name="static")
templates= Jinja2Templates(directory="templates")
@app.get("/",response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})
    #return "Hello I am Working"
@app.post("/predict")
async def predict(
    file: UploadFile = File(...)):
      
    
      print(file.filename)
      
      
      return{
           "file":file.filename
      }
      
      pass
    
    
    
if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=2023)
