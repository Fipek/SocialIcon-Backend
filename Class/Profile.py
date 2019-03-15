# -*- coding: utf-8 -*-
import json,base64
from datetime import datetime
import Constant,ErrorMessages
#------------------ENUM Definations------------------
USER_ID_ROW = 0
FULL_NAME_ROW = 1
USER_NAME_ROW = 2
PICTURE_ROW = 3
#---------------------------------------------------- 

class Profile(object):
	
    def __init__(self):
        self.user_id = ""
        self.full_name = ""
        self.user_name = ""
        self.picture = ""
        self.offer_count = ""
        self.offer_obj_list = ""
    
    def Deserialize(self,json_object):
        self.__dict__ = json_object
        if hasattr(self, 'user_id'):
            return self.EmptyControl()
        else:
            return self.EmptyControlSign()
        
    def SetVariablesWithRules(self):
        self.full_name = base64.b64decode(self.full_name).decode('utf-8').strip()
        if hasattr(self, 'user_id'):
            self.user_name = base64.b64decode(self.user_name).decode('utf-8').strip()
        else:
            self.user_name = "Guest"+str(datetime.now())
        
    def EmptyControl(self):
        if self.full_name is None or self.full_name == "":
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'2001', 'Message': ErrorMessages.Message['2001']})
        if self.user_name is None or self.user_name == "":
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1006', 'Message': ErrorMessages.Message['1006']})
        return Constant.OK
      
    def EmptyControlSign(self):
        if self.full_name is None or self.full_name == "":
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'2001', 'Message': ErrorMessages.Message['2001']})
        return Constant.OK

    def SetFromDb(self,profile):# Databaseden veri çekerken
        self.user_id = profile[USER_ID_ROW]
        self.full_name = profile[FULL_NAME_ROW]
        self.user_name = profile[USER_NAME_ROW]
        if profile[PICTURE_ROW] == None:
            self.picture = "/user.png"
        else:
            self.picture = str(Constant.PROFILE_IMAGE_CLIENT) + str(profile[PICTURE_ROW])

    def ToJson(self):
    	return  {'user_id' : self.user_id,
               'full_name' : self.full_name,
               'user_name' : self.user_name,
               'picture' : self.picture,
               'offer_count' : self.offer_count,  
               'offer_list' : self.offer_obj_list
              }

    def ToJsonPreview(self):
    	return  {'user_id' : self.user_id,
               'full_name' : self.full_name,
               'user_name' : self.user_name,
               'picture' : self.picture
              }
