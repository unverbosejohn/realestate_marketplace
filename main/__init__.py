"""This module starts a web server on http://127.0.0.1:5000 a simple back-end portal for a real estate listing management system"""

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    session,
    request,
    g,
    jsonify)

import json
import property
import usr
import logger
import data

app = Flask(__name__)
app.secret_key = '2kF?EYjb8HCR9TKzD)XOKn=BltW=wQ'  # TODO: Change this for a production environment


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in usr.users if x.user_id == session['user_id']][0]
        g.user = user


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']

        if username and password:

            try:
                global user
                user = [u for u in usr.users if u.username == username and u.password == password][0]

            except IndexError:
                session['username'] = ''
                return render_template('login.html', error='Λάθος Στοιχεία')

            if user:
                session['user_id'] = user.user_id
                session['username'] = username
                user.logged_in = True
                user.get_properties()
                return redirect(url_for('profile'))

    return render_template('login.html')


@app.route('/getProps', methods=['POST'])
def getProps():
    try:
        if user.logged_in:
            data = {}

            for prop_id, prop in user.properties.items():
                data[prop_id] = ', '.join(prop.listify())
            return data

        else:
            return redirect(url_for('index'))

    except NameError:
        return redirect(url_for('index'))


@app.route('/saveProp', methods=['POST'])
def saveProp():

    try:
        if not session['user_id'] == user.user_id or not user.logged_in:
            return redirect(url_for('index'))

    except NameError:
        return redirect(url_for('index'))

    try:
        if user.logged_in:
            price = request.form['price']
            city = request.form['city']
            avail = request.form['avail']
            area = request.form['area']

            dinput = [price, city, avail, area]
            if not all(dinput):
                return jsonify({'err': 'Άδεια πεδία'}), 300, {'ContentType': 'application/json'}

            if not all(list(map(data.is_int, dinput))):
                return jsonify({'err': 'Μόνο αριθμητικές τιμές είναι αποδεκτές για τα πεδία:\n Τιμή, Τετραγωνικά'}), 300, {'ContentType': 'application/json'}

            prop = property.Property(
                user_id=user.user_id,
                loc_id=city,
                avail_id=avail,
                price=price,
                area=area
            )
            result = prop.save()

            if result[0]:
                while True:
                    if prop.stored:
                        user.properties[prop.prop_id] = prop
                        break

            else:
                del prop
                if result[1] == 0:
                    return jsonify({'err': 'Λάθος Τιμή!'}), 300, {'ContentType': 'application/json'}
                if result[1] == 3:
                    return jsonify({'err': 'Λάθος Εμβαδόν'}), 300, {'ContentType': 'application/json'}
                return 'bad data'
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

        else:
            return redirect(url_for('index'))

    except NameError:
        return redirect(url_for('index'))


@app.route('/delprop', methods=['POST'])
def delprop():

    if request.method == "POST":

        try:
            if not session['user_id'] == user.user_id or not user.logged_in:
                return redirect(url_for('index'))
        except NameError:
            return redirect(url_for('index'))

        del_id = request.form['del_id']

        if int(del_id) not in list(user.properties.keys()):
            return json.dumps({'success': False}), 300, {'ContentType': 'application/json'}

        logger.log(f'Deleted property with id {del_id}')

        return json.dumps({'success':True}), 200, {'ContentType': 'application/json'}


@app.route('/profile', methods=['GET', 'POST'])
def profile():

    try:
        if not session['user_id'] == user.user_id or not user.logged_in:
            return redirect(url_for('index'))
    except NameError:
        return redirect(url_for('index'))

    return render_template(
        'profile.html',
        user=str(g.user.username).title(),
        cities=data.cities,
        avail=data.availability,
    )


if __name__ == '__main__':
    app.run(debug=True)
