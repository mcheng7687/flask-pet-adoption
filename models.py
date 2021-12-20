from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class Pet (db.Model):
    """Pet Class"""
    __tablename__ = "pets"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    name = db.Column(db.String(),
                    nullable = False)
    species = db.Column(db.String(),
                    nullable = False)
    photo_url = db.Column(db.String())
    age = db.Column(db.Integer)
    notes = db.Column(db.String())
    available = db.Column(db.Boolean,
                    default = True)

    def __repr__(self):
        return f"<Pet obj id:{self.id} name:{self.name} species:{self.species} available:{self.available}"
    

