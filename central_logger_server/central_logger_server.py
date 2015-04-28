from flask import Flask, jsonify, make_response, request, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Error

# TODO: Require API Key Wrapper

app = Flask(__name__)
engine = create_engine('sqlite:///central_logger.db', echo=False)
Session = sessionmaker(bind=engine)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/logger/api/v1.0/get_error_logs', methods=['GET'])
def get_error_logs():
    session = Session()
    res = session.query(Error).all()
    return jsonify(result=[i.serialize for i in res])


@app.route('/logger/api/v1.0/logs', methods=['POST'])
def create_log():
    if not request.json or not 'error_type' in request.json:
        abort(400)

    session = Session()
    error_type = request.json['error_type']
    description = request.json.get('description', "")
    occurred_at = request.json.get('occurred_at', None)
    new_error = Error(error_type, description, occurred_at)
    session.add(new_error)
    session.commit()
    return jsonify({'result': new_error.serialize}), 201


@app.route('/logger/api/v1.0/time_data', methods=['POST'])
def time_data():
    return jsonify({})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
