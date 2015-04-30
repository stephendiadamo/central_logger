from flask import Flask, request, session, redirect, url_for, \
    render_template, flash
import requests

app = Flask(__name__)

app.config.update(dict(
    USERNAME='admin',
    PASSWORD='admin'
))

API_URI = 'http://localhost:5000/logger/api/v1.0/'


@app.route('/')
def landing_page():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Logged in')
            return redirect(url_for('add_log'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/add_log', methods=['GET', 'POST'])
def add_log():
    error = None
    if request.method == 'POST':
        if not 'log_type' in request.form:
            error = 'Missing log type information'
        elif request.form['event_type'] is None:
            error = 'Missing event type information'
        elif request.form['application'] is None:
            error = 'Missing application information'
        else:
            data = {
                'log_type': request.form['log_type'],
                'event_type': request.form['event_type'],
                'application': request.form['application']
            }
            if 'occurred_at' in request.form:
                data['occurred_at'] = request.form['occurred_at']
            if 'description' in request.form:
                data['description'] = request.form['description']
            if 'log_message' in request.form:
                data['log_message'] = request.form['log_message']

            result = requests.post(API_URI + 'logs', json=data)
            if 'error' in result.json()['result']:
                flash('Failed to log error')
            else:
                flash('Successfully logged error with id: ' + str(result.json()['result']['id']))
                return redirect(url_for('add_log'))
    return render_template('add_log.html', error=error)


@app.route('/view_logs', methods=['GET'])
def view_logs():
    data_filter = None
    if 'filter' in request.args:
        data_filter = request.args['filter']
    result = requests.get(API_URI + 'get_logs', json={'filter': data_filter})
    return render_template('view_logs.html', data=result.json())


if __name__ == '__main__':
    app.secret_key = 'abcdefggggg'
    app.run(port=5050, debug=True)
