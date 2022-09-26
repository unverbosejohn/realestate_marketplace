from flask import Flask, render_template, redirect, url_for, session, request
import usr
import flask_bootstrap

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST' and request.form['username'] and request.form['password']:
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']

            global user
            user = usr.User(email=username, pwd=password)

            if user.login():
                session['logged_in'] = True
                return redirect(url_for('profile'))

            else:
                return render_template('login.html', error='Wrong Email or Password')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def new():
    # New user method
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        password_conf = request.form['password_conf']

        if password != password_conf:
            return render_template('register.html', pwd_error='Password mismatch!')

        else:
            global user
            user = usr.User(email=username, pwd=password)
            user.first_name = first_name
            user.last_name = last_name
            registration = user.register()

            if registration[0]:
                return redirect(url_for('profile'))

            elif registration[1] == 'user':
                return render_template('register.html', user_error='Email exists!')

            elif registration[1] == 'fields':
                return render_template('register.html', fields_error='Please fill all fields')

    return render_template('register.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if session['logged_in']:
        print(session)
        if request.method == 'POST':
            if request.form[''] == 'logout':
                user.logout()
                session['logged_in'] = False
                print(session['logged_in'])
                return redirect(url_for('index'))
        return render_template('profile.html', first_name=user.first_name, last_name=user.last_name)

    # return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
