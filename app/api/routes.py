"""
使用restful来书写
"""
import ujson as json
from datetime import datetime
from app import db 
from flask import jsonify
import httprunner
from flask_restful import Resource
from flask_restful import reqparse
from . import api 
from app import create_token
from models.models import *
from models.test_group import add_group
from models.test_group import get_group_by_id
from models.test_group import update_group
from models.test_group import delete_group
from models.suites import add_suites
from models.suites import update_suites
from models.suites import delete_suites
from models.cases import add_case
from models.cases import update_case
from models.cases import get_case_by_id
from models.cases import delete_case
from models.api_info import add_api
from models.api_info import get_api_by_id
from models.api_info import update_api
from models.api_info import delete_api
from models.config import add_config
from models.config import get_config_by_id
from models.config import update_config
from models.config import delete_config
from app import auth

# 问题记录
# requests解决指定host问题
"""
import requests
requests.get("https:// 192.168.1.2",headers={'Host':'test.com'},verify=False)
"""

# 关于类似debugTalk功能
"""
想永久保存写的函数内容可以写入数据库
然后在初始化用例运行之前， 动态创建一个.py文件 通过importlib模块动态导入进来
当所有用例运行完成后再销毁此文件 
是否可行？

def px(l):
    for i, k in enumerate(l):
        a = [0, 1, 2]
        a.remove(i)
        print(l[i], l[a[0]], l[a[1]])
        print(l[i], l[a[1]], l[a[0]])
"""


class ResquestMinxin(object):
    """请求相关混入"""
    def get_params(self, params):
        """用来获取参数"""
        parser = reqparse.RequestParser()
        for param in params:
            parser.add_argument(**param)

        return parser

    def _update(self, args, obj):
        for k, v in args.items():
            if v:
                setattr(obj, k, v)
        return obj

    def get_product_by_project_id(self, project_id):
        """通过project_id获取product信息"""
        pass


class UserResource(Resource):
    """需要登录权限的Resource"""
    decorators = [auth.login_required]


# @api.resource('/users')
# class Users(Resource):
#     """用户相关"""
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('')
#         pass
#
#     def post(self):
        # https://www.jianshu.com/p/5fe9167ce243
        # https://flask-restful.readthedocs.io/en/latest/reqparse.html
        # 关于参数解析
        # 我感觉最佳的使用方式是获取了前端传来的参数，直接parser.parse_args获取
        #  然后通过 **args 来直接构建一个要存入数据库的对象
        #  若前后端定义字段不一致 可以在add_argument中添加dest来改成后端的名称

    # def post(self):
    #     """已测试 接口通"""
    #     args = [
    #         {'name': 'product_name', 'type': str, 'required': True,
    #          'help': '产品线名称必填项'},
    #         {'name': 'desc', 'type': str},
    #         {'name': 'admin_ids', 'type': json.loads, 'required': True,
    #          'help': '必填项'}
    #     ]
    #     parser = self.get_params(args)
    #     args = parser.parse_args()


@api.resource('/groups')
class Groups(Resource, ResquestMinxin):
    """组信息"""
    def get(self):
        # 用来获取所有的数据
        pass

    def post(self):
        args = [
            {'name': 'group_name', 'type': str, 'required': True, 'help': '组名为必填项'},
            {'name': 'desc', 'type': str},
            # {'name': 'create_user', 'type': str, 'required': True, 'help': '创建人为必填项'}
        ]
        parser = self.get_params(args)
        args = parser.parse_args()
        args['create_user'] = 'test_user'
        gid = add_group(args)
        return {'status': 200, 'gid': gid}


@api.resource('/group/<int:gid>')
class GroupDetail(Resource, ResquestMinxin):
    """组详情"""
    def get(self, gid):
        group = get_group_by_id(gid)
        return jsonify({'status': 200, 'result': group.to_dict()})

    def patch(self, gid):
        args = [
            {'name': 'group_name', 'type': str, 'required': True,
             'help': '组名为必填项'},
            {'name': 'desc', 'type': str},
        ]
        parser = self.get_params(args)
        args = parser.parse_args()
        group = update_group(gid, args)
        return jsonify({'status': 200, 'result': group.to_dict()})

    def delete(self, gid):
        delete_group(gid)
        return {'status': 200, 'result': '删除成功'}


@api.resource('/suites')
class Suites(Resource, ResquestMinxin):
    """suites"""
    def get(self):
        pass

    def post(self):
        """创建一个组"""
        args = [
            {'name': 'group_id', 'type': int, 'required': True,
             'help': '组id为比传项'},
            {'name': 'suites_name', 'type': str, 'required': True,
             'help': 'suites_name 未填写'},
            {'name': 'desc', 'type': str},
        ]
        parser = self.get_params(args)
        args = parser.parse_args()
        sid = add_suites(args)
        return {'status': 200, 'result': sid}


@api.resource('/suite/<int:sid>')
class SuitesDetail(Resource, ResquestMinxin):
    """suites_detail"""
    def get(self, sid):
        pass

    def patch(self, sid):
        args = [
            {'name': 'group_id', 'type': int, 'required': True,
             'help': '组id为比传项'},
            {'name': 'suites_name', 'type': str, 'required': True,
             'help': 'suites_name 未填写'},
            {'name': 'desc', 'type': str},
        ]
        parser = self.get_params(args)
        args = parser.parse_args()
        suites = update_suites(sid, args)
        return jsonify({'status': 200, 'result': suites})

    def delete(self, sid):
        delete_suites(sid)
        return {'status': 200, 'result': sid}


@api.resource('/cases')
class TestCases(db.Model):
    """testcase"""
    def get(self):
        pass

    def post(self):
        args = [
            {'name': 'suites_id', 'type': int, 'required': True,
             'help': 'suites_id为必传项'},
            {'name': 'case_name', 'type': str, 'required': True,
             'help': 'case_name 未填写'},
            {'name': 'priority', 'type': int},
            {'name': 'desc', 'type': str},
            {'name': 'steps', 'type': int},
        ]
        parser = self.get_params(args)
        args = parser.parse_args()
        cid = add_case(args)
        return {'status': 200, 'result': cid}


@api.resource('/case/<int:cid>')
class CaseDetail(Resource, ResquestMinxin):
    """case 详情"""
    def get(self, cid):
        case = get_case_by_id(cid)
        return {'status': 200, 'result': case.to_dict()}

    def patch(self, cid):
        args = [
            {'name': 'suites_id', 'type': int, 'required': True,
             'help': 'suites_id为必传项'},
            {'name': 'case_name', 'type': str, 'required': True,
             'help': 'case_name 未填写'},
            {'name': 'priority', 'type': int},
            {'name': 'desc', 'type': str},
            {'name': 'steps', 'type': int},
        ]
        parser = self.get_params(args)
        args = parser.parse_args()
        case = update_case(cid, args)
        return jsonify({'status': 200, 'result': case.to_dict()})

    def delete(self, cid):
        delete_case(cid)
        return {'status': 200, 'result': cid}


@api.resource('/apis')
class Apis(Resource, ResquestMinxin):
    """api"""
    def get(self):
        pass

    def post(self):
        args = [
            {'name': 'api_name', 'type': str, 'required': True,
             'help': 'name是必填项'},
            {'name': 'desc', 'type': str},
            {'name': 'url', 'type': str, 'required': True,
             'help': 'url是必填项'},
            {'name': 'methods', 'type': str, 'required': True,
             'help': 'methods是必填项'},
            {'name': 'headers', 'type': json.loads},
            {'name': 'variable_type', 'type': str, 'required': True,
             'help': 'variable_type是必填项'},
            {'name': 'json', 'type': json.loads},
            {'name': 'variables', 'type': json.loads},
            {'name': 'extract', 'type': json.loads},
            {'name': 'setup_hooks', 'type': json.loads},
            {'name': 'teardown_hooks', 'type': json.loads}
        ]
        # TODO 此处没想好， 需看下原来功能是怎么使用的？
        parser = self.get_params(args)
        args = parser.parse_args()
        aid = add_api(args)
        return {'status': 200, 'result': aid}


@api.resource('/api/<int:aid>')
class ApiDetail(Resource, ResquestMinxin):
    def get(self, aid):
        api = get_api_by_id(aid)
        return jsonify({'status': 200, 'result': api.to_dict()})

    def patch(self, aid):
        args = [
            {'name': 'api_name', 'type': str, 'required': True,
             'help': 'name是必填项'},
            {'name': 'desc', 'type': str},
            {'name': 'url', 'type': str, 'required': True,
             'help': 'url是必填项'},
            {'name': 'methods', 'type': str, 'required': True,
             'help': 'methods是必填项'},
            {'name': 'headers', 'type': json.loads},
            {'name': 'variable_type', 'type': str, 'required': True,
             'help': 'variable_type是必填项'},
            {'name': 'json', 'type': json.loads},
            {'name': 'variables', 'type': json.loads},
            {'name': 'extract', 'type': json.loads},
            {'name': 'setup_hooks', 'type': json.loads},
            {'name': 'teardown_hooks', 'type': json.loads}
        ]
        parser = self.get_params(args)
        args = parser.parse_args()
        api = update_api(aid, args)
        return jsonify({'status': 200, 'result': api.to_dict()})

    def delete(self, aid):
        delete_api(aid)
        return {'status': 200}


@api.resource('/configs')
class Conifgs(Resource, ResquestMinxin):
    def get(self):
        pass

    def post(self):
        args = [
            {'name': 'suites_id', 'type': str, 'required': True,
             'help': 'name是必填项'},
            {'name': 'case_id', 'type': str, 'required': True,
             'help': 'case_id是必填项'},
            {'name': 'config_name', 'type': str, 'required': True,
             'help': 'config_name是必填项'},
            {'name': 'desc', 'type': str},
            {'name': 'variables', 'type': json.loads, 'required': True,
             'help': 'variables是必填项'},
        ]
        parser = self.get_params(args)
        args = parser.parse_args()
        cid = add_config(args)
        return {'status': 200, 'result': cid}


@api.resource('/config/<int:cid>')
class ConfigDetail(Resource, ResquestMinxin):
    def get(self, cid):
        api = get_config_by_id(cid)
        return {'status': 200, 'result': api.to_dict()}

    def patch(self, cid):
        args = [
            {'name': 'suites_id', 'type': str, 'required': True,
             'help': 'name是必填项'},
            {'name': 'case_id', 'type': str, 'required': True,
             'help': 'case_id是必填项'},
            {'name': 'config_name', 'type': str, 'required': True,
             'help': 'config_name是必填项'},
            {'name': 'desc', 'type': str},
            {'name': 'variables', 'type': json.loads, 'required': True,
             'help': 'variables是必填项'},
        ]
        parser = self.get_params(args)
        args = parser.parse_args()
        config = update_config(cid, args)
        return {'status': 200, 'result': config.to_dict()}

    def delete(self, cid):
        delete_config(cid)
        return {'status': 200}


