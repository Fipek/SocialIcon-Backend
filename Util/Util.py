# -*- coding: utf-8 -*-
import sys,uuid,os,re,pytz
sys.path.append('/root/Project/Api/Db')
from validate_email import validate_email
from datetime import datetime
from UserDatabaseLayer import UserDatabase
import Constant,ErrorMessages


class Util(object):
    
    def VerifyEmailAdress(self,email_adress):
        is_valid = validate_email(email_adress,verify=True)
        return is_valid
      
    def CheckUniqueEmailAdress(self,email_adress):
        result = UserDatabase().GetCheckEmailForSign(email_adress)
        if result == None:
          return True
        else:
          return False
    
    def CheckVerifyEmailAdressForEdit(self,user_id, exist_email_adress):
        email_adress = UserDatabase().GetCheckEmailForEdit(user_id)
        if self.VerifyEmailAdress(exist_email_adress):
            print exist_email_adress
            print email_adress[0]
            if email_adress == None:
                return {'Status': Constant.OK, 'Data':'', 'Code':'', 'Message':''}
            elif str(email_adress[0]) == str(exist_email_adress):
                return {'Status': Constant.OK, 'Data':'', 'Code':'', 'Message':''}
            else:
                return({'Status': Constant.ERROR, 'Data':'', 'Code':'1002', 'Message': ErrorMessages.Message['1002']})
        else:
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1001', 'Message': ErrorMessages.Message['1001']})
      
    def VerifyPassword(self,password):
        if len(password) >= 6:
            return True
        else:
            return False
          
    def VerifyYoutubeLink(self,url):
        #control url is malformed
        #youtube_regex = (r'(https?://)?(www\.)?youtube\.(com|nl)/watch\?v=([-\w]+)')
        youtube_regex = (r'(https?://)?(www\.)?' '(youtube|youtu|youtube-nocookie)\.(com|be)/' '(watch\?.*?(?=v=)v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        result = re.match(youtube_regex, url)
        if result:
            return {'Status': Constant.OK, 'Data':'', 'Code':'', 'Message':''}
        else:
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1010', 'Message': ErrorMessages.Message['1010']})
          
    def SaveImage(self,image_file):
        try:
            unique_image_name = str(uuid.uuid4())+str(".png")
            image_file.save(os.path.join(Constant.PROFILE_UPLOAD_IMAGE, unique_image_name))
            return {'Status': Constant.OK, 'Data':unique_image_name, 'Code':'', 'Message':''}
        except Exception as e:
            print str(e)
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1003', 'Message': ErrorMessages.Message['1003']})
          
    def DeleteImage(self,image_name):
        try:
            print image_name
            if os.path.exists(Constant.PROFILE_UPLOAD_IMAGE + image_name):
                os.remove(Constant.PROFILE_UPLOAD_IMAGE + image_name)
            return {'Status': Constant.OK, 'Data':'', 'Code':'', 'Message':''}
        except Exception as e:
            print str(e)
            return({'Status': Constant.ERROR, 'Data':'', 'Code':'1003', 'Message': ErrorMessages.Message['1003']})
          
    def GetDateTimeNow(self):
        istanbul = pytz.timezone('Europe/Istanbul')
        return datetime.now(pytz.utc).astimezone(istanbul).strftime("%Y-%m-%d %H:%M:%S")
          
          