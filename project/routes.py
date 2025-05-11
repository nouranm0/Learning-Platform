from flask import render_template, url_for, redirect, flash, session , request
from project.models import User, Category, Course, Enrollment, Subscription, Content, Progress, Review, Certificate
from project.forms import RegistrationForm, loginForm, contactForm , CourseForm, DeleteForm , EnrollmentForm
from datetime import datetime
from project import app, db, bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)

@login_manager.user_loader
def load_user(UserID):
    return User.query.get(int(UserID))


@app.route("/")
@app.route("/home")
def home():
    try:
        form = CourseForm()
        
        if not current_user.is_authenticated:
            return render_template("home.html",Ptitle="Home",courses=[],form=form)
        
        if current_user.Role == 'Instructor':
            courses = Course.query.filter_by(InstructorID=current_user.UserID).all()
            courses_data = [(c.CourseID, c.Title, c.Description, None) for c in courses]
        else:
            enrollments = Enrollment.query.filter_by(UserID=current_user.UserID).all()
            courses_data = [(e.course.CourseID, e.course.Title, e.course.Description, e.progress)for e in enrollments if e.course]
        
        return render_template("home.html",Ptitle="Home",courses=courses_data,form=form)
    
    except Exception as e:
        app.logger.error(f"Error in home route: {str(e)}")
        return render_template("home.html",Ptitle="Home",courses=[],form=CourseForm())

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
                Role=form.role.data,
                # Role=form.role.data,  # تم التعديل هنا
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

#/* Course Management Routes */
@app.route("/courses")
@login_required
def courses():
    courses = Course.query.all()
    return render_template("courses.html", Ptitle="Courses", courses=courses)

@app.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    enrollment = None
    user_review = None
    form = DeleteForm()  # Add this line
    
    if current_user.Role == 'Student':
        enrollment = Enrollment.query.filter_by(
            UserID=current_user.UserID, 
            CourseID=course_id
        ).first()
        user_review = Review.query.filter_by(
            UserID=current_user.UserID,
            CourseID=course_id
        ).first()
    
    return render_template(
        'course_detail.html',
        course=course,
        enrollment=enrollment,
        user_review=user_review,
        form=form  # Add form to template context
    )

# للتسجيل في الكورس (للطلاب)
@app.route('/enroll/<int:course_id>', methods=['GET', 'POST'])  # تأكد من وجود POST هنا
@login_required
def enroll(course_id):
    if current_user.Role != 'Student':
        flash('هذه الصفحة للطلاب فقط', 'danger')
        return redirect(url_for('course_detail', course_id=course_id))
    
    course = Course.query.get_or_404(course_id)
    form = EnrollmentForm()  # استخدم النموذج إذا كنت تستخدم Flask-WTF
    
    # التحقق من التسجيل المسبق
    if Enrollment.query.filter_by(UserID=current_user.UserID, CourseID=course_id).first():
        flash('أنت مسجل بالفعل في هذا الكورس', 'warning')
        return redirect(url_for('course_detail', course_id=course_id))
    
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_enrollment = Enrollment(
                UserID=current_user.UserID,
                CourseID=course_id,
                EnrollmentDate=datetime.utcnow()
            )
            
            new_progress = Progress(
                UserID=current_user.UserID,
                CourseID=course_id,
                CompPercent=0.0,
                LastUpdated=datetime.utcnow()
            )
            
            db.session.add(new_enrollment)
            db.session.add(new_progress)
            db.session.commit()
            
            flash('تم التسجيل بنجاح!', 'success')
            return redirect(url_for('course_detail', course_id=course_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    
    return render_template('enroll.html', course=course, form=form)

@app.route('/delete_course/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    form = DeleteForm()  # استخدم نموذجاً فارغاً للتحقق من CSRF
    
    if form.validate_on_submit():
        course = Course.query.get_or_404(course_id)
        if current_user.UserID != course.InstructorID:
            flash('فقط المدرب يمكنه حذف هذا الكورس', 'danger')
            return redirect(url_for('course_detail', course_id=course_id))
        
        db.session.delete(course)
        db.session.commit()
        flash('تم حذف الكورس بنجاح', 'success')
        return redirect(url_for('courses'))
    
    flash('فشل في الحذف: توكن الحماية غير صالح', 'danger')
    return redirect(url_for('course_detail', course_id=course_id))

@app.route("/my_courses")
@login_required
def my_courses():
    if current_user.Role == "Student":
        enrollments = Enrollment.query.filter_by(UserID=current_user.UserID).all()  # تم التعديل هنا
        courses = [enrollment.CourseID for enrollment in enrollments]
        return render_template("my_courses.html", Ptitle="My Courses", courses=courses)
    else:
        flash("Only students can view their courses.", "danger")
        return redirect(url_for('home'))
    
@app.route("/my_courses/<int:course_id>")
@login_required
def my_course_detail(course_id):
    if current_user.Role == "Student":
        course = Course.query.get_or_404(course_id)
        progress = Progress.query.filter_by(UserID=current_user.UserID, CourseID=course.CourseID).first()
        return render_template("my_course_detail.html", Ptitle=course.Title, course=course, progress=progress)
    else:
        flash("Only students can view their courses.", "danger")
        return redirect(url_for('home'))
    
@app.route('/add_course', methods=['GET', 'POST'])  # يجب أن يكون هكذا
@login_required
def add_course():
    form = CourseForm()  # إنشاء نموذج
    
    if form.validate_on_submit():
        new_course = Course(
            Title=form.title.data,
            Description=form.description.data,
            InstructorID=current_user.UserID,
            CategoryID=form.category.data,
            Price=form.price.data,
            
            )
        
        db.session.add(new_course)
        db.session.commit()
        flash('تم إضافة الكورس بنجاح!', 'success')
        return redirect(url_for('courses'))
    
    # إصلاح: تمرير المتغير form إلى القالب
    return render_template('add_course.html', form=form)
