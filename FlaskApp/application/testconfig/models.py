from . import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	useremail = db.Column(db.String(80), nullable=False, default ="test")
	password = db.Column(db.String(80), nullable=False)
	bookings = db.relationship("Booking", cascade='all, delete-orphan', uselist=False, backref="User")	
	

class Hospital(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	hospitalname = db.Column(db.String(80), unique=True, nullable=False)
	location = db.Column(db.String(80), nullable=False)
	contact = db.Column(db.Integer, nullable=False)
	capacity = db.Column(db.Integer, nullable=False)
	test = db.relationship("Testcenter", cascade='all, delete-orphan', uselist=False, backref="Hospital")

	def serialize(self):
		return {"id": self.id, "hospitalname": self.hospitalname, "location": self.location,"capacity":self.capacity}

class Testcenter(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	testcenter_name = db.Column(db.String(80), unique=True, nullable=False)
	hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
	is_available = db.Column(db.Boolean, default=True)

	def serialize(self):
		return {"id": self.id,"testcenter_name":self.testcenter_name, "hospital_id": self.hospital_id , "is_available": self.is_available}

class Booking(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'),nullable=False)
	testing_center_id = db.Column(db.Integer, nullable=False)
	status = db.Column(db.Boolean,default=False)

	def serialize(self):
		return {"id": self.id,"user_id":self.user_id, "testing_center_id":self.testing_center_id, "status":self.status}
