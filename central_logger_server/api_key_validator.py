from functools import wraps
from flask import request, abort

API_KEY = '112233STEPHEN2323'


def require_apikey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and request.args.get('key') == API_KEY:
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function