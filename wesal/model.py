from datetime import datetime 
from wesal import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    phone_number = db.Column(db.String(14), primary_key=True, nullable=False)
    email = db.Column(db.String(125), unique=True)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password_hash = db.Column(db.String(60), nullable=False)
    password_salt = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.Boolean, default=False, nullable=False)  # Assuming True for Male and False for Female
    birth_date = db.Column(db.DateTime, nullable=False)
    user_role = db.Column(db.String(20), nullable=False, default="Normal")
    #last_login = db.Column(db.DateTime, nullable=False)
    #created_at = db.Column(db.DateTime, nullable=False)
    favorites = db.relationship("Favorite", backref="user.id", lazy=True)
    #Course = db.relationship("Course", backref="user.id", lazy=True)
    def __repr__(self):
        return f"User('{self.username}', '{self.phone_number}', '{self.email}', '{self.user_role}', '{self.last_login}', '{self.created_at}', '{self.image_file}')"

class Temp_User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    phone_number = db.Column(db.String(14), primary_key=True, nullable=False)
    email = db.Column(db.String(125), unique=True)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password_hash = db.Column(db.String(60), nullable=False)
    password_salt = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.Boolean, default=False, nullable=False)  # Assuming True for Male and False for Female
    birth_date = db.Column(db.DateTime, nullable=False)
    user_role = db.Column(db.String(20), nullable=False, default="Normal")
    favorites = db.relationship("Favorite", backref="user_id", lazy=True)
    enrolled_course=db.relationship("Enrolled_Courses", backref="user", lazy=True)
    completed_course=db.relationship("Completed_Courses", backref="user", lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.phone_number}', '{self.email}', '{self.user_role}', '{self.last_login}', '{self.created_at}', '{self.image_file}')"

class Course(db.Model):
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(150), nullable=False)
    icon = db.Column(db.String(20), nullable=False, default="default_icon.jpg")
    lessons = db.relationship("Lesson", backref="course", lazy=True)
    enrolled_course=db.relationship("Enrolled_Courses", backref="course", lazy=True)
    completed_course=db.relationship("Completed_Courses", backref="course", lazy=True)
    
    def __repr__(self):
        return f"Course('{self.title}', '{self.description}', '{self.icon}', '{self.lessons}', '{self.phone_number}', '{self.phone_number}', '{self.user_id}')"
class Enrolled_Courses (db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    course = db.relationship("Course", backref="enrolled_course", foreign_keys=[course_id], lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="enrolled_course", foreign_keys=[user_id], lazy=True)
class Completed_Courses (db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    course = db.relationship("Course", backref="completed_course", foreign_keys=[course_id], lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="completed_course", foreign_keys=[user_id], lazy=True)

class Lesson(db.Model):
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String(20), nullable=True, default="default_thumbnail.jpg")
    video = db.Column(db.String(255), nullable=True)
    documentation = db.Column(db.LargeBinary, nullable=True)
    duration = db.Column(db.Interval, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    course = db.relationship("Course", backref="lessons", foreign_keys=[course_id], lazy=True)
    
    def __repr__(self):
        return f"Lesson('{self.title}', '{self.date_posted}', '{self.description}', '{self.video}', '{self.duration}', '{self.course_id}')"
    
class Favorite(db.Model):
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    text = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="favorites", foreign_keys=[user_id], lazy=True)
    
    def __repr__(self):
        return f"Lesson('{self.text}', '{self.user_id}')"

class Verify(db.Model):
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Phone_number = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"Lesson('{self.Phone_number}', '{self.code}')"
    
from wesal import app,db
with app.app_context():
    db.create_all()