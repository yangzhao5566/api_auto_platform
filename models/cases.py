"""TestCases"""
from .models import TestCases
from .models import update
from app import db


def get_case_by_id(cid):
    """通过id获取case信息"""
    case = TestCases.query.get(cid)
    return case


def add_case(args):
    case = TestCases(**args)
    db.session.add(case)
    db.session.commit()
    return case.id


def update_case(cid, args):
    """更新case"""
    case = TestCases.query.get(cid)
    case = update(case, args)
    db.session.commit()
    return case


def delete_case(cid):
    """删除case"""
    case = TestCases.query.get(cid)
    case.status = 0
    db.session.commit()
