"""config相关"""

from .models import Config
from .models import update
from app import db


def add_config(args):
    """添加"""
    config = Config(**args)
    db.session.add(config)
    db.session.commit()
    return config.id


def get_config_by_id(cid):
    """通过id获取配置"""
    config = Config.query.get(cid)
    return config


def update_config(cid, args):
    """更新指定config"""
    config = Config.query.get(cid)
    config = update(config, args)
    db.session.commit()
    return config


def delete_config(cid):
    """删除config"""
    config = Config.query.get(cid)
    config.status = 0
    db.session.commit()