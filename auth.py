from models import UserModel
from functools import wraps
from flask import request, Response
from werkzeug.security import check_password_hash

def basic_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return Response('Could not verify your access level for that URL.\nYou have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        user = UserModel.query.filter_by(username=auth.username).first()
        if not user or not check_password_hash(user.password_hash, auth.password):
            return Response('Could not verify your access level for that URL.\nYou have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated
