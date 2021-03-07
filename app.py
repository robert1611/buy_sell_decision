from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import datetime
import os

from mortgage_calc import mortgage_calculation
from auth import find_or_create_user


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ['JWT_SECRET_KEY']


api = Api(app)
cors = CORS()
cors.init_app(app)

jwt = JWTManager(app)

mortgage_parser = reqparse.RequestParser()
mortgage_parser.add_argument('zip_code')
mortgage_parser.add_argument('credit_score')
mortgage_parser.add_argument('has_been_bankrupt')

auth_parser = reqparse.RequestParser()
auth_parser.add_argument('email')
auth_parser.add_argument('display_name')
auth_parser.add_argument('google_id')
auth_parser.add_argument('facebook_id')

class AuthApi(Resource):
  def post(self):
    args = auth_parser.parse_args()

    data = {
      'email': args['email'],
      'display_name': args['display_name'],
      'google_id': args['google_id'],
      'facebook_id': args['facebook_id']
    }

    user_result = find_or_create_user(data)
    if user_result['success'] == False:
      return user_result, 500
    user = user_result['user']
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(user.email), expires_delta=expires)
    return {'success': True, 'token': access_token}, 200


class MortgageCalculation(Resource):
    def get(self):
        return {'hello': 'world'}

    @jwt_required
    def post(self):
        args = mortgage_parser.parse_args()
        zip_code = args['zip_code']
        credit_score = args['credit_score']
        has_been_bankrupt = args['has_been_bankrupt']

        result = mortgage_calculation(zip_code, credit_score, has_been_bankrupt)
        return jsonify(result)


api.add_resource(MortgageCalculation, '/')
api.add_resource(AuthApi, '/auth')

if __name__ == '__main__':
    app.run(debug=True)