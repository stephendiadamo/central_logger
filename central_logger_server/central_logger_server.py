from flask import Flask, jsonify, make_response, request, abort
from api_key_validator import require_apikey

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/logger/api/v1.0/get_error_logs', methods=['GET'])
@require_apikey
def get_error_logs():
    return jsonify({})


@app.route('/logger/api/v1.0/logs', methods=['POST'])
@require_apikey
def create_log():
    return jsonify({})


@app.route('/logger/api/v1.0/time_data', methods=['POST'])
@require_apikey
def time_data():
    return jsonify({})


if __name__ == '__main__':
    # todo: remove debug
    app.run(port=5000, debug=True)
