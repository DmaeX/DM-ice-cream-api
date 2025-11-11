from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy #ORM
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)


# Create Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ice-cream.db" #app configured to accept sql db


db = SQLAlchemy(app) #database object 

class IceCreamFlavors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column (db.String, nullable=False)
    flavor = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    #convert data into json format 
    def to_dict(self):
        return {
            "id" : self.id,
            "image" : self.image,
            "flavor" : self.flavor,
            "rating": self.rating
        }

#context manager to set file 
with app.app_context():
    db.create_all()

# HOME
# https://www.dmicecream.io/
# Create Routes 
@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")


# GET all flavors
# https://www.dmicecream.io/flavors
@app.route("/flavors", methods=["GET"])
@cross_origin()
def get_flavors():
    flavors = IceCreamFlavors.query.all()

    return jsonify([flavor.to_dict() for flavor in flavors])

# GET single flavor based on flavor_id
# https://www.dmicecream.io/flavors/3
@app.route("/flavors/<int:flavor_id>", methods=["GET"])
@cross_origin()
def get_flavor(flavor_id):
    flavor = IceCreamFlavors.query.get(flavor_id)
    if flavor:
        return jsonify(flavor.to_dict())
    else:
        return jsonify({"error":"Flavah no heere - haya!"}), 404

#POST 
# https://www.dmicecream.io/flavors
@app.route("/flavors", methods=["POST"])
@cross_origin()
def add_flavor():

    data = request.get_json() #takes the request and parses data 

    new_flavor = IceCreamFlavors(flavor=data["flavor"],
                                 image=data["image"], 
                                 rating=data["rating"])
    
    db.session.add(new_flavor) #inserts new flavor to db 
    db.session.commit() #anytime something is added to db, commit back to the db

    return jsonify(new_flavor.to_dict()), 201 

# PUT 
# https://www.dmicecream.io/flavors
@app.route("/flavors/<int:flavor_id>", methods=["PUT"])
@cross_origin()
def update_flavor(flavor_id):
    data = request.get_json()

    flavor = IceCreamFlavors.query.get(flavor_id)
    if flavor:
        flavor.flavor = data.get("image", flavor.image)
        flavor.flavor = data.get("flavor", flavor.flavor)
        flavor.rating = data.get("rating", flavor.rating)

        db.session.commit()

        return jsonify(flavor.to_dict())
    
    else:
        return jsonify({"error": "Flavah no heere - haya!"}), 404
    
# DELETE 
# https://www.dmicecream.io/flavors
@app.route("/flavors/<int:flavor_id>", methods=["DELETE"])
@cross_origin()
def delete_flavor(flavor_id):
    flavor = IceCreamFlavors.query.get(flavor_id)
    if flavor:
        db.session.delete(flavor)
        db.session.commit()

        return jsonify({"message":"Flavah was deleted!"})
    else:
        return jsonify({"error": "Flavah no heere - haya!"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
