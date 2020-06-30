from flask import Flask, request, jsonify, make_response, session, app, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate, MigrateCommand
import json
from . import app
from ..data import db
from ..data.models import User
from flask import render_template, redirect, url_for, flash
from datetime import timedelta
import requests

#Put your code here

def responseMessage( data):
    #return '{"Message":"'+data+'"}'
    return jsonify(  data  )

@app.route('/', methods=['GET'])
def home():
    return responseMessage("Welcome to user service"),200


@app.route('/register', methods=['POST'])
def registerUser():
    if request.method == 'POST':
        json_request = request.get_json()
        if 'username' in json_request and 'useremail' in json_request and \
                'password' in json_request:
            #print(json_request)
            username = json_request['username']
            useremail = json_request['useremail']
            password = json_request['password']
        else:
            return "Check the fields entered",400

        newuser = User(username,useremail,password)
        db.session.add(newuser)
        #db.session.commit()


        try:
            #print("It is here",username,useremail,password)
            db.session.commit()
            data_set = {"Message": "Registration successful"}

            return jsonify(data_set),201
        except:
            #print("It is here failed")
            db.session.rollback()
            data_set = {"Message": "Check the fields entered"}
            return jsonify(data_set), 400



@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':

        json_request = request.get_json()
        #print (json_request+"valid_credentials")
        username = request.authorization['username']
        password = request.authorization['password']



        if 1 > 2 and 'username' in json_request and \
                'password' in json_request:
            username = json_request['username']
            password = json_request['password']
        #else:
            #return "Could not verify",400

        response_data = User.query.filter_by(username=username).filter_by(password=password).first()

        if response_data is None:
            data_set = {"Message": "Could not verify"}
            return jsonify(data_set),400
        else:
            session['username'] = username
            session['key'] = "username"
            data_set = {"Message": "Login success"}
            return jsonify(data_set),200

@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        if session.get('username') is None:
            data_set = {"Message": 'Already logged out'}
            return jsonify(data_set), 400
        else:
            session.pop('username')
            data_set = {"Message": 'Logout successful'}
            return jsonify(data_set), 200





@app.route('/list/hospitals', methods=['GET'])
def list_hospitals():
    if request.method == 'GET':
        if session.get('username') is None:
            data_set = {"Message": 'Login to proceed'}
            return jsonify(data_set), 400
        else:
            response_data=requests.get('http://localhost:8002/hospitals')
            #print(response_data.content,"response_data.status_code")
            return str(response_data.content),200

@app.route('/search/hospital/<name>', methods=['GET'])
def list_hospitals_by_name(name):
    if session.get('username') is None:
        data_set = {"Message": "Login to proceed"}
        return jsonify(data_set), 400
    else:
        response_data=requests.get('http://localhost:8002/hospital/'+name)
        json_list=[i.serialize for i in response_data]
        return jsonify(json_list),200

@app.route('/list/centers', methods=['GET'])
def list_centers():

    if session.get('username') is None:
        data_set = {"Message": "Login to proceed"}
        return jsonify(data_set), 400
    else:
        response_data=requests.get('http://localhost:8003/centers')
        return  jsonify(response_data),200


@app.route('/book/center', methods=['POST'])
def book_center():
    if request.method == 'POST':
        json_request = request.get_json()
        if session.get('username') is None:
            data_set = {"Message": "Login to proceed"}
            return jsonify(data_set), 400
        else:
            if 'hospital_id' in json_request and 'user_id' in json_request:
                hospital_id = json_request['hospital_id']
                user_id = json_request['user_id']

            else:
                return "Check the fields entered",400
        api_url = 'http://localhost:8003/request/center'
        create_row_data = {'hospital_id': hospital_id, 'user_id': user_id}
        r = requests.post(url=api_url, data=create_row_data)

        return r

@app.route('/status', methods=['GET'])
def status():
    if session.get('username') is None:
        data_set = {"Message": "Login to proceed"}
        return jsonify(data_set), 400
    else:
        username=session.get('username')
        response_data = User.query.filter_by(username=username).first()
        user = response_data.serialize
        #print(user['id'])
        url='http://localhost:8003/center/booking/status/'+str(user['id'])
        response_data=requests.get(url)
        #json_list=[i.serialize for i in response_data]
        return str(response_data.content), 200
