#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Planet, Scientist, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''


#GET /scientists
class Scientists(Resource):
    def get(self):
        #1. query
        scientists = Scientist.query.all()
        #2. dict
        scientists_dict = [s.to_dict() for s in scientists]
        #3. res return
        res = make_response(
            scientists_dict,
            200
        )
        return res

#POST /scientists
    def post(self):
        try:
            #1. DATA TO JSON
            data = request.get_json()
            #2. instance
            new_scientist = Scientist(
                name = data.get('name'),
                field_of_study= data.get('field_of_study'),
                avatar = data.get('avatar')
            )
            #ADDDD ANDDD COMMIIITTTT
            db.session.add(new_scientist)
            db.session.commit()
            #3. dict
            new_scientist_dict = new_scientist.to_dict()
            #4. res
            res = make_response(
                new_scientist_dict,
                201
            )
            #5. return
            return res
        except:
            return {"error": "400: Validation error"}, 400
#4. add api resource
api.add_resource(Scientists, "/scientists")


#GET /scientists/int:id
class OneScientist(Resource):
    def get(self, id):
        try:
            #1. query
            scientist = Scientist.query.filter_by(id=id).first()
            #2. dict
            scientist_dict = scientist.to_dict()
            #3. res return
            res = make_response(
                scientist_dict,
                200
            )
            return res
        except: 
            return {"error": "404: Scientist not found"}, 404

#PATCH /scientists/:id
    def patch(self, id):
        #1. get by id
        scientist = Scientist.query.filter_by().first()
        #EXCEPTION
        if not scientist:
            return {"error": "Scientist not found"}, 404
        #EXCEPTION
        try:
            #2. get data request in json
            data = request.get_json()
            #3. update values setattr()
            #need to loop through the DATA not the SINGLE scientist
            for attr in data:
                setattr(scientist, attr, data.get(attr))
            #4. update database
            db.session.add(scientist)
            db.session.commit()
            #return res
            return make_response(scientist.to_dict(), 202)
        except:
            return {"error": "400: Validation error"}, 400


#DELETE /scientists/int:id
    def delete(self, id):
        #1. get scientist by id
        scientist = Scientist.query.filter_by(id = id).first()
        if scientist:
            #2. delete MISSION
            Mission.query.filter_by(scientist_id=id).delete()
            #3. delete SCIENTIST
            db.session.delete(scientist)
            #4. commit
            db.session.commit()
            #res
            res = make_response({}, 204)
        else:
            return {"error": "404: Scientist not found"}, 404




#4. add api resource
api.add_resource(OneScientist, "/scientists/<int:id>")



#GET /planets
class Planets(Resource):
    def get(self):
        #1. query
        planets = Planet.query.all()
        #2. dict
        planets_dict = [p.to_dict() for p in planets]
        #3. res return
        res = make_response(
            planets_dict,
            200
        )
        return res

#4. add api resource
api.add_resource(Planets, "/planets")



#POST /missions
class Missions(Resource):
    def get(self):
        missions = Mission.query.all()
        missions_dict = [m.to_dict() for m in missions]
        res = make_response(
            missions_dict,
            200
        )
        return res


    def post(self):
        #1. data
        data = request.get_json()
        try:
            #2. instance
            new_mission = Mission(
                name=data.get('name'),
                scientist_id=data.get('scientist_id'),
                planet_id=data.get('planet_id')
            )
            #need to add to table FIRST before turning into dict
            #want table to be an object
            #4. adding/committing
            db.session.add(new_mission)
            db.session.commit()
            #3. dict
            new_mission_dict = new_mission.to_dict()
            #want response to be a dictionary
            #5. res return
            res = make_response(
                new_mission_dict,
                201
            )
            return res
        except:
            return {"error": "400: Validation error"}, 400
#6. api
api.add_resource(Missions, "/missions")
        



if __name__ == '__main__':
    app.run(port=5555, debug=True)
