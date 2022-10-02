"""This module starts a web server on http://127.0.0.1:5000 a simple back-end portal for a real estate listing management system"""
import flask
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    session,
    request,
    g,
    jsonify)
import gunicorn
import json
import property
import messages
import usr
import logger
import data

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '2kF?EYjb8HCR9TKzD)XOKn=BltW=wQ'  # TODO: Change this for a production environment


@app.before_request
def before_request():
    g.user = None

    try:
        if session['username']:
            logger.log(f'Session found: {session["username"]}')
            g.user = usr.User(session.get('username'), '')
            g.user.get_details()
            g.user.get_properties()

    except KeyError:
        pass

@app.route('/', methods=['GET', 'POST'])
def index():

    try:
        if session.get('user_id') and g.user.logged_in:
            # assume the user is logged in and build user class
            return redirect(url_for('profile'))

    except AttributeError:
        pass

    if request.method == 'POST':
        session.pop('username', None)
        username = request.form['username']
        password = request.form['password']

        if username and password:
            g.user = usr.User(username=username, pwd=password)
            if g.user.login():
                session['username'] = g.user.username
                session['user_id'] = g.user.user_id
                g.user.get_properties()
                return redirect(url_for('profile'))

            else:
                session['username'] = ''
                return render_template('login.html', error=messages.wrong_cred)

    return render_template('login.html')


@app.route('/getProps', methods=['POST'])
def getProps():
    try:
        if g.user.logged_in:
            data = {}

            for prop_id, prop in g.user.properties.items():
                data[prop_id] = ', '.join(prop.listify())
            return data

        else:
            return redirect(url_for('index'))

    except NameError:
        return redirect(url_for('index'))


@app.route('/saveProp', methods=['POST'])
def saveProp():

    try:
        if not session['user_id'] == g.user.user_id or not g.user.logged_in:
            return redirect(url_for('index'))

    except NameError:
        return redirect(url_for('index'))

    try:
        if g.user.logged_in:
            price = request.form['price']
            city = request.form['city']
            avail = request.form['avail']
            area = request.form['area']

            dinput = [price, city, avail, area]
            if not all(dinput):
                return jsonify({'err': messages.empty_fields}), 300, {'ContentType': 'application/json'}

            if not all(list(map(data.is_int, dinput))):
                return jsonify({'err': messages.numeric_only}), 300, {'ContentType': 'application/json'}

            prop = property.Property(
                user_id=g.user.user_id,
                loc_id=city,
                avail_id=avail,
                price=price,
                area=area
            )
            result = prop.save()

            if result[0]:
                while True:
                    if prop.stored:
                        g.user.properties[prop.prop_id] = prop
                        break

            else:
                del prop
                if result[1] == 0:
                    return jsonify({'err': messages.wrong_price}), 300, {'ContentType': 'application/json'}
                if result[1] == 3:
                    return jsonify({'err': messages.wrong_area}), 300, {'ContentType': 'application/json'}
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
            if not session['user_id'] == g.user.user_id or not g.user.logged_in:
                return redirect(url_for('index'))
        except NameError:
            return redirect(url_for('index'))

        del_id = request.form['del_id']

        if int(del_id) not in list(g.user.properties.keys()):
            return json.dumps({'success': False}), 300, {'ContentType': 'application/json'}

        g.user.del_property(int(del_id))
        logger.log(f'Deleted property with id {del_id}')

        return json.dumps({'success':True}), 200, {'ContentType': 'application/json'}


@app.route('/profile', methods=['GET', 'POST'])
def profile():

    try:
        if not session['user_id'] == g.user.user_id or not g.user.logged_in:
            return redirect(url_for('index'))
    except AttributeError:
        return redirect(url_for('index'))

    return render_template(
        'profile.html',
        user=str(g.user.username).title(),
        cities=data.cities,
        avail=data.availability,
    )


@app.route('/logout')
def logout():
    logger.log(f'Logging out {session["username"]}')
    del session['username']
    del g.user
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
