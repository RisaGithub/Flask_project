import flask
from flask import render_template, request, abort, redirect

from admin.admin_forms import CourseForm, TopicForm
from data import db_session
from data.account import Account
from data.course import Course, Topic

admin = flask.Blueprint(
    'admin_api',
    __name__,
    template_folder='templates_admin'
)


@admin.route('/')
def index():
    return render_template("base_admin.html")


@admin.route("/users_data")
def users_data():
    db_sess = db_session.create_session()
    all_accounts = db_sess.query(Account).all()
    return render_template("users_data_admin.html", all_accounts=all_accounts)


@admin.route('/all_courses', methods=['GET', 'POST'])
def all_courses():
    db_sess = db_session.create_session()
    all_courses = db_sess.query(Course).all()
    return render_template("all_courses_admin.html", all_courses=all_courses)


@admin.route('/all_courses/<int:course_id>', methods=['GET', 'POST'])
@admin.route('/all_courses/<int:course_id>/topics', methods=['GET', 'POST'])
def course(course_id):
    # find course in db
    db_sess = db_session.create_session()
    course = db_sess.query(Course).filter(Course.id == course_id).first()

    if not course:
        # not found error
        abort(404)

    if request.method == "GET":
        return render_template('course_admin.html', course=course)


@admin.route('/all_courses/add_course', methods=['GET', 'POST'])
def add_course():
    form = CourseForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # form data
            name = form.name.data
            # add course to db
            db_sess = db_session.create_session()
            course = Course()
            course.name = name
            db_sess.add(course)
            db_sess.commit()
            # go to previews page after adding
            return redirect('/admin/all_courses')
    else:
        return render_template('add_or_edit_course.html', form=form)


@admin.route('/all_courses/<int:course_id>/edit_course', methods=['GET', 'POST'])
def edit_course(course_id):
    form = CourseForm()
    # find course in db
    db_sess = db_session.create_session()
    course = db_sess.query(Course).filter(Course.id == course_id).first()

    if not course:
        # not found error
        abort(404)

    if request.method == "POST":
        if form.validate_on_submit():
            course.name = form.name.data
            db_sess.commit()
            # go to previews page after editing
            return redirect('/admin/all_courses')
    else:
        # add current data of course to form
        form.name.data = course.name
        return render_template('add_or_edit_course.html', form=form)


@admin.route('/all_courses/<int:course_id>/delete_course', methods=['GET', 'POST'])
def delete_course(course_id):
    db_sess = db_session.create_session()
    # find course in db
    course = db_sess.query(Course).filter(Course.id == course_id).first()

    if not course:
        # not found error
        abort(404)

    if request.method == "GET":
        db_sess.delete(course)
        db_sess.commit()
        return redirect('/admin/all_courses')


@admin.route('/all_courses/<int:course_id>/topics/add_topic', methods=['GET', 'POST'])
def add_topic(course_id):
    form = TopicForm()
    db_sess = db_session.create_session()
    # find course in db
    course = db_sess.query(Course).filter(Course.id == course_id).first()
    if request.method == "POST":
        if form.validate_on_submit():
            # form data
            name = form.name.data
            content = form.content.data
            # add topic to db
            topic = Topic()
            topic.name = name
            topic.content = content
            db_sess.add(topic)
            # add topic to course
            course.topics.append(topic)
            db_sess.commit()
            # go to previews page after adding
            return redirect(f'/admin/all_courses/{course_id}/topics')
    else:
        return render_template('add_or_edit_topic.html', form=form, course=course)


@admin.route('/all_courses/<int:course_id>/topics/<int:topic_id>/edit_topic', methods=['GET', 'POST'])
def edit_topic(course_id, topic_id):
    form = TopicForm()
    db_sess = db_session.create_session()
    # find course and topic in db
    course = db_sess.query(Course).filter(Course.id == course_id).first()
    topic = db_sess.query(Topic).filter(Topic.id == topic_id).first()

    if not topic:
        # not found error
        abort(404)

    if request.method == "POST":
        if form.validate_on_submit():
            topic.name = form.name.data
            db_sess.commit()
            # go to previews page after editing
            return redirect(f'/admin/all_courses/{course_id}/topics')
    else:
        # add current data of course to form
        form.name.data = topic.name
        form.content.data = topic.content
        return render_template('add_or_edit_topic.html', form=form, course=course, topic=topic)


@admin.route('/all_courses/<int:course_id>/topics/<int:topic_id>/delete_topic', methods=['GET', 'POST'])
def delete_topic(course_id, topic_id):
    db_sess = db_session.create_session()
    # find topic in db
    topic = db_sess.query(Topic).filter(Topic.id == topic_id).first()

    if not topic:
        # not found error
        abort(404)

    if request.method == "GET":
        db_sess.delete(topic)
        db_sess.commit()
        return redirect(f'/admin/all_courses/{course_id}/topics')
