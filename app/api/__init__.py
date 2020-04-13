from flask import Blueprint
from flask_restful import Api

route_api = Blueprint('api', __name__, url_prefix='/api')
api = Api(route_api)

from . import routes
