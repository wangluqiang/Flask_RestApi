# coding=utf-8
from flask.ext.restful import Resource, reqparse, Api
from ..models import Task
from .. import auth, db
from flask import abort,Blueprint
task_blueprnt = Blueprint('task_blueprint', __name__)
# from . import task_blueprnt

api = Api(task_blueprnt)


class TaskListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='No task title provided.', location='json')
        self.reqparse.add_argument('description', type=str, default='', location='json')
        self.reqparse.add_argument('done', type=bool, required=True, help='No task done provide.', location='json')
        super(TaskListAPI, self).__init__()

    def get(self):
        tasks = Task.query.all()
        print(tasks)
        return str(tasks)

    def post(self):
        task = dict(self.reqparse.parse_args())
        title = task.get('title')
        done = task.get('done')
        description = task.get('description')
        task = Task.query.filter_by(title=title).first()
        if task:
            return {'code': 200, 'message': 'The title is already used!'}
        task = Task(title=title, done=done, description=description)
        db.session.add(task)
        db.session.commit()
        return {'code': 200, 'message': 'create task success!',
                'data': {'title': title, 'done': done, 'description': description}}, 200


class TaskAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        print(id)
        task = Task.query.filter_by(id=id).first()
        if not task:
            abort(404)
        return {'code': 200, 'data': {'title': task.title, 'done': task.done, 'description': task.description},
                'message': 'query task success!'}, 200

    def put(self, id):
        task = dict(self.reqparse.parse_args())
        task_sql = Task.query.filter_by(id=id).first()
        print(task_sql)
        if not task_sql:
            abort(404)
        task_sql.title = task.get('title')
        task_sql.done = task.get('done')
        task_sql.description = task.get('description')
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return {'code': 200, 'message': 'The title has bean used!'}
        return {'code': 200, 'message': 'Modify task success!'}

    def delete(self, id):
        task_sql = Task.query.filter_by(id=id).first()
        if not task_sql:
            abort(404)
        db.session.delete(task_sql)
        return {'code': 200, 'message': 'Delete task success!'}


api.add_resource(TaskListAPI, '/tasks', '/tasks/', endpoint='tasks')
api.add_resource(TaskAPI, '/tasks/<int:id>', endpoint='task')
