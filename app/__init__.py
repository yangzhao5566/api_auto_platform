from flask import Flask
from flask import g 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import import_string
from flask_cors import CORS
from config.config import Config

from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, \
    BadSignature, SignatureExpired

blueprints = ['app.api:route_api']


app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources=r'/*')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

auth = HTTPTokenAuth(scheme='Bearer')
serializer = Serializer(app.config["SECRET_KEY"], expires_in=3600)


def create_token(data):
    """生成token"""
    token = serializer.dumps(data)
    return token.decode("utf-8")


@auth.verify_token
def verify_token(token):
    """验证token"""
    # 待完善。
    try:
        data = serializer.loads(token)
        print(data)
    except BadSignature:
        print("无效的token")
    except SignatureExpired:
        print('过期的token')
    return True


for bp_name in blueprints:
    bp = import_string(bp_name)
    app.register_blueprint(bp)
