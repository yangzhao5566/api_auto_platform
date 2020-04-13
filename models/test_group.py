"""test_group 相关"""

from .models import TestGroup
from .models import update
from app import db


def add_group(args):
    """添加一个组"""
    tg = TestGroup(**args)
    db.session.add(tg)
    db.session.commit()
    return tg.id


def get_group_by_id(gid):
    """通过组id获取组信息"""
    tg = TestGroup.query.get(gid)
    return tg


def update_group(gid, args):
    """更新组信息"""
    tg = TestGroup.query.get(gid)
    tg = update(tg, args)
    db.session.commit()
    return tg


def delete_group(gid):
    tg = TestGroup.query.get(gid)
    tg.status = 0
    db.session.commit()


