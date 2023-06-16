from userApp import db


class DecisionMaker(db.Model):
    __tablename__ = "decision_maker"
    dm_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    position = db.Column(db.Text)
    dm_region = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    dm_phone = db.Column(db.Text)
    dm_site = db.Column(db.Text)
    dm_mail = db.Column(db.Text)
    dm_tg = db.Column(db.Text)
    dm_ok = db.Column(db.Text)
    dm_vk = db.Column(db.Text)
    dm_facebook = db.Column(db.Text)

    def __repr__(self):
        return '<DecisionMaker %r>' % self.dm_id