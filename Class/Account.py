# -*- coding: utf-8 -*-
import json,base64,bcrypt
import Constant,ErrorMessages
#------------------ENUM Definations------------------
POST_ID_ROW = 0

#---------------------------------------------------- 

class Account(object):
	
    def __init__(self):
        self.user_id =""
        self.email_adress = ""
        self.password = ""
        self.phone = ""
    
    def Deserialize(self,json_object):
        self.__dict__ = json_object
        return self.EmptyControl()
        
    def SetVariablesWithRules(self):
        if not hasattr(self, 'user_id'):
            self.password = bcrypt.hashpw(self.password.encode('utf8'), bcrypt.gensalt())
        
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
                 'title' : self.title,
                 'date' : self.date,
                 'picture' : self.picture,
                 'quill_obj' : base64.decodestring(self.quill_obj),  
                 'tag_list' : self.tag_obj_list,
                 'comment_list' : self.comment_obj_list,
                 'is_private': self.is_private,
                 'view_count': self.view_count
                 }
