from flask import Flask, request, redirect, url_for, \
    render_template, flash
import requests

app = Flask(__name__)
API_URI = 'http://localhost:5000/logger/api/v1.0/'


@app.route('/')
def landing_page():
    """
    Return the main page
    """
    return render_template('add_log.html')


@app.route('/add_log', methods=['GET', 'POST'])
def add_log():
    """
    Add a single log entry.
    """
    error = None
    if request.method == 'POST':
        if 'log_type' not in request.form:
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

            try:
                result = requests.post(API_URI + 'logs', json=data)
                if 'error' in result.json()['result']:
                    flash('Failed to log')
                else:
                    flash('Successfully logged')
            except requests.ConnectionError:
                flash('Unable to connect to central logger server.')
            except:
                flash('Issues with request.')

            return redirect(url_for('add_log'))

    return render_template('add_log.html', error=error)


@app.route('/simulate_bulk_logging', methods=['GET'])
def simulate_bulk_logging():
    """
    Simulate heavy traffic to the server.
    """
    i = 0
    successful_entries = 0
    while i < 1000:
        data = {
            'log_type': 'sim_log',
            'event_type': 'sim_event',
            'application': 'sim'
        }
        try:
            requests.post(API_URI + 'logs', json=data)
            successful_entries += 1
        except:
            flash('Failed')
        i += 1
    flash('Successfully added %d' % successful_entries)
    return render_template('add_log.html')


if __name__ == '__main__':
    app.secret_key = 'AABBMmBBBRERERER8998822333444'
    app.run(port=5050, debug=False)
