# -*- coding: utf-8 -*-
import json,base64,bcrypt
import Constant,ErrorMessages
#------------------ENUM Definations------------------
USER_ID_ROW = 0
TOKEN_ID_ROW = 0
IP_ADRESS_ID_ROW = 0
USER_AGENT_ID_ROW = 0
CREATE_DATE_ID_ROW = 0
#---------------------------------------------------- 

class Session(object):
	
    def __init__(self):
        self.user_id =""
        self.token = ""
        self.ip_adress = ""
        self.user_agent = ""
        self.create_date = ""
    
    def Deserialize(self,json_object):
        self.__dict__ = json_object
        #return self.EmptyControl()
        
    def SetVariablesWithRules(self):
        pass
        
    def EmptyControl(self):
        if self.email_adress is None or self.email_adress == "":
             return({'Status': Constant.ERROR, 'Data':'', 'Code':'1007', 'Message': ErrorMessages.Message['1007']})
        return Constant.OK

    def SetFromDb(self,post):# Databaseden veri çekerken
        pass
        """self.post_id = post[POST_ID_ROW]
        self.title = post[TITLE_ROW]
        self.date = post[DATE_ROW]
        self.quill_obj = post[QUILL_OBJ_ROW]
        self.picture = post[PIC_PATH_ROW]
        self.is_private = post[IS_PRIVATE]
        self.view_count = post[VIEW_COUNT]"""

    def ToJson(self):
    	return  {'  user_id' : self.user_id,
                 'token' : self.token,
                 'ip_adress' : self.ip_adress,
                 'user_agent' : self.user_agent,
                 'create_date' : self.create_date
                 }
