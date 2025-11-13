from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blood_bank_management_system.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(50), nullable = False)
    user_age = db.Column(db.Integer, nullable = False)
    user_blood_group = db.Column(db.String(20), nullable = False)

    def to_user(self):
        return {
            "user_id" : self.user_id,
            "user_name" : self.user_name,
            "user_age" : self.user_age,
            "user_blood_group" : self.user_blood_group
        }

with app.app_context():
    db.create_all()

#routes
@app.route("/")
def home():
    return "Blood Bank Management System Backend with Flask + Sqlite + SqlAlchemy"

#GET route
@app.route("/users",methods=["GET"])
def get_data():
    users = User.query.all()
    return jsonify([d.to_user() for d in users])

#post route
@app.route("/users",methods=["POST"])
def create_user():
    data = request.get_json()

    new_user = User(
        user_id = data["user_id"],
        user_name = data["user_name"],
        user_age = data["user_age"],
        user_blood_group = data["user_blood_group"]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message":"post successful"}),201

#put route
@app.route("/users/<int:user_id>",methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "not found"}),404

    user.user_name = data["user_name"]
    user.user_age = data["user_age"]
    user.user_blood_group = data["user_blood_group"]

    db.session.commit()

    return jsonify({"message": "update successful "}),200

#delete route
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "not found"}),404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message":"delete successful"}),200

#main
if __name__ == "__main__":
    app.run(debug=True)