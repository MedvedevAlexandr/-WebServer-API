from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

# from forms.news import NewsForm
from forms.user import RegisterForm, LoginForm
from data.users import User
from data.inquiry import Inquiry
from data.klass import Klass
from data.schools import Schools
from forms.addschools import AddSchoolsForm
from data.student import Student
from data.users_profile import UsersProfile

from data import db_session

# роли пользователей:
# 1) admin
# 2) director
# 3) student
# 4) none - простой пользователь, который может запросить получение разных прав
# 5) aplication_director - статус при подаче заявлегния на директора
# 6) aplication_student - статус при подаче заявления на ученика

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/DataBase.db")
    app.run(debug=True)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    schools = db_sess.query(Schools)
    directors = db_sess.query(User)
    return render_template("index.html", schools=schools)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            apprentice=form.apprentice.data,
            patronymic=form.patronymic.data,
            email=form.email.data,
            # about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add-student', methods=['GET', 'POST'])
@login_required
def add_student():
    pass


@app.route('/add_director', methods=['GET', 'POST'])
@login_required
def add_director():
    if current_user.roles == 'admin':
        form = AddSchoolsForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(
                User.id == int(form.id.data)).first()
            user.roles = 'director'
            school = db_sess.query(Schools).filter(
                Schools.name_schools == form.name.data).first()
            school.director = int(form.id.data)
            db_sess.commit()
        return render_template('add_director.html', form=form)
    else:
        return render_template('admin_authorization_error.html')


@app.route('/profile')
def porfile():
    return render_template("profile.html")


@app.route("/school/<int:id>")
def school_info(id):
    db_sess = db_session.create_session()
    school = db_sess.query(Schools).filter(Schools.id == id).first()
    director = db_sess.query(User).filter(User.id == school.director).first()
    return render_template("school.html", school=school, director=director)


@app.route("/homework")
def students_homework():
    return render_template("homework.html")


@app.route("/schedule")
def stundents_schedule():
    return render_template("schedule.html")


@app.route("/marks")
def students_marks():
    return render_template("marks.html")


if __name__ == '__main__':
    main()
