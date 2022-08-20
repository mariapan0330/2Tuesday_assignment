from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash as gen_pw, check_password_hash as check_pw
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    contacts = db.relationship('Contact', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
    # has to have kwargs ability and call super with the kwargs
        super().__init__(**kwargs)
        self.set_password(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.user_id} | {self.username}>"
    
    def check_password(self, pw):
        # returns true if self.password == the password they put in
        return check_pw(self.password, pw)

    def set_password(self, pw):
        self.password = gen_pw(pw)



@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class Contact(db.Model):
    contact_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(10))
    address = db.Column(db.String(200))
    notes = db.Column(db.String(500))
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()
    

    def __repr__(self):
        return f"<Contact {self.contact_id} | {self.name}>"
    

    def update(self, **kwargs):
        for key, val in kwargs.items():
            if key in {'name', 'phone','address','notes'}:
                setattr(self, key, val)
        db.session.commit() # so the database changes as well 


    def delete(self):
        db.session.delete(self)
        db.session.commit()