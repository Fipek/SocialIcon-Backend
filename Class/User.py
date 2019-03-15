# -*- coding: utf-8 -*-
import json,base64,bcrypt
from datetime import datetime
import Constant
#------------------ENUM Definations------------------
ID_ROW = 0
EMAIL_ROW = 1
PHONE_ROW = 2
FULL_NAME_ROW = 3
USER_NAME_ROW = 4
PICTURE_ROW = 5
#---------------------------------------------------- 

class User(object):
	
    def __init__(self):
        self.id =""
        self.email_adress = ""
        self.phone = ""
        self.full_name = ""
        self.user_name = ""
        self.picture = ""
    
    def Deserialize(self,json_object):
        self.__dict__ = json_object
        
    def SetVariablesWithRules(self):
        self.full_name = base64.b64decode(self.full_name).decode('utf-8').strip()
        self.user_name = "Guest"+str(datetime.now())
        self.password = bcrypt.hashpw(self.password.encode('utf8'), bcrypt.gensalt())

    def SetFromDb(self,user_list):# Databaseden veri çekerken
        self.id = user_list[ID_ROW]
        self.email_adress = user_list[EMAIL_ROW]
        self.phone = user_list[PHONE_ROW]
        self.full_name = user_list[FULL_NAME_ROW]
        self.user_name = user_list[USER_NAME_ROW]
        if user_list[PICTURE_ROW] == None:
            self.picture = "/user.png"
        else:
            self.picture = str(Constant.PROFILE_IMAGE_CLIENT) + str(user_list[PICTURE_ROW])

    def ToJson(self):
        print self.picture
        return  {'id' : self.id,
                'email_adress' : self.email_adress,
                'phone' : self.phone,
                'full_name' : self.full_name,
                'user_name' : self.user_name,  
                'picture' : self.picture
               }
