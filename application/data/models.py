from . import db

#Put your code here and use the serializers given below

# 	def serialize(self):
# 		return {"id": self.id, "hospitalname": self.hospitalname, "location": self.location,"capacity":self.capacity}

	# def serialize(self):
	# 	return {"id": self.id,"testcenter_name":self.testcenter_name, "hospital_id": self.hospital_id , "is_available": self.is_available}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    useremail = db.Column(db.String(80), nullable=False, default="test")
    password = db.Column(db.String(80), nullable=False)
    bookings = db.relationship("Booking", cascade='all, delete-orphan', uselist=False, backref="User")

    def __init__ (self,username, useremail, password):
        self.username = username
        self.useremail = useremail
        self.password = password

    @property
    def serialize(self):
        return {"id": self.id,"username":self.username, "useremail":self.useremail}


class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospitalname = db.Column(db.String(80), unique=True, nullable=False)
    location = db.Column(db.String(80), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    test = db.relationship("Testcenter", cascade='all, delete-orphan', uselist=False, backref="Hospital")

    def __init__ (self,hospitalname, location, contact,capacity):
        self.hospitalname = hospitalname
        self.location = location
        self.contact = contact
        self.capacity = capacity

    @property
    def serialize(self):
        return {"id": self.id, "hospitalname": self.hospitalname, "location": self.location, "capacity": self.capacity, "contact": self.contact}


class Testcenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    testcenter_name = db.Column(db.String(80), unique=True, nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
    is_available = db.Column(db.Boolean, default=True)

    def __init__ (self,testcenter_name, hospital_id, is_available):
        self.testcenter_name = testcenter_name
        self.hospital_id = hospital_id
        self.is_available = is_available

    @property
    def serialize(self):
        return {"id": self.id, "testcenter_name": self.testcenter_name, "hospital_id": self.hospital_id,
                "is_available": self.is_available}


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hospital_id = db.Column(db.Integer,nullable=False)
    testing_center_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=False)

    def __init__ (self,user_id, hospital_id, testing_center_id,status):
        self.user_id = user_id
        self.hospital_id = hospital_id
        self.testing_center_id = testing_center_id
        self.status = status

    @property
    def serialize(self):
        return {"id": self.id, "user_id": self.user_id, "testing_center_id": self.testing_center_id,
                "status": self.status}

