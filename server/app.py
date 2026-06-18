# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here

@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    found = Earthquake.query.filter_by(id=id).first()

    if found:
        return make_response({
            "id": found.id,
            "location": found.location,
            "magnitude": found.magnitude,
            "year": found.year
        }, 200)
    else:
        return make_response(
            {"message": f"Earthquake {id} not found."}, 404
        )
    
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    found = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude
    ).all()

    return make_response({
        "count": len(found),
        "quakes": [
            {
                "id": quake.id,
                "location": quake.location,
                "magnitude": quake.magnitude,
                "year": quake.year
            }
            for quake in found
        ]}, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
