from flask import Flask, request, jsonify, make_response, session, app, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate, MigrateCommand
import json
from . import app
from ..data import db
from ..data.models import Hospital
from flask import render_template, redirect, url_for, flash

def responseMessage( data):
    text="{'Message': '"+data+"'}"
    return jsonify(text)


def responseMessage1( data):
    #text="{'Message': '"+data+"'}"
    #return jsonify(text)
    return jsonify(  data  )

@app.route('/', methods=['GET'])
def home():
    return jsonify("Welcome to hospital service"),200

@app.route('/add/hospital', methods=['POST'])
def add_hospital():
    if request.method == 'POST':

        json_request = request.get_json()
        if 'hospitalname' in json_request and 'location' in json_request and \
                'contact' in json_request and 'capacity' in json_request:
            hospitalname = json_request['hospitalname']
            location = json_request['location']
            contact = int(json_request['contact'])
            capacity = int(json_request['capacity'])
        else:
            return "Check your values",400

        hospital = Hospital(hospitalname,location,contact,capacity)
        db.session.add(hospital)

        try:
            db.session.commit()
            data_set = {"Message": "Added successfully"}
            return jsonify(data_set), 201
        except:
            db.session.rollback()
            data_set = {"Message": "Check your values"}
            return jsonify(data_set), 400


@app.route('/hospitals', methods=['GET'])
def list_hospitals():
    response_data=Hospital.query.all()
    json_list=[i.serialize for i in response_data]
    return  jsonify(json_list),200

@app.route('/hospital/<name>', methods=['GET'])
def list_hospitals_by_name(name):
    response_data=Hospital.query.filter(Hospital.hospitalname.startswith(name)).all()
    if len(response_data) > 0:
        json_list = [i.serialize for i in response_data]
        return jsonify(json_list),200
    else:
        data_set = {"Message": "No hospital with that name"}
        return jsonify(data_set), 400

@app.route('/hospital/<id>', methods=['GET'])
def list_hospitals_by_id(id):
    response_data=Hospital.query.filter_by(id=id).all()
    if len(response_data) > 0:
        json_list = [i.serialize for i in response_data]
        return jsonify(json_list),200
    else:
        data_set = {"Message": "No hospital with that name"}
        return jsonify(data_set), 400
