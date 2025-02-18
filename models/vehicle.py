from database import db

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.String(20), nullable=False)

    def __init__(self, license_plate, vehicle_type, brand, owner, registration_date):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.brand = brand
        self.owner = owner
        self.registration_date = registration_date
