from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#database======================================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(50), nullable = False)
    user_age = db.Column(db.Integer, nullable= False)

    def to_user(self):
        return {
            "user_id" : self.user_id,
            "user_name" : self.user_name,
            "user_age" : self.user_age
        }

with app.app_context():
    db.create_all()

#Routes ================================
#POST
@app.route("/add", methods = ["POST"])
def create_user():
    data = request.get_json()
    new_user = User(user_name = data["user_name"],user_age = data["user_age"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_user()), 201


# GET
@app.route("/get", methods=["GET"])
def get_user():
    all_data = User.query.all()
    return jsonify([d.to_user() for d in all_data])


@app.route("/")
def home():
    return "Welcome to flask api home"

#main======================================
if __name__ == "__main__":
    app.run(debug=True)