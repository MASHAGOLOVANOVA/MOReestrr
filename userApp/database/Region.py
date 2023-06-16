from userApp import db


class Region(db.Model):
    __tablename__ = "region"
    id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False, default='Российская Федерация')

    clinics = db.relationship('Clinic', backref='region',  cascade="all,delete", lazy=True)
    dms = db.relationship('DecisionMaker', backref='region', cascade="all,delete", lazy=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'region_name': self.region_name,
            'country': self.country,
        }

    def __repr__(self):
        return '<Region %r>' % self.id
