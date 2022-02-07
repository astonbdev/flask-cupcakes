"""Flask app for Cupcakes"""
import os
from flask import Flask, redirect, render_template, jsonify, request
from itsdangerous import json
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = os.getenv("APP_SECRET_KEY")

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)


@app.get("/api/cupcakes")
def show_all_cupcakes():
    """Responds with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = Cupcake.query.all()

    serialized = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def show_cupcake(cupcake_id):
    """For given cupcake_id, responds with JSON like: {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post("/api/cupcakes")
def create_cupcake():
    """Adds cupcake to database and responds with 
    JSON like: {cupcake: {id, flavor, size, rating, image}}"""

    image=request.json.get("image") or None 

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

@app.patch("/api/cupcakes/<int:cupcake_id>")
def update_cupcake(cupcake_id):
    """Updates cupcake in database and responds with JSON of the newly-updated 
    cupcake, like this: {cupcake: {id, flavor, size, rating, image}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # for arg in request.json:
    #     cupcake.set_attribute(arg, request.json[arg])

    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_cupcake(cupcake_id):
    """Deletes cupcake and responds with {deleted: [cupcake-id]}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    Cupcake.query.filter(id = cupcake_id).delete()

    return {"deleted": cupcake_id}