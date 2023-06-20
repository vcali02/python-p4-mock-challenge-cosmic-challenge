from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
#cascade="all, delete.orphan" CHECK SYNTAX

class Scientist(db.Model, SerializerMixin):

    __tablename__ = "scientists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    field_of_study = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #RELATIONSHIPS
    #A Scientist has many Missions
    missions_of_cur_scientist = db.relationship( "Mission", back_populates= "scientist")

    #ASSOCIATION_PROXY
    #A Scientist has many Planets through Missions
    planets_of_cur_scientist = association_proxy("missions_of_cur_scientist", "planet")


    #SERIALIZE RULES
    serialize_rules= (
        "-missions_of_cur_scientist.scientist", 
        "-planets_of_cur_scientist.scientists_of_cur_planet", 
        "-missions_of_cur_scientist.planet",
        "-created_at",
        "-updated_at"
        )




    #VALIDATIONS
    #must have a name
    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Must have a name.")
        names = db.session.query(Scientist.name).all()
        if name in names:
            raise ValueError("Scientist needs unique name.")
        return name
    
    #Must have a field_of_study
    @validates("field_of_study")
    def validate_field_of_study(self, key, field_of_study):
        if not field_of_study:
            raise ValueError("Must have a field of study.")
        return field_of_study




class Planet(db.Model, SerializerMixin):

    __tablename__ = "planets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #RELATIONSHIPS
    #A Planet has many Missions
    missions_of_cur_planet = db.relationship("Mission", back_populates= "planet")

    #ASSOCIATION_PROXY
    #A Planet has many Scientists through Missions
    #association_proxy('relationship to intermediary', 'relationship from intermediary to target')
    scientists_of_cur_planet = association_proxy("missions_of_cur_planet", "scientist")


    #SERIALIZE RULES
    serialize_rules = (
        "-missions_of_cur_planet.planet", 
        "-scientists_of_cur_planet.planet"
        )

    






class Mission(db.Model, SerializerMixin):

    __tablename__ = "missions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #FOREIGN KEYS
    scientist_id = db.Column(db.Integer, db.ForeignKey("scientists.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))


    #RELATIONSHIPS
    scientist = db.relationship("Scientist", back_populates= "missions_of_cur_scientist")
    #missions_of_cur_scientist = db.relationship( Mission, back_populates= "scientist")

    planet = db.relationship("Planet", back_populates = "missions_of_cur_planet")
    #missions_of_cur_planet = db.relationship("Mission", back_populates= "planet")


    #SERIALIZE RULES
    serialize_rules = (
        "-planet.missions_of_cur_scientist", 
        "-planet.missions_of_cur_planet"
        )

    



    #VALIDATIONS
    #must have a name, a scientist and a planet
    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Must have a name.")
        return name


    @validates("scientist_id")
    def validate_scientist(self, key, scientist):
        if not scientist:
            raise ValueError("Must have a scientist.")
        return scientist

    
    @validates("planet_id")
    def validate_planet(self, key, planet):
        if not planet:
            raise ValueError("Must have a planet.")
        return planet

    




# add any models you may need. 