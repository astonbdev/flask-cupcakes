"""Flask app for Cupcakes"""
import os
from flask import Flask, jsonify, request
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
    """Responds with JSON like:
    {cupcakes: [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = Cupcake.query.all()

    serialized = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def show_cupcake(cupcake_id):
    """For given cupcake_id, responds with JSON like:
    {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post("/api/cupcakes")
def create_cupcake():
    """Adds cupcake to database and responds with
    JSON like: {cupcake: {id, flavor, size, rating, image}}"""

    image = request.json.get("image") or None

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

    if request.json.get("flavor"):
        cupcake.flavor = request.json["flavor"]

    if request.json.get("size"):
        cupcake.size = request.json["size"]
    
    if request.json.get("rating") or request.json.get("rating") == 0:
        cupcake.rating = request.json["rating"]

    if request.json.get("image"):
        cupcake.image = request.json["image"]

    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_cupcake(cupcake_id):
    """Deletes cupcake and responds with
    JSON: {deleted: [cupcake-id]}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    Cupcake.query.filter(Cupcake.id == cupcake.id).delete()

    db.session.commit()

    return {"deleted": cupcake_id}
