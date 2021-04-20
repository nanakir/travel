from flights import db

class Qpxflightdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.String(80))
    flightid = db.Column(db.String(10))
    leg = db.Column(db.String(10))
    departuret = db.Column(db.String(20))
    arrivalt = db.Column(db.String(20))
    origin = db.Column(db.String(10))
    destination = db.Column(db.String(10))
    cabin = db.Column(db.String)
    carrier = db.Column(db.String(20))

    category_id = db.Column(db.Integer, db.ForeignKey('qpxflight.id'))
    qpxflight = db.relationship('Qpxflight', backref=db.backref('flights', lazy='dynamic'))

    def __init__(self, price, flightid, leg, departuret, arrivalt, origin, destination, cabin, carrier, qpxflight):
        self.price = price 
        self.flightid = flightid
        self.leg = leg
        self.departuret = departuret
        self.arrivalt = arrivalt 
        self.origin = origin 
        self.destination = destination 
        self.cabin = cabin 
        self.carrier = carrier
        self.qpxflight = qpxflight

    def __repr__(self):
        return '<Qpxflightdata%r>' % self.flightid

class Qpxflight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Flight Number %r>' % self.name

class Qpxiata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iata = db.Column(db.String(200))
    description = db.Column(db.String(200))

    def __init__(self, iata, description):
        self.iata = iata
        self.description = description

    def ___repr__(self):
        return '<Airport Code %r>' % self.iata
