# -*- coding: utf-8 -*-
import sys,json
from datetime import datetime
sys.path.append('/root/Project/Api/Class')
sys.path.append('/root/Project/Api/Service')
sys.path.append('/root/Project/Api/Db')
sys.path.append('/root/Project/Api/Util')
sys.path.append('/root/Project/Api/Constant')
#------------------Local Component-------------------
#--Class--
from Offer import Offer
from OfferStatistic import OfferStatistic
#--Db--
from OfferDatabaseLayer import OfferDatabase
#--Others--
from Util import Util
import Constant,ErrorMessages,SuccessMessages


class OfferService(object):
    def __init__(self):
        self.offer_db_instance = OfferDatabase()
        self.util_instance = Util()

    def AddOfferService(self,offer_json):
        offer_instance = Offer()
        offer_instance.Deserialize(offer_json)
        url_flag = self.util_instance.VerifyYoutubeLink(offer_instance.url)
        if url_flag['Status'] is not Constant.OK:
            return url_flag 
        offer_instance.SetVariablesWithRules()
        result= self.offer_db_instance.AddOfferDb(offer_instance)
        return result
      
    def AddLikeOfferService(self,like_json):
        result= self.offer_db_instance.AddOfferLikeDb(like_json['offer_id'], like_json['user_id'], self.util_instance.GetDateTimeNow())
        return result

    def GetOfferGlobalList(self,user_id):
        result = self.offer_db_instance.GetOfferGlobalList(user_id)
        offer_obj_list = []
        offer_list = result['Data']
        for index in range(0,len(offer_list)):
            offer_obj = self.SetOfferForGlobal(offer_list[index][0], offer_list[index][1], user_id)
            offer_obj_list.append(offer_obj)
        return({'Status': Constant.OK, 'Data':offer_obj_list, 'Code':'', 'Message':''})
      
    def GetOfferService(self,offer_id):
        result = self.offer_db_instance.GetOfferDb(offer_id)
        if result['Status'] == Constant.ERROR:
            return result
        offer_instance = Offer()
        offer_instance.SetFromDb(result['Data'])
        return({'Status': Constant.OK, 'Data':offer_instance.ToJson(), 'Code':'', 'Message':''})

    def UpdateOfferService(self, offer_json):
        offer_instance = Offer()
        offer_flag = offer_instance.Deserialize(offer_json)
        if offer_flag is not Constant.OK:
            return offer_flag
        offer_instance.SetVariablesWithRules()
        result = self.offer_db_instance.UpdateOfferDb(offer_instance)
        return result
      
    def DeleteOfferService(self, offer_json):
        result = self.offer_db_instance.DeleteOfferDb(offer_json['offer_id'], offer_json['user_id'])
        return result
    
    def OfferStatisticService(self, statistic_json):
        if statistic_json['statistic_type'] == Constant.VIEWING_STATISTIC_TYPE:
            result = self.offer_db_instance.OfferStatisticViewingDb(statistic_json['offer_id'], statistic_json['user_id'], self.util_instance.GetDateTimeNow())
            return result
        elif statistic_json['statistic_type'] == Constant.SHARE_STATISTIC_TYPE:
            result = self.offer_db_instance.OfferStatisticShareDb(statistic_json['offer_id'], statistic_json['user_id'], self.util_instance.GetDateTimeNow())
            return result
          
    def OfferGetStatisticService(self, statistic_json):
        result = self.offer_db_instance.GetOfferStatisticDb(statistic_json['offer_id'], statistic_json['user_id'])
        offer_statistic_instance = OfferStatistic()
        offer_statistic_instance.SetFromDb(result['Data'])
        return({'Status': Constant.OK, 'Data':offer_statistic_instance.ToJson(), 'Code':'', 'Message':''})
          
    def OfferAgreementCompletedService(self,agreement_json):
        result= self.offer_db_instance.AddOfferAgreementDb(agreement_json['offer_id'], agreement_json['user_id'], self.util_instance.GetDateTimeNow())
        return result
      
    def SetOfferForProfile(self,offer_list,user_id):
        offer_obj_list = []
        for index in range(0,len(offer_list)):
            offer_instance = Offer()
            offer_instance.SetFromDb(offer_list[index])
            offer_instance.is_liked= self.offer_db_instance.GetIsLikedOfferDb(offer_instance.offer_id, user_id)
            offer_instance.is_agreement= self.offer_db_instance.GetIsAgreementOfferDb(offer_instance.offer_id, user_id)
            offer_obj_list.append(offer_instance.ToJson())
        return offer_obj_list
      
    def SetOfferForGlobal(self, offer, profile, user_id):
        from UserService import UserService
        user_service_instance = UserService()
        offer_instance = Offer()
        offer_instance.SetFromDb(offer)
        offer_instance.is_liked= self.offer_db_instance.GetIsLikedOfferDb(offer_instance.offer_id, user_id)
        offer_instance.is_agreement= self.offer_db_instance.GetIsAgreementOfferDb(offer_instance.offer_id, user_id)
        offer_instance.profile_object = user_service_instance.SetProfileForGlobal(profile)
        return offer_instance.ToJson()
    
    def DeleteLikeOfferService(self,like_json):
        result = self.offer_db_instance.DeleteOfferLikeDb(like_json['offer_id'], like_json['user_id'])
        return result

            