import os  
from dotenv import load_dotenv
DIALECT = ''
DRIVER = ''
USERNAME = ''
PASSWORD = ''
HOST = ''
PORT = ''
DATABASE = ''
ISDEBUG = False

# 引入local_settings 本地配置
try:
    from .local_settings import *
except ImportError:
    pass

basedir = os.path.abspath(os.path.dirname(__file__))

# 获取.env 中的配置
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """配置文件"""
    print("=============.env================")
    print(os.environ.get("FLASK_APP"))
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-or-some'
    # 打印拼接后的sql， 便于排查问题
    SQLALCHEMY_ECHO = ISDEBUG
    SQLALCHEMY_TRACK_MODIFICATIONS = False
