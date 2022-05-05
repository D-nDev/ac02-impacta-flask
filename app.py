from flask import Flask, jsonify, request, render_template, make_response
from model.user import db
from flask_cors import CORS

from model.user import User


app = Flask(__name__, static_url_path='',
            static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456@localhost:5432/students'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, resources={r"*": {"origins": "*"}})

db.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/list')
def userlist():
    return render_template('list.html')


@app.route('/newuser', methods=['POST'])
def create_user():
    try:
        db.create_all()
        db.session.commit()

        user_data = request.json

        user_name = user_data['name']
        user_email = user_data['email']
        user_address = user_data['address']

        user = User(user_name=user_name, user_email=user_email,
                    user_address=user_address)

        db.session.add(user)
        db.session.commit()

        res = make_response(jsonify({"success": "User created"}), 201)
        return res
    except Exception as e:
        print(e)
        err = make_response(jsonify({"error: ": "An error has occurred"}), 500)
        return err


@app.route('/allusers', methods=['GET'])
def get_users():
    try:
        all_users = []
        users = User.query.all()
        for user in users:
            result = {
                "id": user.id,
                "name": user.user_name,
                "email": user.user_email,
                "address": user.user_address,
            }
            all_users.append(result)

        res = make_response(jsonify(all_users), 200)
        return res
    except Exception as e:
        print(e)
        err = make_response(jsonify({"error: ": "An error has occurred"}), 500)
        return err


if __name__ == "__main__":
    app.run(host='0.0.0.0')
