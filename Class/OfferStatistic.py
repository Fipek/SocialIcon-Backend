# -*- coding: utf-8 -*-
import json,base64 
#------------------ENUM Definations------------------
OFFER_ID_ROW = 0
PLATFORM_ID_ROW = 1
COIN_ROW = 2
COUNTER_ROW = 3
CREATE_DATE_ROW = 4
LIKE_COUNT_ROW = 5
SHARE_COUNT_ROW = 6
VIEWING_COUNT_ROW = 7
AGREEMENT_COUNT_ROW = 8
VIEWING_LIST_ROW = 9
#---------------------------------------------------- 

class OfferStatistic(object):
	
    def __init__(self):
        self.offer_id = ""        
        self.platform_id = ""
        self.coin = ""
        self.counter = ""
        self.create_date = ""
        self.like_count = ""
        self.share_count = ""
        self.viewing_count = ""
        self.agreement_count = ""
        self.viewing_list = ""
    
    def Deserialize(self,json_object):
        self.__dict__ = json_object

    def SetVariablesWithRules(self):
        pass      
    
    def EmptyControl(self):
        pass  
    
    def SetFromDb(self,offer):# Fetch data from Database.
        self.offer_id = offer[OFFER_ID_ROW]
        self.platform_id = offer[PLATFORM_ID_ROW]
        self.coin = offer[COIN_ROW]
        self.counter = offer[COUNTER_ROW]
        self.create_date = offer[CREATE_DATE_ROW]
        self.like_count = offer[LIKE_COUNT_ROW]
        self.share_count = offer[SHARE_COUNT_ROW]
        self.viewing_count = offer[VIEWING_COUNT_ROW]
        self.agreement_count = offer[AGREEMENT_COUNT_ROW]
        self.viewing_list = offer[VIEWING_LIST_ROW]

    def ToJson(self):
    	return  {'offer_id' : self.offer_id,
               'platform_id' : self.platform_id,  
               'coin' : self.coin, 
               'counter': self.counter,
               'create_date' : self.create_date,
               'like_count' : self.like_count,
               'share_count' : self.share_count,
               'viewing_count' : self.viewing_count,
               'agreement_count' : self.agreement_count,
               'viewing_list' : self.viewing_list
              }

