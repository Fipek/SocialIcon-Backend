# -*- coding: utf-8 -*-
import sys,os
#sys.path.append('/root/Project/Api/Log')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseDeclarative import Base,Account,Profile,Offer,SessionStorage
#--Others--
import Constant,ErrorMessages


class SecurityDatabase(object):
    instance = None

    def __new__(cls,*args,**kwargs):
        if cls.instance is None:
            cls.instance = super(SecurityDatabase, cls).__new__(cls,*args,**kwargs)
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
    def CreateSession(self,session_obj):
        try:
            session = self.CreateSessionSqlAlchemy()
            #unique ya da primary key leri gözden geçir token uniqliği geçersiz gibi görünüyor.
            new_session = SessionStorage(USER_ID= session_obj.user_id, TOKEN= session_obj.token, IP_ADRESS=session_obj.ip_adress, USER_AGENT=session_obj.user_agent, CREATE_DATE=session_obj.create_date)
            session.add(new_session)
            session.commit()
            session.refresh(new_session)
            session.close()
            return {'Status': Constant.OK, 'Data':'', 'Code':'', 'Message':''}
        except Exception as error:
            print str(error)
            session.close()
            #logger_instance = Logger()
            #logger_instance.AddLog(str(error).decode('UTF-8'),"PostDatabase--CreateSessionSqlAlchemy()")
            
    def CheckSession(self,email_adress):
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
            
    def DeleteSession(self):
        try:
            session = self.CreateSessionSqlAlchemy()
            pass
            session.commit()
            session.close()
            return {'Status': Constant.OK, 'Data':'', 'Code':'', 'Message':''}
        except Exception as error:
            print str(error)
            session.close()
            #logger_instance = Logger()
            #logger_instance.AddLog(str(error).decode('UTF-8'),"PostDatabase--CreateSessionSqlAlchemy()")