"""ApiInfo"""
from .models import ApiInfo
from .models import update
from app import db


def get_api_by_id(aid):
    """通过id获取api信息"""
    api = ApiInfo.query.get(aid)
    return api


def add_api(args):
    api = ApiInfo(**args)
    db.session.add(api)
    db.session.commit()
    return api.id


def update_api(aid, args):
    """更新api"""
    api = ApiInfo.query.get(aid)
    api = update(api, args)
    db.session.commit()
    return api


def delete_api(aid):
    """删除api"""
    api = ApiInfo.query.get(aid)
    api.status = 0
    db.session.commit()
