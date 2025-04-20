from flask import render_template, url_for, redirect, flash, session
from project.models import User, Category, Course, Enrollment, Subscription, Content, Progress, Review, Certificate
from project.forms import RegistrationForm, loginForm, contactForm
from project import app, db, bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", Ptitle="Home", cssFile='main')

@app.route("/about")
def about():
    return render_template("about.html", Ptitle="About")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = contactForm()
    if form.validate_on_submit():
        flash("Message sent successfully", 'success')
        return redirect(url_for('home'))
    return render_template("contact.html", Ptitle="Contact", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(
                Username=form.username.data,
                Email=form.email.data,
                Password=hashed_password,
                Role="Student",
                FirstName=form.fname.data,  
                LastName=form.lname.data   
            )
            db.session.add(user)
            db.session.commit()
            flash(f"Account created successfully for {form.username.data}", "success")
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash("Registration failed. Username or Email may already be in use.", "danger")
            return render_template("register.html", Ptitle="Register", form=form)
    else:
        print(form.errors)  
    return render_template("register.html", Ptitle="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.Password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Login failed. Please check email or password.", "danger")
    return render_template("login.html", Ptitle="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", Ptitle="Profile", user=current_user)