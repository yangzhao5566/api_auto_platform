"""
model 文件
flask db init
flask db migrate -m "crate table"
flask db upgrade

sqlalchemy 相关使用
https://www.cnblogs.com/wf-skylark/p/9306326.html
http://docs.jinkan.org/docs/flask-sqlalchemy
"""
from app import db 
from datetime import datetime


def to_dict(self):
    """将结果转化成字典"""
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


def update(obj, args):
    """更新"""
    for k, v in args.items():
        if v:
            setattr(obj, k, v)
    return obj


db.Model.to_dict = to_dict


class TestGroup(db.Model):
    """测试组"""
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(200), nullable=False, comment='组名称')
    desc = db.Column(db.String(200), comment='测试组的描述')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    create_user = db.Column(db.String(40), comment='创建人')
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='测试组的状态0无效, 1有效')

    def __repr__(self):
        return f'<TestGroup> {self.id}'


class TestSuites(db.Model):
    """testsuites"""
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=False, comment='所属testGroup')
    suites_name = db.Column(db.String(60), nullable=False, comment='suites名称')
    desc = db.Column(db.String(200), comment='测试组的描述')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='测试组的状态0无效, 1有效')

    def __repr__(self):
        return f'<TestSuite> {self.id}, {self.test_group_id}'


class TestCases(db.Model):
    """testcase"""
    id = db.Column(db.Integer, primary_key=True)
    suites_id = db.Column(db.Integer, nullable=False, comment='testsuite id')
    case_name = db.Column(db.String(200), nullable=False, comment='case的名称')
    priority = db.Column(db.SMALLINT, default=3)
    desc = db.Column(db.String(200), comment='测试组的描述')
    # TODO 缺少接口信息
    steps = db.Column(db.JSON, comment='接口步骤')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='case的状态0无效, 1有效')

    def __repr__(self):
        return f'<TestCases> {self.id}, {self.suites_id} {self.case_name}'


class ApiInfo(db.Model):
    """单个接口信息"""
    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String(200), nullable=False, comment='case的名称')
    desc = db.Column(db.String(200), comment='接口描述')
    url = db.Column(db.String(800), nullable=False, comment='请求url')
    methods = db.Column(db.String(30), nullable=False, comment='请求方式')
    headers = db.Column(db.JSON, comment='请求头信息')
    variable_type = db.Column(db.String(32), nullable=True, comment='参数类型选择')
    json = db.Column(db.JSON, comment='请求body')
    variables = db.Column(db.JSON, comment='测试步骤中定义的变量，作用域为当前测试步骤')
    validate = db.Column(db.JSON, comment='结果校验项')
    extract = db.Column(db.JSON, comment='extract')
    setup_hooks = db.Column(db.JSON, comment='setup_hooks')
    teardown_hooks = db.Column(db.JSON, comment='teardown_hooks')

    def __repr__(self):
        return f'<ApiInfo> {self.id}, {self.api_name} {self.desc}'


class Config(db.Model):
    """配置"""
    id = db.Column(db.Integer, primary_key=True)
    suites_id = db.Column(db.Integer, nullable=False, comment='testsuite id')
    case_id = db.Column(db.Integer, nullable=False, default=0, comment='case id')
    config_name = db.Column(db.String(200), nullable=False, comment='配置名称')
    desc = db.Column(db.String(200), comment='测试组的描述')
    variables = db.Column(db.JSON, comment='参数')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='测试组的状态0无效, 1有效')

    def __repr__(self):
        return f'<TestCases> {self.id}, {self.suites_id} {self.case_name}'


class Task(db.Model):
    """定时任务"""
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(80), nullable=False, comment='任务名称')
    desc = db.Column(db.String(200), comment='任务描述')
    detail = db.Column(db.JSON, nullable=False)
    task_num = db.Column(db.String(200), nullable=False)
    task_type = db.Column(db.Integer, nullable=False, comment='运行方式 1. 一次 2. 每天. 3.指定次数')
    task_time = db.Column(db.JSON, nullable=False, comment='运行时间')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='测试组的状态0无效, 1有效')

    def __repr__(self):
        return f'<Task> {self.id}, {self.task_num} {self.task_type}'
