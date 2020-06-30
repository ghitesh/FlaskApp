import requests
import pytest
import base64
from flask import Flask, session

from .hospital import app
from .testcenter import app as testcenterapp
from .user import app as userapp

from .testconfig import db
from .testconfig.models import Hospital, Testcenter, User, Booking


class Test_hospitalAPI:

    client  = app.test_client()
    
    @pytest.fixture(autouse=True, scope='session')
    def setUp(self):
        # app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.db'
        db.create_all()
        yield db
        db.drop_all()

    def test_data_in_db_before(self):
        hvalues = Hospital.query.all()
        assert len(hvalues) == 0

    def test_display_list_hospitals_before_adding(self):
        url = "/hospitals"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == []


    def test_successful_registration(self):
        url = "/add/hospital"
        payload = "{\n\t\"hospitalname\": \"test1\",\n\t\"location\": \"test\",\n\t\"contact\": 85,\n\t\"capacity\": 8}"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        response = self.client.post(url, data=payload, headers=headers)
        
        assert response.status_code == 201
        assert response.json == {'Message': 'Added successfully'}

    def test_failed_registration(self):
        url = "/add/hospital"
        payload = "{\n\t\"hospitalname\": \"test1\",\n\t\"location\": \"test\",\n\t\"contact\": 85,\n\t\"capacity\": 8}"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        response = self.client.post(url, data=payload, headers=headers)
        
        assert response.status_code == 400
        assert response.json == {'Message': 'Check your values'}

    def test_data_in_db_after(self):
        hvalues = Hospital.query.all()
        assert len(hvalues) == 1
        assert hvalues[0].hospitalname == "test1"

    def test_display_list_hospitals(self):
        url = "/hospitals"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == [{'hospitalname': 'test1', 'capacity': 8, 'location': 'test', 'id': 1, 'contact': 85}]

    def test_search_hospital_success(self):
        url = "/hospital/test"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == [{'hospitalname': 'test1', 'capacity': 8, 'location': 'test', 'id': 1, 'contact': 85}]

    def test_search_hospital_failure(self):
        url = "/hospital/test22"
        response = self.client.get(url)
        assert response.status_code == 400
        assert response.json == {'Message': 'No hospital with that name'}


class Test_testcenterAPI:

    client  = testcenterapp.test_client()
    
    @pytest.fixture(autouse=True, scope='session')
    def setUp(self):
        # app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.db'
        db.create_all()
        yield db
        db.drop_all()

    def test_testcenter_in_db_before_Adding(self):
        test_center_values = Testcenter.query.all()
        assert len(test_center_values) == 0        

    def test_list_all_centers_before_adding(self):
        url = "/centers"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == []

    def test_add_centers(self):
        url = "/add/center"
        payload = "{\n\t\"testcenter_name\": \"test1\",\n\t\"hospital_id\": 1,\n\t\"is_available\": true}"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        response = self.client.post(url, data=payload, headers=headers)
        
        assert response.status_code == 201
        assert response.json == {'Message': 'Added successfully'}

    def test_testcenter_in_db_after_Adding(self):
        test_center_values = Testcenter.query.all()
        assert len(test_center_values) == 1

    def test_list_all_centers(self):
        url = "/centers"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == [{'is_available': True, 'testcenter_name': 'test1', 'hospital_id': 1, 'id': 1}]

    def test_centers_under_hopsital_success(self):
        url = 'centers/hospital/1'
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == [{'is_available': True, 'testcenter_name': 'test1', 'hospital_id': 1, 'id': 1}]

    def test_centers_under_hopsital_failure(self):
        url = 'centers/hospital/12'
        response = self.client.get(url)
        assert response.status_code == 400
        assert response.json == {'Message': 'Enter a valid hospital id'}

    def test_request_booking_a_center_success(self):
        url = "/request/center"
        payload = "{\n\t\"hospital_id\": 1,\n\t\"user_id\": 1}"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        response = self.client.post(url, data=payload, headers=headers)
        
        assert response.status_code == 200
        assert response.json == {'Message': 'Request made, wait for approval'}

    def test_request_booking_a_center_failure(self):
        url = "/request/center"
        payload = "{\n\t\"hospital_id\": 2,\n\t\"user_id\": 1}"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        response = self.client.post(url, data=payload, headers=headers)
        
        assert response.status_code == 400
        assert response.json == {'Message': 'Enter a valid hospital id'}
    
    def test_request_booking_a_center_failure_invalid_details(self):
        url = "/request/center"
        payload = "{\n\t\"hospital_id\": 1}"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        response = self.client.post(url, data=payload, headers=headers)
        
        assert response.status_code == 400
        assert response.json == {'Message': 'Check your values'}

    def test_request_booking_in_db_before_approval(self):
        bookings = Booking.query.all()
        assert len(bookings) == 1
        assert bookings[0].testing_center_id == 9999
        assert bookings[0].status == False

    def test_request_approve_booking_success(self):
        url = '/approve/booking/1/center/1'
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == {'Message': 'Approved your request'}

    def test_request_approve_booking_failure(self):
        url = '/approve/booking/1/center/12'
        response = self.client.get(url)
        assert response.status_code == 400
        assert response.json == {'Message': 'Enter valid booking id and center id'}


    def test_booking_status_for_users_before_approval(self):
        url = '/center/booking/status/1'
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == [{'user_id': 1, 'id': 1, 'testing_center_id': 1, 'status': True}]

    def test_request_booking_in_db_after_approval(self):
        bookings = Booking.query.all()
        assert len(bookings) == 1
        assert bookings[0].testing_center_id == 1
        assert bookings[0].status == True

    def test_booking_status_for_users_after_approval(self):
        url = '/center/booking/status/1'
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == [{'user_id': 1, 'status': True, 'id': 1, 'testing_center_id': 1}]

    def test_booking_status_for_users_failure(self):
        url = '/center/booking/status/12'
        response = self.client.get(url)
        assert response.status_code == 400
        assert response.json == {'Message': 'Enter a valid user id'}

class Test_UserAPI:

    client  = userapp.test_client()

    @pytest.fixture(autouse=True, scope='session')
    def setUp(self):
        # app.config['TESTING'] = True
        userapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.db'
        db.create_all()
        yield db
        db.drop_all()    

    def test_successful_registration(self):
        url = "/register"
        payload = "{\n\t\"username\": \"test01\",\n\t\"useremail\": \"user@test.com\",\n\t\"password\": \"test\"}"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        response = self.client.post(url, data=payload, headers=headers)
        assert response.status_code == 201
        assert response.json['Message'].strip() == 'Registration successful'
    
    def test_failed_registration(self):
        url = "/register"
        payload = "{\n\t\"username\": \"test01\",\n\t\"useremail\": \"user@test.com\",\n\t\"password\": \"test\"}"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        response = self.client.post(url, data=payload, headers=headers)
        assert response.status_code == 400
        assert response.json['Message'].strip() == 'Check the fields entered'

    def test_successful__user_login(self):
        valid_credentials = base64.b64encode(b'test01:test').decode('UTF-8')
        response = self.client.post('/login', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 200
        assert response.json['Message'].strip() == 'Login success'
        with self.client.session_transaction() as session:
            assert len(session)==2
            assert session['username'] == 'test01'
    
    def test_user_logout(self):
        url="/logout"
        response = self.client.post(url)
        assert response.status_code == 200
        assert response.json['Message'].strip() == 'Logout successful'
        with self.client.session_transaction() as session:
            assert len(session)==1
            
    def test_failed_user_login(self):
        valid_credentials = base64.b64encode(b'test01:test01').decode('UTF-8')
        response = self.client.post('/login', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 400
        assert response.json['Message'].strip() == 'Could not verify'
        with self.client.session_transaction() as session:
            assert len(session)==1
    
    def test_failed_user_logout(self):
        url="/logout"
        response = self.client.post(url)
        assert response.status_code == 400
        assert response.json['Message'].strip() == 'Already logged out'
        with self.client.session_transaction() as session:
            assert len(session)==1
    
class Test_UserAPI_calling_otherAPIs:
    client  = userapp.test_client()

    @pytest.fixture(autouse=True, scope='session')
    def setUp(self):
        # app.config['TESTING'] = True
        userapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.db'
        db.create_all()
        yield db
        db.drop_all()    

    def test_list_hospitals_without_login(self):
        url="/list/hospitals"
        response = self.client.get(url)
        assert response.status_code == 400
        assert response.json['Message'].strip() == 'Login to proceed'
        

    def test_list_hospitals_with_login(self):
        valid_credentials = base64.b64encode(b'test01:test').decode('UTF-8')
        response = self.client.post('/login', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 200

        url="/list/hospitals"
        response = self.client.get(url)
        #assert response.content == 'Login to proceed'
        assert response.status_code == 200

        self.client.post('/logout')
    
    def test_search_hospital_name_without_login(self):
        url="/search/hospital/1"
        response = self.client.get(url)
        assert response.status_code == 400
        assert response.json['Message'].strip() == 'Login to proceed'
    
    def test_list_all_centers_without_login(self):
        url="/list/centers"
        response = self.client.get(url)
        assert response.status_code == 400
        assert response.json['Message'].strip() == 'Login to proceed'
        
    def test_booking_center_without_login(self):
        url="/book/center"
        response = self.client.post(url)
        assert response.status_code == 400
        assert response.json['Message'].strip() == 'Login to proceed'

    def test_status_without_login(self):
        url = '/status'
        response = self.client.get(url)
        assert response.status_code == 400
        assert response.json['Message'].strip() == 'Login to proceed'

    def test_status_with_login(self):    
        valid_credentials = base64.b64encode(b'test01:test').decode('UTF-8')
        response = self.client.post('/login', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 200

        url = '/status'
        response = self.client.get(url)
        assert response.status_code == 200


class Test_ports_API:
    
    def test_testcenter_app(self):
        url="http://localhost:8003/"
        response = requests.get(url)
        assert response.json() == "Welcome to test center service"
 
    def test_hospital_app(self):
        url="http://localhost:8002/"
        response = requests.get(url)
        assert response.json() == "Welcome to hospital service"

    def test_user_app(self):
        url="http://localhost:8001/"
        response = requests.get(url)
        assert response.json() == "Welcome to user service"
    
  