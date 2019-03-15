# -*- coding: utf-8 -*-
import sys,json
from datetime import datetime
sys.path.append('/root/Project/Api/Class')
sys.path.append('/root/Project/Api/Db')
sys.path.append('/root/Project/Api/Util')
sys.path.append('/root/Project/Api/Constant')
#------------------Local Component-------------------
#--Service--

#--Class--
from Session import Session
#--Db--
from SecurityDatabaseLayer import SecurityDatabase
#--Others--
from Util import Util
import Constant,ErrorMessages,SuccessMessages


class SecurityService(object):
    def __init__(self):
        self.security_db_instance = SecurityDatabase()
        self.util_instance = Util()
        
    def CreateSessionService(self, user_id, token, ip_adress, user_agent): 
        print user_id
        print token,
        print ip_adress
        print user_agent
        print dir(user_agent)

    def CreateUser(self,user_json):
        pass
