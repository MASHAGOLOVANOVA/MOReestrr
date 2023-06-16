from userApp import db


class Clinic(db.Model):
    __tablename__ = "clinic"
    clinic_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    short_name = db.Column(db.Text)
    leader = db.Column(db.Text)
    is_private = db.Column(db.Boolean)
    clinic_region = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    clinic_legal_address = db.Column(db.Text)
    inn = db.Column(db.String(10), nullable=False)
    phone_numbers = db.Column(db.Text)
    mail = db.Column(db.Text)
    nets = db.Column(db.Text)
    specialization = db.Column(db.Text)
    partner = db.Column(db.Boolean,default=False)

    def serialize(self):
        return{
            'clinic_id': self.clinic_id,
        'name':self.name,
        'short_name': self.short_name,
        'leader': self.leader,
        'is_private': self.is_private,
       'clinic_region': self.clinic_region,
        'clinic_legal_address': self.clinic_legal_address,
        'inn': self.inn,
        'phone_numbers': self.phone_numbers,
        'mail': self.mail,
        'nets': self.nets,
        'specialization': self.specialization,
        'partner': self.partner
        }

    def __repr__(self):
        return '<Clinic %r>' % self.clinic_id
