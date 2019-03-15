# -*- coding: utf-8 -*-
import sys,json
from datetime import datetime
sys.path.append('/root/Project/Api/Class')
sys.path.append('/root/Project/Api/Db')
sys.path.append('/root/Project/Api/Util')
sys.path.append('/root/Project/Api/Constant')
#------------------Local Component-------------------
#--Service--
from OfferService import OfferService
#--Class--
from Account import Account
from Profile import Profile
from User import User
#--Db--
from UserDatabaseLayer import UserDatabase
from OfferDatabaseLayer import OfferDatabase
#--Others--
from Util import Util
import Constant,ErrorMessages,SuccessMessages


class UserService(object):
    def __init__(self):
        self.user_db_instance = UserDatabase()
        self.util_instance = Util()
        self.offer_db_instance = OfferDatabase()
        
    def VerifyEMailAdress(self,email_adress, purpose= None ):#If the "purpose" field is full, it is intended to check if there is an e-mail address. 
        result = self.util_instance.VerifyEmailAdress(email_adress)
        if result:
            if self.util_instance.CheckUniqueEmailAdress(email_adress):
                if purpose == None:
                    return({'Status': Constant.OK, 'Data':result, 'Code':'', 'Message':''})
                else:
                    return({'Status': Constant.ERROR, 'Data':result, 'Code':'1008', 'Message': ErrorMessages.Message['1008']})
            else:
                if purpose == None:
                    return({'Status': Constant.ERROR, 'Data':result, 'Code':'1002', 'Message': ErrorMessages.Message['1002']})
                else:
                    #Send Mail
                    return({'Status': Constant.OK, 'Data':result, 'Code':'', 'Message':SuccessMessages.Message['1001']})
        else:
            return({'Status': Constant.ERROR, 'Data':result, 'Code':'1001', 'Message': ErrorMessages.Message['1001']}) 

    def CreateUser(self,user_json):
        profile_instance = Profile()
        account_instance = Account()
        profile_instance.Deserialize(user_json)
        account_instance.Deserialize(user_json)
        if self.util_instance.VerifyPassword(account_instance.password):
            profile_instance.SetVariablesWithRules()
            account_instance.SetVariablesWithRules()
            result = self.user_db_instance.CreateUser(profile_instance, account_instance)
            return({'Status': Constant.OK, 'Data':'', 'Code':'', 'Message':''})
        else:
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1000', 'Message': ErrorMessages.Message['1000']})


    def UpdateUser(self, user_json, image_file):
        profile_instance = Profile()
        account_instance = Account()
        profile_flag = profile_instance.Deserialize(user_json)
        if profile_flag is not Constant.OK:
            return profile_flag
        account_flag = account_instance.Deserialize(user_json)
        if account_flag is not Constant.OK:
            return account_flag
        email_flag = self.util_instance.CheckVerifyEmailAdressForEdit(profile_instance.user_id,profile_instance.email_adress)
        if email_flag['Status'] is not Constant.OK:
            return email_flag
        if image_file is not None:
            image_flag= self.util_instance.SaveImage(image_file)
            if image_flag['Status'] == Constant.ERROR:
                return({'Status': Constant.ERROR, 'Data':'', 'Code':'1003', 'Message': ErrorMessages.Message['1003']})
            else:
                profile_instance.picture = image_flag['Data']
        profile_instance.SetVariablesWithRules()
        account_instance.SetVariablesWithRules()
        result = self.user_db_instance.UpdateUser(profile_instance, account_instance)
        
        if result['Status'] == Constant.OK:
            self.util_instance.DeleteImage(result['Data'])
            return({'Status': Constant.OK, 'Data':'', 'Code':'', 'Message':''})
        else:
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1003', 'Message': ErrorMessages.Message['1003']})

    def GetUser(self,user_id):
        result = self.user_db_instance.GetUser(user_id)
        if result['Status'] == Constant.ERROR:
            return result
        user_instance = User()
        user_instance.SetFromDb(result['Data'])
        return({'Status': Constant.OK, 'Data':user_instance.ToJson(), 'Code':'', 'Message':''})

    def GetFullProfile(self,user_id):
        print user_id
        result = self.user_db_instance.GetFullProfileDb(user_id)
        if result['Status'] == Constant.ERROR:
            return result
        profile_instance = Profile()
        profile_instance.SetFromDb(result['Data'])
        #----------GetOfferProcess------------------
        result = self.offer_db_instance.GetUserOfferDb(user_id)
        if result['Status'] == Constant.ERROR:
            return result
        if result:
            offer_service_instance = OfferService()
            profile_instance.offer_obj_list = offer_service_instance.SetOfferForProfile(result['Data'],user_id)
            profile_instance.offer_count = len(profile_instance.offer_obj_list)
        return({'Status': Constant.OK, 'Data':profile_instance.ToJson(), 'Code':'', 'Message':''})
      
    def SetProfileForGlobal(self, profile):
        profile_instance = Profile()
        profile_instance.SetFromDb(profile)
        return profile_instance.ToJson() 
        
    def UpdateOffer(self):
        pass

    def DeleteOffer(self):
        pass
