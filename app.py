from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from flask_restful_swagger import swagger
import requests

app = Flask(name)
api = swagger.docs(Api(app), apiVersion='0.1')


class Welcome(Resource):
    @swagger.operation(
        notes='Get the welcome message',
        responseMessages=[
            {
                "code": 200,
                "message": "Success"
            }
        ]
    )
    def get(self):
        return {"message": "Welcome to the Currency Converter"}


class ConversionRate(Resource):
    @swagger.operation(
        notes='Get the conversion rate between two currencies',
        parameters=[
            {
                "name": "from",
                "description": "The currency to convert from",
                "required": True,
                "type": "string",
                "paramType": "query"
            },
            {
                "name": "to",
                "description": "The currency to convert to",
                "required": True,
                "type": "string",
                "paramType": "query"
            },
            {
                "name": "value",
                "description": "The value to convert",
                "required": True,
                "type": "float",
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Success",
                "responseModel": "ConversionResult"
            }
        ]
    )
    def get(self):
        from_currency = request.args.get('from')
        to_currency = request.args.get('to')
        value = float(request.args.get('value'))

        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{from_currency}')
        rates = response.json()['rates']
        rate = rates[to_currency]

        result = value * rate

        return jsonify({'result': result})


class ConversionResult:
    def init(self, result):
        self.result = result


api.add_resource(Welcome, '/')
api.add_resource(ConversionRate, '/api/rates')

if name == 'main':
    app.run(host='0.0.0.0')