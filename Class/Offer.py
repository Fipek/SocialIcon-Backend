# -*- coding: utf-8 -*-
import json,base64 
import Constant,ErrorMessages
from Util import Util
#------------------ENUM Definations------------------
OFFER_ID_ROW = 0
USER_ID_ROW = 1
URL_ROW = 2
TITLE_ROW = 3
PLATFORM_ID_ROW = 4
COIN_ROW = 5
DURATION_ROW = 6
COUNTER_ROW = 7
CREATE_DATE_ROW = 8
LIKE_COUNT_ROW = 9
#---------------------------------------------------- 

class Offer(object):
	
    def __init__(self):
        self.offer_id = ""
        self.user_id = ""
        self.url = ""
        self.title = ""
        self.platform_id = ""
        self.coin = ""
        self.duration = ""
        self.counter = ""
        self.create_date = ""
        self.like_count = ""
        self.is_liked = ""
        self.is_agreement = ""
        self.profile_object = ""
    
    def Deserialize(self,json_object):
        self.__dict__ = json_object
        if int(self.platform_id) != -1:
            return self.EmptyControl()

    def SetVariablesWithRules(self):
        util_instance = Util()
        self.create_date = util_instance.GetDateTimeNow()        
    
    def EmptyControl(self):
        if self.user_id is None or self.user_id == "":
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'2000', 'Message': ErrorMessages.EmptyMessage['2000']})
        if self.url is None or self.url == "":
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'2004', 'Message': ErrorMessages.EmptyMessage['2004']})
        if self.title is None or self.title == "":
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'2005', 'Message': ErrorMessages.EmptyMessage['2005']})
        if self.platform_id is None or self.platform_id == "":
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'2006', 'Message': ErrorMessages.EmptyMessage['2006']})
        if self.coin is None or self.coin == "":
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'2007', 'Message': ErrorMessages.EmptyMessage['2007']})
        if self.duration is None or self.duration == "":
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'2008', 'Message': ErrorMessages.EmptyMessage['2008']})
        if self.counter is None or self.counter == "":
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'2009', 'Message': ErrorMessages.EmptyMessage['2009']})
        return Constant.OK    
    
    def SetFromDb(self,offer):# Databaseden veri çekerken
        self.offer_id = offer[OFFER_ID_ROW]
        self.user_id = offer[USER_ID_ROW]
        self.url = offer[URL_ROW]
        self.title = offer[TITLE_ROW]
        self.platform_id = offer[PLATFORM_ID_ROW]
        self.coin = offer[COIN_ROW]
        self.duration = offer[DURATION_ROW]
        self.counter = offer[COUNTER_ROW]
        self.create_date = offer[CREATE_DATE_ROW]
        self.like_count = offer[LIKE_COUNT_ROW]

    def ToJson(self):
    	return  {'offer_id' : self.offer_id,
               'user_id' : self.user_id,
               'url' : self.url,
               'title' : self.title,
               'platform_id' : self.platform_id,  
               'coin' : self.coin,
               'duration' : self.duration, 
               'counter': self.counter,
               'create_date' : self.create_date,
               'like_count' : self.like_count,
               'is_liked' : self.is_liked,
               'is_agreement' : self.is_agreement,
               'profile_object' : self.profile_object
              }

