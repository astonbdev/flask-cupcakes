"""Flask app for Cupcakes"""
import os
from flask import Flask, redirect, render_template, jsonify, request
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "test"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)


@app.get("/api/cupcakes")
def show_all_cupcakes():
    """Returns all cupcakes in database as JSON"""

    cupcakes = Cupcake.query.all()

    serialized = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def show_cupcake(cupcake_id):
    """Returns info about individual cupcake in JSON"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post("/api/cupcakes")
def create_cupcake():
    """Creates a new cupcake instance 
    from request.json and adds it to existing database 
    then returns cupcake instance as JSON"""

    try: 
        image=request.json["image"]
    except KeyError:
        image=None

    cupcake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"],
        rating=request.json["rating"],
        image=image
    )

    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)
