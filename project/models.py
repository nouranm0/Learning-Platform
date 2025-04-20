from datetime import datetime
from project import db
from flask_login import UserMixin


class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(255), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Role = db.Column(db.String(50), nullable=False)
    FirstName = db.Column(db.String(255), nullable=True)
    LastName = db.Column(db.String(255), nullable=True)

    enrollments = db.relationship('Enrollment', backref='user', lazy=True)
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)
    progress = db.relationship('Progress', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    certificates = db.relationship('Certificate', backref='user', lazy=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.UserID)

    def __repr__(self):
        return f"User({self.Username}, {self.Email}, {self.Role})"
class Category(db.Model):
    CategoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False, unique=True)
    Description = db.Column(db.Text)
    courses = db.relationship('Course', backref='category', lazy=True)
    def __repr__(self):
        return f"Category({self.Name})"

class Course(db.Model):
    CourseID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    InstructorID = db.Column(db.Integer, nullable=False)
    CategoryID = db.Column(db.Integer, db.ForeignKey('category.CategoryID'), nullable=False)
    CreatedDate = db.Column(db.DateTime, nullable=False)
    Price = db.Column(db.Float, nullable=False)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    subscriptions = db.relationship('Subscription', backref='course', lazy=True)
    progress = db.relationship('Progress', backref='course', lazy=True)
    reviews = db.relationship('Review', backref='course', lazy=True)
    certificates = db.relationship('Certificate', backref='course', lazy=True)
    contents = db.relationship('Content', backref='course', lazy=True)
    def __repr__(self):
        return f"Course({self.Title}, {self.Price})"

class Enrollment(db.Model):
    EnrollmentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    CourseID = db.Column(db.Integer, db.ForeignKey('course.CourseID'), nullable=False)
    EnrollmentDate = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return f"Enrollment(User {self.UserID}, Course {self.CourseID})"

class Subscription(db.Model):
    SubsID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    CourseID = db.Column(db.Integer, db.ForeignKey('course.CourseID'), nullable=False)
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)
    Status = db.Column(db.String(50), nullable=False)
    PaymentAmount = db.Column(db.Float, nullable=False)
    def __repr__(self):
        return f"Subscription(User {self.UserID}, Course {self.CourseID}, Status {self.Status})"

class Content(db.Model):
    ContentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseID = db.Column(db.Integer, db.ForeignKey('course.CourseID'), nullable=False)
    Title = db.Column(db.String(255), nullable=False)
    Type = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return f"Content({self.Title}, {self.Type})"

class Progress(db.Model):
    ProgressID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    CourseID = db.Column(db.Integer, db.ForeignKey('course.CourseID'), nullable=False)
    CompPercent = db.Column(db.Float, nullable=False)
    LastUpdated = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return f"Progress(User {self.UserID}, Course {self.CourseID}, {self.CompPercent}%)"

class Review(db.Model):
    ReviewID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    CourseID = db.Column(db.Integer, db.ForeignKey('course.CourseID'), nullable=False)
    Rating = db.Column(db.Integer, nullable=False)
    Comment = db.Column(db.Text, nullable=True)
    ReviewDate = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return f"Review(User {self.UserID}, Course {self.CourseID}, Rating {self.Rating})"

class Certificate(db.Model):
    CertificateID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    CourseID = db.Column(db.Integer, db.ForeignKey('course.CourseID'), nullable=False)
    IssueDate = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return f"Certificate(User {self.UserID}, Course {self.CourseID})"