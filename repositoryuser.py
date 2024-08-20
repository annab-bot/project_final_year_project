#loginregister/repositoryuser.py
from sqlalchemy.orm import Session
from models import UserModel,DoctorModel
from typing import  Dict,Any

import smtplib
from email.message import EmailMessage
 
class UserRepository:
    def __init__(self,sess:Session):
        self.sess: Session=sess
 
    def create_user(self,signup_insert:UserModel) -> bool:
         try:
             self.sess.add(signup_insert)
             self.sess.commit()
         except:
             return False
         return True
    
class DoctorRepository:
    def __init__(self,sess:Session):
        self.sess: Session=sess
 
    def create_dr(self,dr_insert:DoctorModel) -> bool:
         try:
             self.sess.add(dr_insert)
             self.sess.commit()
         except:
             return False
         return True
    
    def get_user(self):
        return  self.sess.query(UserModel).all()
 
    def get_user_by_username(self,username:str):
        return self.sess.query(UserModel).filter(UserModel.username==username).first()
    
class SendEmailVerify:
 
  def sendVerify(token):
    email_address = "zaheer.myvertex@gmail.com" # type Email
    email_password = "twxldmnfdchplgyr" # If you do not have a gmail apps password, create a new app with using generate password. Check your apps and passwords https://myaccount.google.com/apppasswords

    # create email
    msg = EmailMessage()
    msg['Subject'] = "Verify Mail by clik on link "
    msg['From'] = email_address
    msg['To'] = "dhanashakerchotu66@gmail.com" # type Email
    msg.set_content(
       f"""\
    verify account        
    http://localhost:2023/verify/{token}
    """,
         
    )
    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)