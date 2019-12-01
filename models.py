from db_instance import db

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pooper_name = db.Column(db.String(600),nullable=False)
    poop_date = db.Column(db.String(600),nullable=False)
    