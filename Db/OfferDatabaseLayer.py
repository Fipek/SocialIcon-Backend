# -*- coding: utf-8 -*-
import sys,os
#sys.path.append('/root/Project/Api/Log')
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from DatabaseDeclarative import Base,Account,Profile,Offer,OfferLikeYoutube,OfferViewingLog,OfferAgreementYoutube
#--Others--
import Constant,ErrorMessages,SuccessMessages


class OfferDatabase(object):
    instance = None

    def __new__(cls,*args,**kwargs):
        if cls.instance is None:
            cls.instance = super(OfferDatabase, cls).__new__(cls,*args,**kwargs)
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
    def AddOfferDb(self,offer_obj):
        try:
            session = self.CreateSessionSqlAlchemy()
            new_offer = Offer(USER_ID= offer_obj.user_id, URL= offer_obj.url, TITLE= offer_obj.title, PLATFORM_ID= offer_obj.platform_id, COIN= offer_obj.coin, DURATION= offer_obj.duration, COUNTER= offer_obj.counter, CREATE_DATE= offer_obj.create_date, LIKE_COUNT=0, SHARE_COUNT=0,AGREEMENT_COUNT=0, VIEWING_COUNT=0)
            session.add(new_offer)
            session.commit()
            session.refresh(new_offer)
            session.close()
            return {'Status': Constant.OK, 'Data':'', 'Code':'1002', 'Message':SuccessMessages.Message['1002']}
        except Exception as error:
            print str(error)
            session.close()
            #logger_instance = Logger()
            #logger_instance.AddLog(str(error).decode('UTF-8'),"PostDatabase--CreateSessionSqlAlchemy()")
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1009', 'Message': ErrorMessages.Message['1009']})
    
    def AddOfferAgreementDb(self,offer_id, user_id, create_date):
        try:
            session = self.CreateSessionSqlAlchemy()
            new_agreement = OfferAgreementYoutube(OFFER_ID= offer_id, USER_ID= user_id, CREATE_DATE= create_date)
            session.add(new_agreement)
            update_offer = (session.query(Offer).filter(Offer.OFFER_ID == offer_id)).one_or_none()
            if update_offer is not None:
                update_offer.AGREEMENT_COUNT = update_offer.AGREEMENT_COUNT + 1 
            session.commit()
            session.close()
            return {'Status': Constant.OK, 'Data':'', 'Code':'1002', 'Message':SuccessMessages.Message['1002']}
        except Exception as error:
            print str(error)
            session.close()
            #logger_instance = Logger()
            #logger_instance.AddLog(str(error).decode('UTF-8'),"PostDatabase--CreateSessionSqlAlchemy()")
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1009', 'Message': ErrorMessages.Message['1009']})
    
    def AddOfferLikeDb(self,offer_id, user_id, create_date):
        try:
            session = self.CreateSessionSqlAlchemy()
            new_like = OfferLikeYoutube(OFFER_ID= offer_id, USER_ID= user_id, CREATE_DATE= create_date)
            session.add(new_like)
            update_offer = (session.query(Offer).filter(Offer.OFFER_ID == offer_id)).one_or_none()
            if update_offer is not None:
                update_offer.LIKE_COUNT = update_offer.LIKE_COUNT + 1 
            session.commit()
            session.close()
            return {'Status': Constant.OK, 'Data':'', 'Code':'1002', 'Message':SuccessMessages.Message['1002']}
        except Exception as error:
            print str(error)
            session.close()
            #logger_instance = Logger()
            #logger_instance.AddLog(str(error).decode('UTF-8'),"PostDatabase--CreateSessionSqlAlchemy()")
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1009', 'Message': ErrorMessages.Message['1009']})
#------------------------GET PROCESS------------------------------------------------------		
    
    def GetOfferDb(self,offer_id):
        try:
            session = self.CreateSessionSqlAlchemy()
            offer = session.query(Offer.OFFER_ID, Offer.USER_ID, Offer.URL, Offer.TITLE, Offer.PLATFORM_ID, Offer.COIN, Offer.DURATION, Offer.COUNTER, Offer.CREATE_DATE, Offer.LIKE_COUNT).filter_by(OFFER_ID = offer_id).one_or_none()
            session.close()
            if offer is not None:
                return {'Status': Constant.OK, 'Data':offer, 'Code':'', 'Message':''}
            else:
                return({'Status': Constant.ERROR, 'Data':'', 'Code':'', 'Message': ErrorMessages.Message['1003']})
        except Exception as error:
            print str(error)
            #logger_instance = Logger()
            #logger_instance.AddLog(str(error),"UserDatabase--GetUser()")
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'', 'Message': ErrorMessages.Message['1003']})
  
    def GetUserOfferDb(self,user_id):
        try:
            session = self.CreateSessionSqlAlchemy()
            #print dir(session)
            #print "-------"
            #print dir(session.query(Offer.OFFER_ID, Offer.USER_ID, Offer.URL, Offer.TITLE, Offer.PLATFORM_ID, Offer.COIN, Offer.DURATION, Offer.COUNTER, Offer.CREATE_DATE).filter_by(USER_ID = user_id))
            offer_list = session.query(Offer.OFFER_ID, Offer.USER_ID, Offer.URL, Offer.TITLE, Offer.PLATFORM_ID, Offer.COIN, Offer.DURATION, Offer.COUNTER, Offer.CREATE_DATE, Offer.LIKE_COUNT).filter_by(USER_ID = user_id).all()
            session.close()
            return {'Status': Constant.OK, 'Data':offer_list, 'Code':'', 'Message':''}
        except Exception as error:
            print str(error)
            session.close()
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'', 'Message': ErrorMessages.Message['1003']})
          
    def GetOfferGlobalList(self, user_id):
        try:
            offer_information_list = []
            session = self.CreateSessionSqlAlchemy()
            offer_list = session.query(Offer.OFFER_ID, Offer.USER_ID, Offer.URL, Offer.TITLE, Offer.PLATFORM_ID, Offer.COIN, Offer.DURATION, Offer.COUNTER, Offer.CREATE_DATE, Offer.LIKE_COUNT).all()
            for index in range(0,len(offer_list)):
                sub_list = []
                profile = session.query(Profile.ID, Profile.FULLNAME, Profile.USERNAME, Profile.PICTURE,).filter_by(ID = offer_list[index].USER_ID).one()
                sub_list.append(offer_list[index])
                sub_list.append(profile)
                offer_information_list.append(sub_list)
            session.close()
            return {'Status': Constant.OK, 'Data':offer_information_list, 'Code':'', 'Message':''}
        except Exception as error:
            print str(error)
            session.close()
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'', 'Message': ErrorMessages.Message['1003']})
    
    def GetIsLikedOfferDb(self,offer_id,user_id):
        try:
            session = self.CreateSessionSqlAlchemy()
            is_liked = (session.query(OfferLikeYoutube).filter(OfferLikeYoutube.OFFER_ID == offer_id).filter(OfferLikeYoutube.USER_ID == user_id)).one_or_none()
            session.close()
            if is_liked is not None:
                return True
            else:
                return False
        except Exception as error:
            print str(error)
            session.close()
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'', 'Message': ErrorMessages.Message['1003']})
          
    def GetIsAgreementOfferDb(self,offer_id,user_id):
        try:
            session = self.CreateSessionSqlAlchemy()
            is_agreement = (session.query(OfferAgreementYoutube).filter(OfferAgreementYoutube.OFFER_ID == offer_id).filter(OfferAgreementYoutube.USER_ID == user_id)).one_or_none()
            session.close()
            if is_agreement is not None:
                return True
            else:
                return False
        except Exception as error:
            print str(error)
            session.close()
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'', 'Message': ErrorMessages.Message['1003']})
          
    def GetOfferStatisticDb(self,offer_id,user_id):
        try:
            offer_statistic_list = []
            session = self.CreateSessionSqlAlchemy()
            offer = session.query(Offer.OFFER_ID, Offer.PLATFORM_ID, Offer.COIN, Offer.COUNTER, Offer.CREATE_DATE, Offer.LIKE_COUNT, Offer.SHARE_COUNT, Offer.VIEWING_COUNT).filter_by(OFFER_ID = offer_id).one_or_none()
            if offer is not None:
                for index in range(0,len(offer)):
                    offer_statistic_list.append(offer[index])
                agreement_count = (session.query(func.count(OfferAgreementYoutube.USER_ID)).filter(OfferAgreementYoutube.OFFER_ID == offer_id)).all()
                offer_statistic_list.append(agreement_count[0][0])
                statistic = session.query(OfferViewingLog.CREATE_DATE, func.count(OfferViewingLog.ROW_ID)).filter(OfferViewingLog.OFFER_ID == offer_id).group_by(func.DATE(OfferViewingLog.CREATE_DATE)).all()
                print statistic
                offer_statistic_list.append(statistic)
                session.close()
                return {'Status': Constant.OK, 'Data':offer_statistic_list, 'Code':'', 'Message':''}
            else:
                return({'Status': Constant.ERROR, 'Data':'', 'Code':'', 'Message': ErrorMessages.Message['1003']})
        except Exception as error:
            print str(error)
            session.close()
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'', 'Message': ErrorMessages.Message['1003']})

#----------------------UPDATE PROCESS------------------------------------------------------
    def UpdateOfferDb(self,offer_obj):
        try:
            session = self.CreateSessionSqlAlchemy()
            update_offer = (session.query(Offer).filter(Offer.OFFER_ID == offer_obj.offer_id).filter(Offer.USER_ID == offer_obj.user_id)).one_or_none()
            if update_offer is not None:
                update_offer.TITLE = offer_obj.title
                update_offer.COIN = offer_obj.coin
                update_offer.DURATION = offer_obj.duration
                update_offer.counter = offer_obj.counter
                session.commit()
                session.close()
            else:
                session.close()
                return({'Status': Constant.ERROR, 'Data':'', 'Code':'1003', 'Message': ErrorMessages.Message['1003']})
            return {'Status': Constant.OK, 'Data':'', 'Code':'', 'Message': SuccessMessages.Message['1003']}
        except Exception as error:
            print str(error)
            session.close()
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1003', 'Message': ErrorMessages.Message['1003']})
          
    def OfferStatisticViewingDb(self, offer_id, user_id, create_date):
        try:
            session = self.CreateSessionSqlAlchemy()
            new_view = OfferViewingLog(OFFER_ID= offer_id, USER_ID= user_id, CREATE_DATE= create_date)
            session.add(new_view)
            update_offer = (session.query(Offer).filter(Offer.OFFER_ID == offer_id)).one_or_none()
            if update_offer is not None:
                update_offer.VIEWING_COUNT = update_offer.VIEWING_COUNT + 1 
            else:
                return {'Status': Constant.ERROR, 'Data':'', 'Code':'1011', 'Message':ErrorMessages.Message['1011']}
            session.commit()
            session.close()
            return {'Status': Constant.OK, 'Data':'', 'Code':'1002', 'Message':SuccessMessages.Message['1002']}
        except Exception as error:
            print str(error)
            session.close()
            #logger_instance = Logger()
            #logger_instance.AddLog(str(error).decode('UTF-8'),"PostDatabase--CreateSessionSqlAlchemy()")
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1009', 'Message': ErrorMessages.Message['1009']})
          
    def OfferStatisticShareDb(self, offer_id, user_id, create_date):
        try:
            session = self.CreateSessionSqlAlchemy()
            update_offer = (session.query(Offer).filter(Offer.OFFER_ID == offer_id)).one_or_none()
            if update_offer is not None:
                update_offer.SHARE_COUNT = update_offer.SHARE_COUNT + 1 
            session.commit()
            session.close()
            return {'Status': Constant.OK, 'Data':'', 'Code':'1002', 'Message':SuccessMessages.Message['1002']}
        except Exception as error:
            print str(error)
            session.close()
            #logger_instance = Logger()
            #logger_instance.AddLog(str(error).decode('UTF-8'),"PostDatabase--CreateSessionSqlAlchemy()")
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1009', 'Message': ErrorMessages.Message['1009']})

    def DeleteOfferDb(self,offer_id, user_id):
        try:
            session = self.CreateSessionSqlAlchemy()
            session.query(OfferLikeYoutube).filter(OfferLikeYoutube.OFFER_ID == offer_id).delete()
            session.query(Offer).filter(Offer.OFFER_ID == offer_id).filter(Offer.USER_ID == user_id).delete()
            session.commit()
            session.close()
            return {'Status': Constant.OK, 'Data':'', 'Code':'1002', 'Message':SuccessMessages.Message['1002']}
        except Exception as error:
            print str(error)
            session.close()
            #logger_instance = Logger()
            #logger_instance.AddLog(str(error).decode('UTF-8'),"PostDatabase--CreateSessionSqlAlchemy()")
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1009', 'Message': ErrorMessages.Message['1009']})
      
    def DeleteOfferLikeDb(self,offer_id, user_id):
        try:
            session = self.CreateSessionSqlAlchemy()
            session.query(OfferLikeYoutube).filter(OfferLikeYoutube.OFFER_ID == offer_id).filter(OfferLikeYoutube.USER_ID == user_id).delete()
            update_offer = (session.query(Offer).filter(Offer.OFFER_ID == offer_id)).one_or_none()
            if update_offer is not None:
                update_offer.LIKE_COUNT = update_offer.LIKE_COUNT - 1 
            session.commit()
            session.close()
            return {'Status': Constant.OK, 'Data':'', 'Code':'1002', 'Message':SuccessMessages.Message['1002']}
        except Exception as error:
            print str(error)
            session.close()
            #logger_instance = Logger()
            #logger_instance.AddLog(str(error).decode('UTF-8'),"PostDatabase--CreateSessionSqlAlchemy()")
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1009', 'Message': ErrorMessages.Message['1009']})
