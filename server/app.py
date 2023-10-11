#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API",
        }
        return response_dict, 200

api.add_resource(Home, '/')

class Newsletters(Resource):
    def get(self):
        newsletters = Newsletter.query.all()
        response_dict_list = [n.to_dict() for n in newsletters]
        return response_dict_list, 200

    def post(self):
        data = request.get_json()
        new_record = Newsletter(
            title=data['title'],
            body=data['body'],
        )
        db.session.add(new_record)
        db.session.commit()
        response_dict = new_record.to_dict()
        return response_dict, 201

api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        if newsletter:
            response_dict = newsletter.to_dict()
            return response_dict, 200
        else:
            return {"message": "Newsletter not found"}, 404

    def patch(self, id):
        data = request.get_json()
        newsletter = Newsletter.query.filter_by(id=id).first()
        if newsletter:
            newsletter.title = data['title']
            newsletter.body = data['body']
            db.session.commit()
            response_dict = newsletter.to_dict()
            return response_dict, 200
        else:
            return {"message": "Newsletter not found"}, 404

    def delete(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        if newsletter:
            db.session.delete(newsletter)
            db.session.commit()
            return {"message": "record successfully deleted"}, 200
        else:
            return {"message": "Newsletter not found"}, 404

api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
