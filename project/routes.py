from flask import render_template,  url_for,redirect,flash
from project.forms import RegistrationForm, loginForm , contactForm
from project import app

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", Ptitle = "Home", cssFile='main')

@app.route("/about")
def about():
    return render_template("about.html", Ptitle = "About" )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = contactForm()
    if form.validate_on_submit():
        flash(f"message send successfully",'success')
        return redirect(url_for('home'))
    return render_template("contact.html", Ptitle = "Contact",form =form )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"account created successfully for {form.fname.data}",'success')
        return redirect(url_for('home'))
    return render_template("register.html" ,Ptitle = "Register" ,form = form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = loginForm()
    if form.validate_on_submit():
        flash(f"login successfully ",'success')
        return redirect(url_for('home'))
    return render_template("login.html" ,Ptitle = "Login" ,form = form)

