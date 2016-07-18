# coding=utf-8
from flask.ext.restful import Resource, reqparse, Api
from ..models import User
from .. import auth, db
from flask import abort, jsonify, g, Blueprint

users_blueprint = Blueprint('users_blueprint', __name__)
# from . import users_blueprint

api = Api(users_blueprint)


class UserApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, help='No username provided.', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='No password provided.', location='json')
        super(UserApi, self).__init__()

    def post(self):
        args = dict(self.reqparse.parse_args())
        print(args)
        username = args.get('username')
        password = args.get('password')
        if User.query.filter_by(username=username).first():
            return {'Message': 'The username is already used!'}
        user = User(username=username)
        user.password = password
        db.session.add(user)
        db.session.commit()
        return {'username': user.username}

    @auth.login_required
    def put(self):
        args = dict(self.reqparse.parse_args())
        print(args)
        username = args.get('username')
        password = args.get('password')
        g.user.username = username
        g.user.password = password
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return {'code': 200, 'message': 'The username is alreadr used!'}
        return {'code': 200, 'message': 'Modify user info success!'}


api.add_resource(UserApi, '/user', endpoint='user')


@users_blueprint.route('/user/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    return jsonify({'username': user.username})


@users_blueprint.route('/token')
@auth.login_required
def get_auth_token():
    print(g.user)
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token})
