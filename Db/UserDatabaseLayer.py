# -*- coding: utf-8 -*-
import sys,os
#sys.path.append('/root/Project/Api/Log')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseDeclarative import Base,Account,Profile,Offer
#--Others--
import Constant,ErrorMessages


class UserDatabase(object):
    instance = None

    def __new__(cls,*args,**kwargs):
        if cls.instance is None:
            cls.instance = super(UserDatabase, cls).__new__(cls,*args,**kwargs)
        return cls.instance

    def __init__(self):
        self.connection_instance = None

    def CreateSessionSqlAlchemy(self):
        try:
            engine = create_engine("mysql://root:4878@localhost/SOCIALICONDB?charset=utf8&use_unicode=1", pool_recycle=3600, encoding='utf-8')
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind= engine)
            session = DBSession()
            self.connection_instance = session 
            return self.connection_instance
        except Exception as error:
            print str(error)
            #logger_instance = Logger()
            #logger_instance.AddLog(str(error).decode('UTF-8'),"PostDatabase--CreateSessionSqlAlchemy()")

#------------------------INSERT PROCESS------------------------------------------------
    def CreateUser(self,profile_obj,account_obj):
        try:
            session = self.CreateSessionSqlAlchemy()
            new_user = Account(EMAIL= account_obj.email_adress, PASSWORD= account_obj.password, PHONE="")
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            new_profile = Profile(ID= new_user.ID, FULLNAME= profile_obj.full_name, USERNAME= profile_obj.user_name)
            session.add(new_profile)
            session.commit()
            session.close()
            return {'Status': Constant.OK, 'Data':'', 'Code':'', 'Message':''}
        except Exception as error:
            print str(error)
            session.close()
            #logger_instance = Logger()
            #logger_instance.AddLog(str(error).decode('UTF-8'),"PostDatabase--CreateSessionSqlAlchemy()")
            
    def GetAccount(self,email_adress):
        try:
            session = self.CreateSessionSqlAlchemy()
            account = session.query(Account.ID, Account.PASSWORD).filter_by(EMAIL= email_adress).first()
            session.close()
            if(account):
                return {'Status': Constant.OK, 'Data': account, 'Code':'', 'Message':''}
            else:
                return({'Status': Constant.ERROR, 'Data':'', 'Code':'', 'Message': ErrorMessages.Message['1003']})
        except Exception as error:
            print str(error)
            #logger_instance = Logger()
            #logger_instance.AddLog(str(error),"UserDatabase--GetUser()")
            #return ERROR
            
#------------------------GET PROCESS------------------------------------------------------		

    def GetUser(self, user_id):
        try:
            session = self.CreateSessionSqlAlchemy()
            user_information_list = []
            account_list = session.query(Account.ID,Account.EMAIL,Account.PHONE).filter_by(ID = user_id).one()
            for index in range(0,len(account_list)):
                user_information_list.append(account_list[index])
            profile_list = session.query(Profile.ID, Profile.FULLNAME, Profile.USERNAME, Profile.PICTURE,).filter_by(ID = user_id).one()
            for index in range(1,len(profile_list)):
                user_information_list.append(profile_list[index])
            session.close()
            return {'Status': Constant.OK, 'Data':user_information_list, 'Code':'', 'Message':''}
        except Exception as error:
            print str(error)
            session.close()
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'', 'Message': ErrorMessages.Message['1003']})
          
    def GetFullProfileDb(self, user_id):
        try:
            session = self.CreateSessionSqlAlchemy()
            profile_list = session.query(Profile.ID, Profile.FULLNAME, Profile.USERNAME, Profile.PICTURE,).filter_by(ID = user_id).one()
            print profile_list
            session.close()
            return {'Status': Constant.OK, 'Data':profile_list, 'Code':'', 'Message':''}
        except Exception as error:
            print str(error)
            session.close()
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'', 'Message': ErrorMessages.Message['1003']})
    
    def GetCheckEmailForSign(self, email_adress):
        try:
            session = self.CreateSessionSqlAlchemy()
            result = session.query(Account.EMAIL).filter_by(EMAIL = email_adress).one_or_none()
            session.close()
            return result
        except Exception as error:
            print str(error)
            session.close()
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'', 'Message': ErrorMessages.Message['1003']})
          
    def GetCheckEmailForEdit(self, user_id):
        try:
            session = self.CreateSessionSqlAlchemy()
            result = session.query(Account.EMAIL).filter_by(ID = user_id).one_or_none()
            session.close()
            return result
        except Exception as error:
            print str(error)
            session.close()
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'', 'Message': ErrorMessages.Message['1003']})

#----------------------UPDATE PROCESS------------------------------------------------------
    def UpdateUser(self,profile_obj,account_obj):
        try:
            session = self.CreateSessionSqlAlchemy()
            update_user_account = (session.query(Account).filter(Account.ID == account_obj.user_id)).one_or_none()
            if update_user_account is not None:
                update_user_account.EMAIL = account_obj.email_adress
                update_user_account.PHONE = account_obj.phone
                session.commit()
            else:
                return({'Status': Constant.ERROR, 'Data':'', 'Code':'1003', 'Message': ErrorMessages.Message['1003']})
            update_user_profile = session.query(Profile).filter(Profile.ID == profile_obj.user_id).one_or_none()
            if update_user_account is not None:
                update_user_profile.FULLNAME = profile_obj.full_name
                update_user_profile.USERNAME = profile_obj.user_name
                if hasattr(profile_obj, 'picture'):
                    old_image_name = update_user_profile.PICTURE  
                    update_user_profile.PICTURE = profile_obj.picture         
                else:
                    old_image_name = "-1"
                session.commit()
                session.close()
            else:
                return({'Status': Constant.ERROR, 'Data':'', 'Code':'1003', 'Message': ErrorMessages.Message['1003']})
            return {'Status': Constant.OK, 'Data':old_image_name, 'Code':'', 'Message':''}
        except Exception as error:
            print str(error)
            session.close()
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1003', 'Message': ErrorMessages.Message['1003']})
           

    def DeletePost(self,id):
        pass


