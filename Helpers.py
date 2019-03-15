# -*- coding: utf-8 -*-
import sys,json,requests,re,uuid,os,jwt,datetime,bcrypt
sys.path.append('/root/Project/Api/Service')
sys.path.append('/root/Project/Api/Db')
sys.path.append('/root/Project/Api/Util')
sys.path.append('/root/Project/Api/Constant')
from flask import Flask, jsonify, make_response,request
from flask_restful import Api,reqparse
from flask_cors import CORS, cross_origin
from functools import wraps
#------------------Local Component-------------------
from OfferService import OfferService
from UserService import UserService
from SecurityService import SecurityService
from UserDatabaseLayer import UserDatabase
from Util import Util
import Constant,ErrorMessages

#------------------ENUM Definations------------------
NETWORK_ADRESS = "68.183.216.241"
NETWORK_PORT = 5001
#------------------CONFIGURATION---------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisthesecretkey'
api = Api(app)
CORS(app,supports_credentials=True)
cors = CORS(app, resources={r"/api/*/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
#----------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'message': 'Page Is Not Found'}),403

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal Service Error'}),500

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'Token is missing'}),403
        try:
            date = jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'}),403
        return f(*args,**kwargs)
    return decorated

#---------------------------------------------UNPROTECTED-------------------------------------------------
@cross_origin(origin='*',headers=['Content-Type','Authorization'],methods=['GET','POST'] )
@app.route('/api/unprotected/login',methods=["GET", "POST"])
def Login():
    args = json.loads(request.data)
    password = args['password'].encode('utf-8')
    email_adress = args['email'].encode('utf8')
    account_response = UserDatabase().GetAccount(email_adress)
    if account_response['Status'] == Constant.OK:
        user_id = account_response['Data'][0]
        real_pass = account_response['Data'][1]
        #hashed = bcrypt.hashpw(password, bcrypt.gensalt()
    else:
        return make_response(jsonify({'Status': Constant.ERROR, 'Data':'', 'Code':'1013', 'Message': ErrorMessages.Message['1013']}))
        #return make_response('Could not verify!',401,{'WWW-Authenticate': 'Basic realm="Login Required"'})
    if bcrypt.checkpw(password, real_pass.encode('utf-8')):
        token = jwt.encode({'user_id' : user_id,'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=180)}, app.config['SECRET_KEY'])
        Security_service_instance = SecurityService()
        Security_service_instance.CreateSessionService(user_id, token, request.remote_addr, request.headers['User-Agent'])
        return make_response(jsonify({'Status': Constant.OK, 'Data':{'token' : token.decode('UTF-8')}, 'Code':'', 'Message':''}))
    return make_response(jsonify({'Status': Constant.ERROR, 'Data':'', 'Code':'1012', 'Message': ErrorMessages.Message['1012']}))
  
@app.route('/api/unprotected/verify_email_adress',methods=["GET", "POST"])
def VerifyEMailAdress():
    args = json.loads(request.data)
    User_service_instance = UserService()
    result = User_service_instance.VerifyEMailAdress(args['email'])
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response  
  
@app.route('/api/unprotected/forgot-pass',methods=["POST"])
def ExistsEMailAdress():
    args = request.form.to_dict()
    User_service_instance = UserService()
    result = User_service_instance.VerifyEMailAdress(args['email_adress'], args['purpose'])
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response 
  
@app.route('/api/unprotected/create_user',methods=["POST"])
def SignUp():
    args = json.loads(request.data)
    verify = args['verify']
    if verify:
        User_service_instance = UserService()
        result = User_service_instance.CreateUser(args)
    else:
        result='Unreliable'
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response 

#---------------------------------------------PROTECTED---------------------------------------------------

  
@app.route('/api/protected/get/offer-global',methods=["POST"])
@token_required
def GetOfferListGlobal():
    Offer_service_instance = OfferService()
    args = request.form.to_dict()
    result = Offer_service_instance.GetOfferGlobalList(args['user_id'])
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route('/api/protected/profile/get',methods=["POST"])
@token_required
def GetProfile():
    User_service_instance = UserService()
    args = request.form.to_dict()
    print args
    result = User_service_instance.GetFullProfile(args['user_id'])
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
  
@app.route('/api/protected/edit-profile/get',methods=["POST"])
@token_required
def GetEditProfile():
    User_service_instance = UserService()
    args = request.form.to_dict()
    result = User_service_instance.GetUser(args['user_id'])
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
  
@app.route('/api/protected/profile/update',methods=["POST"])
@token_required
def UpdateProfile():
    User_service_instance = UserService()
    args = request.form.to_dict() 
    if 'profile_picture' in request.files:
        image_file = request.files['profile_picture']
    else:
        image_file= None
    result = User_service_instance.UpdateUser(args, image_file)
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
  
@app.route('/api/protected/offer/get',methods=["POST"])
@token_required
def GetOffer():
    Offer_service_instance = OfferService()
    args = request.form.to_dict()
    result = Offer_service_instance.GetOfferService(args['offer_id'])
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route('/api/protected/offer/add',methods=["POST"])
@token_required
def AddOffer():
    Offer_service_instance = OfferService()
    args = request.form.to_dict()
    result = Offer_service_instance.AddOfferService(args)
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
  
@app.route('/api/protected/offer/update',methods=["POST"])
@token_required
def UpdateOffer():
    Offer_service_instance = OfferService()
    args = request.form.to_dict()
    result = Offer_service_instance.UpdateOfferService(args)
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
  
@app.route('/api/protected/offer/delete',methods=["POST"])
@token_required
def DeleteOffer():
    Offer_service_instance = OfferService()
    args = request.form.to_dict()
    result = Offer_service_instance.DeleteOfferService(args)
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
  
@app.route('/api/protected/offer/add-like',methods=["POST"])
@token_required
def AddOfferLike():
    Offer_service_instance = OfferService()
    args = request.form.to_dict()
    result = Offer_service_instance.AddLikeOfferService(args)
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
  
@app.route('/api/protected/offer/statistic/add',methods=["POST"])
@token_required
def AddOfferStatistic():
    Offer_service_instance = OfferService()
    args = request.form.to_dict()
    result = Offer_service_instance.OfferStatisticService(args)
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
  
@app.route('/api/protected/offer/statistic/get',methods=["POST"])
@token_required
def GetOfferStatistic():
    Offer_service_instance = OfferService()
    args = request.form.to_dict()
    result = Offer_service_instance.OfferGetStatisticService(args)
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
  
@app.route('/api/protected/offer/agreement/completed',methods=["POST"])
@token_required
def OfferAgreementCompleted():
    Offer_service_instance = OfferService()
    args = request.form.to_dict()
    result = Offer_service_instance.OfferAgreementCompletedService(args)
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
  
@app.route('/api/protected/offer/delete-like',methods=["POST"])
@token_required
def DeleteOfferLike():
    Offer_service_instance = OfferService()
    args = request.form.to_dict()
    result = Offer_service_instance.DeleteLikeOfferService(args)
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

#--------------------------------------------RUN----------------------------------------------------------
if __name__ == '__main__':
    app.run(host=NETWORK_ADRESS, port=NETWORK_PORT, debug=True)