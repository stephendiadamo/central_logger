from flask import Flask, jsonify, make_response, request, abort, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Log

# TODO: Require API Key Wrapper

app = Flask(__name__)
engine = create_engine('sqlite:///central_logger.db', echo=False)
Session = sessionmaker(bind=engine)

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
    if not request.json or not 'filter' in request.json or request.json['filter'] is None:
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

    session = Session()
    log_type = request.json['log_type']
    event_type = request.json['event_type']
    application = request.json['application']
    occurred_at = request.json.get('occurred_at', None)
    if occurred_at == '':
        occurred_at = None
    description = request.json.get('description', None)
    log_message = request.json.get('log_message', None)

    new_error = Log(log_type, event_type, application, occurred_at, description, log_message)
    session.add(new_error)
    session.commit()
    return jsonify({'result': new_error.serialize}), 201


@app.route('/logger/api/v1.0/time_data', methods=['POST'])
def time_data():
    return jsonify({})


def has_required_event_data_fields(json_request):
    """
    Used to validate new log entry
    :param json_request: The provided JSON data of the new log
    :return: If valid or not
    """
    for field in REQUIRED_LOG_FIELDS:
        if not field in json_request:
            return False

    return True


if __name__ == '__main__':
    app.run(port=5000, debug=True)
