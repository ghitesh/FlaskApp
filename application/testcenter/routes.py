from flask import Flask, request, jsonify, make_response, session, app, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate, MigrateCommand
import json
from . import app
from ..data import db
from ..data.models import Testcenter, Booking, Hospital
from flask import render_template, redirect, url_for, flash
from datetime import timedelta
import requests

def responseMessage( data):
    text="{'Message': '"+data+"'}"
    return jsonify(text)


@app.route('/', methods=['GET'])
def home():
    data_set = {"Welcome to test center service"}
    return jsonify('Welcome to test center service'), 200
    #return responseMessage(),200

@app.route('/add/center', methods=['POST'])
def add_hospital():
    if request.method == 'POST':

        json_request = request.get_json()
        if 'testcenter_name' in json_request and 'hospital_id' in json_request and \
                'is_available' in json_request:
            testcenter_name = json_request['testcenter_name']
            hospital_id = json_request['hospital_id']
            is_available = json_request['is_available']

        else:
            return "Check your values",400

        testcenter = Testcenter(testcenter_name,hospital_id,is_available)
        db.session.add(testcenter)

        try:
            db.session.commit()
            data_set = {"Message": "Added successfully"}
            return jsonify(data_set), 201
            #return responseMessage(''),201
        except:
            db.session.rollback()
            return responseMessage("Check your values"), 400




@app.route('/centers', methods=['GET'])
def list_centers():
    response_data=Testcenter.query.all()
    json_list=[i.serialize for i in response_data]
    return  jsonify(json_list),200

@app.route('/centers/hospital/<hid>', methods=['GET'])
def list_centers_by_hospital_id(hid):
    response_data=Testcenter.query.filter_by(hospital_id=hid).all()
    #print()
    if len(response_data) > 0:
        json_list = [i.serialize for i in response_data]
        #print("*"*100)
        #print (json_list)
        #print("*" * 100)
        return jsonify(json_list),200
    else:
        data_set = {"Message": "Enter a valid hospital id"}
        return jsonify(data_set), 400
        #return responseMessage("No hospital with that name"),400

@app.route('/request/center', methods=['POST'])
def request_center():
    if request.method == 'POST':

        json_request = request.get_json()
        if 'user_id' in json_request and 'hospital_id' in json_request:
            user_id = json_request['user_id']
            hospital_id = json_request['hospital_id']
        else:
            data_set = {"Message": "Check your values"}
            return jsonify(data_set),400

        if 1 < 2:
            hospital = Hospital.query.filter_by(id=hospital_id).first()
            #print("hospital found" + hospital[id])
            if hospital is None:
                print("Comes in None")
                data_set = {"Message": "Enter a valid hospital id"}
                return jsonify(data_set), 400

        booking = Booking(user_id,hospital_id,9999,False)
        db.session.add(booking)

        try:
            db.session.commit()
            data_set = {"Message": "Request made, wait for approval"}
            return jsonify(data_set), 200
            #return responseMessage('Request made, wait for approval'),200
        except:
            db.session.rollback()
            data_set = {"Message": "Enter a valid hospital id"}
            return jsonify(data_set), 400

@app.route('/approve/booking/<id>/center/<cid>', methods=['GET'])
def approve_bookingid_for_centerid(id,cid):
    try:
        booking = Booking.query.filter_by(id=id).filter_by(hospital_id=cid).first()
    except:
        db.session.rollback()
        data_set = {"Message": "Enter valid booking id and center id"}
        return jsonify(data_set), 400
        #return responseMessage("Enter Valid booking id and center id"), 400

    if booking is None:
        data_set = {"Message": "Enter valid booking id and center id"}
        return jsonify(data_set), 400

    booking.status = True
    booking.testing_center_id=booking.hospital_id


    try:
        db.session.commit()
        data_set = {"Message": "Approved your request"}
        return jsonify(data_set), 200
        #return responseMessage('Approved your request'), 200
    except:
        db.session.rollback()
        data_set = {"Message": "Enter valid booking id and center id"}
        return jsonify(data_set), 402

@app.route('/center/booking/status/<uid>', methods=['GET'])
def center_booking_status(uid):
    response_data=Booking.query.filter_by(user_id=uid).all()
    if len(response_data) > 0:
        json_list = [i.serialize for i in response_data]
        return jsonify(json_list),200
    else:
        data_set = {"Message": "Enter a valid user id"}
        return jsonify(data_set), 400
