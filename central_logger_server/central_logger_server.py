from flask import Flask, jsonify, make_response, request, abort, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Log
from apscheduler.schedulers.background import BackgroundScheduler

# TODO:
# Require API Key Wrapper on endpoints.
# Although implemented in api_key_validator.py, for convenience I
# will not use it.

app = Flask(__name__)
engine = create_engine('sqlite:///central_logger.db', echo=False)
Session = sessionmaker(bind=engine)
scheduler = BackgroundScheduler()

log_buffer = []

REQUIRED_LOG_FIELDS = [
    'log_type',
    'event_type',
    'application'
]


@app.errorhandler(404)
def not_found(error):
    """
    Handles 404 errors
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    """
    Handles 400 errors
    """
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/view_data', methods=['GET'])
def view_data():
    """
    Render a table to show all log entries
    """
    session = Session()
    logs = session.query(Log).all()
    return render_template('index.html', logs=logs)


@app.route('/logger/api/v1.0/get_logs', methods=['GET'])
def get_logs():
    """
    Return JSON formatted data of log entries. Optional filter parameter
    is available to filter data by log_type.
    """
    session = Session()
    if not request.json or 'filter' not in request.json or request.json['filter'] is None:
        res = session.query(Log).all()
    else:
        res = session.query(Log).filter(Log.log_type == request.json['filter']).all()

    return jsonify(result=[i.serialize for i in res])


@app.route('/logger/api/v1.0/logs', methods=['POST'])
def create_log():
    """
    Add a new log entry.
    """
    if not request.json or not has_required_event_data_fields(request.json):
        abort(400)

    log_type = request.json['log_type']
    event_type = request.json['event_type']
    application = request.json['application']
    occurred_at = request.json.get('occurred_at', None)
    if occurred_at == '':
        occurred_at = None
    description = request.json.get('description', None)
    log_message = request.json.get('log_message', None)

    new_log = Log(log_type, event_type, application, occurred_at, description, log_message)
    log_buffer.append(new_log)

    return jsonify({'result': new_log.serialize}), 201


@app.route('/logger/api/v1.0/time_data', methods=['POST'])
def time_data():
    """
    Return bar-graph type data bucketed into intervals specified by the user
    :return: The data
    """

    # TODO:
    # What I would do here is, since we have a date stamp on every log, bucket
    # the data into interval chucks specified by the user. For example,
    # the user can specify 'day' which will return data bucketed into days.
    # Users should also be able to specify a start date and end date of when the
    # logs occurred. To display graphs, there are many libraries, such as
    # Chart.js that produce clean graphs and are easy to use.

    return jsonify({})


def add_and_clear_log_buffer():
    """
    To prevent overloading the database server, make periodic commits on a schedule
    """

    # TODO:
    # Should explore further what happens when this is running and a log is
    # added to the buffer

    session = Session()
    global log_buffer
    for log in log_buffer:
        session.add(log)

    log_buffer = []
    session.commit()


def has_required_event_data_fields(json_request):
    """
    Used to validate new log entry
    :param json_request: The provided JSON data of the new log
    :return: If valid or not
    """
    for field in REQUIRED_LOG_FIELDS:
        if field not in json_request:
            return False

    return True


if __name__ == '__main__':
    scheduler.add_job(add_and_clear_log_buffer, 'interval', seconds=15)
    scheduler.start()
    app.run(port=5000, debug=False)
