from . import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    id_document = db.Column(db.String(20), unique=True, nullable=False)
    #fee_comission = db.Column(db.Float, nullable=False, default=0.0)
    #fee_ticket = db.Column(db.Integer, db.ForeignKey('service.id'))
    license_plate = db.relationship(
        'Vehicle', backref='plate', uselist=False)
    parking_usage = db.relationship(
        'Usage', backref='parking_log', lazy=True)

    def __repr__(self):
        return f"Person('{self.name}', '{self.id_document}')"


class Vehicle(db.Model):
    license_plate = db.Column(db.String(7), primary_key=True)
    vehicle_type = db.Column(db.String(1), nullable=False)
    owner_id_document = db.Column(db.Integer, db.ForeignKey('person.id_document'))
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('lot.id'))

    def __repr__(self):
        return f"Vehicle('{self.license_plate}', '{self.vehicle_type}')"


class Lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_available = db.Column(db.Boolean, nullable=False)
    lot_type = db.Column(db.String(1), nullable=False)
    vehicle_plate = db.relationship(
        'Vehicle', backref='vehicle_lot', uselist=False)

    def __repr__(self):
        return f"Lot('{self.id}', '{self.lot_type}, '{self.is_available}')"


# class Service(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#
#    total_hours = db.Column(db.Integer, nullable=False)
#    total_fee = db.Column(db.Float, nullable=False)
#
#    def __repr__(self):
#        return f"Service('{self.id}', '{self.total_hours}','{self.total_fee}')"


class Usage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    in_time = db.Column(db.DateTime, nullable=False)
    out_time = db.Column(db.DateTime)
    person_id_document = db.Column(
        db.Integer, db.ForeignKey('person.id_document'))
    total_charge = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f"Usage('{self.id}', '{self.in_time}', '{self.out_time}')"
