from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from data import db_session
from data.course import Course, Topic
from data.user import User
from data.account import Account

from admin import admin_api
from forms.forms import RegisterForm, LoginForm

from datetime import timedelta


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = "614984"
app.permanent_session_lifetime = timedelta(days=1)


@login_manager.user_loader
def load_user(account_id):
    db_sess = db_session.create_session()
    return db_sess.query(Account).get(account_id)


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return render_template("need_logout_error.html")

    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            email = form.email.data
            nickname = form.nickname.data
            # find user and account in db
            user = db_sess.query(User).filter(User.email == email).first()
            account = db_sess.query(Account).filter(Account.user_id == user.id,
                                                    Account.nickname == nickname).first() if user else None
            # if account already in db
            if account:
                return render_template('register.html', form=form, message="This account already exists")
            else:
                # if user not in db (email not in db)
                if not user:
                    # add user to db
                    user = User()
                    user.email = form.email.data
                    db_sess.add(user)
                # add account to db
                account = Account()
                account.nickname = form.nickname.data
                account.set_password(form.password.data)
                account.user = user
                db_sess.add(account)
                # add account to user
                user.accounts.append(account)
                db_sess.commit()
                # login user
                login_user(account)
                return redirect('/courses')
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template("need_logout_error.html")

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            email = form.email.data
            nickname = form.nickname.data
            password = form.password.data
            # find user and account in db
            user = db_sess.query(User).filter(User.email == email).first()
            account = db_sess.query(Account).filter(Account.user_id == user.id,
                                                    Account.nickname == nickname).first() if user else None
            # if account in db and password is right
            if account and account.check_password(password):
                # login
                login_user(account, remember=form.remember_me.data)
                # go to home page after login
                return redirect("/courses")
            else:
                # error messages
                # if account in db, but password incorrect
                if account and not account.check_password(password):
                    return render_template('login.html', message="Incorrect password", form=form)
                # if user(email) in db, but account(nickname) not in db
                elif user and not account:
                    return render_template('login.html', message="Incorrect nickname", form=form)
                # if user(email) not in db
                else:
                    return render_template('login.html', message="This account doesn't exist. Register before login",
                                           form=form)
    else:
        return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        # logout user
        logout_user()
        # go to login page after user logged out
        return redirect("/login")
    else:
        return redirect("/")


@app.route("/courses")
def courses():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        all_courses = db_sess.query(Course).all()
        account_courses = current_user.courses
        return render_template("courses.html",
                               account=current_user,
                               account_courses=account_courses,
                               all_courses=all_courses)
    else:
        # go to login page if user isn't logged out
        return redirect("/login")


@app.route('/courses/<int:course_id>', methods=['GET', 'POST'])
def course(course_id):
    # find course in db
    db_sess = db_session.create_session()
    course = db_sess.query(Course).filter(Course.id == course_id).first()

    if not course:
        # not found error
        abort(404)

    if request.method == "GET":
        return render_template('course.html', course=course)


@app.route('/courses/<int:course_id>/topics/<int:topic_id>', methods=['GET', 'POST'])
def topic(course_id, topic_id):
    # find course and topic in db
    db_sess = db_session.create_session()
    course = db_sess.query(Course).filter(Course.id == course_id).first()
    topic = db_sess.query(Topic).filter(Topic.id == topic_id).first()

    if not course or not topic:
        # not found error
        abort(404)

    if request.method == "GET":
        return render_template('topic.html', course=course, topic=topic)


if __name__ == "__main__":
    db_session.global_init("db/blogs.db")
    # register blueprints
    app.register_blueprint(admin_api.admin, url_prefix="/admin")
    app.run(debug=True)
