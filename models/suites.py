"""suites"""
from .models import TestSuites
from .models import update
from app import db


def add_suites(args):
    """添加一个suites"""
    ts = TestSuites(**args)
    db.session.add(ts)
    db.session.commit()
    return ts.id


def update_suites(sid, args):
    """更新suites"""
    suites = TestSuites.query.get(sid)
    suites = update(suites, args)
    db.session.commit()
    return suites


def delete_suites(sid):
    suites = TestSuites.query.get(sid)
    suites.status = 0
    db.session.commit()
