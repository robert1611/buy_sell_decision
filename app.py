from flask import Flask
from flask_restful import Resource, Api, reqparse
from mortgage_calc import mortgage_calculation
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('zip_code')
parser.add_argument('credit_score')
parser.add_argument('has_been_bankrupt')

class MortgageCalculation(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        args = parser.parse_args()
        zip_code = args['zip_code']
        credit_score = args['credit_score']
        has_been_bankrupt = args['has_been_bankrupt']

        result = mortgage_calculation(zip_code, credit_score, has_been_bankrupt)
        return result


api.add_resource(MortgageCalculation, '/')

if __name__ == '__main__':
    app.run(debug=True)