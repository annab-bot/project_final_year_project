#loginregister/models.py
from sqlalchemy import Column,String,Integer,Boolean,Enum
from schema import Roles
from connection import  Base
 
class UserModel(Base):
    __tablename__ = "users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,index=True)
    username=Column(String,unique=True,index=True)
    password=Column(String,unique=False,index=True)
    is_active=Column(Boolean,default=False)
    role=Column(Enum(Roles),default="user")


class DoctorModel(Base):
    __tablename__ = "doctors"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,index=True)
    username=Column(String,unique=True,index=True)
    password=Column(String,unique=False,index=True)
    mobileno=Column(Integer,unique=False,index=True)
    address=Column(String,unique=False,index=True)
    hospital_name=Column(String,unique=False,index=True)
    qualification=Column(String,unique=False,index=True)
    specialization=Column(String,unique=False,index=True)
    
    


class BoneModel(Base):
    __tablename__ = "bone"
    id=Column(Integer,primary_key=True,index=True)
    cause=Column(String,unique=True,index=True)
    symptom=Column(String,unique=False,index=True)
    part_of_fractured=Column(Integer,unique=False,index=True)
    last_test_details=Column(String,unique=False,index=True)
















