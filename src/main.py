from flask import Flask, jsonify, request, render_template, make_response
import psycopg2
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests as http_request

app = Flask(__name__, template_folder="templates")

# Configuração do JWT
app.config["JWT_SECRET_KEY"] = "goku-vs-vegeta"
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

jwt = JWTManager(app)


def get_db_connection():
    conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="db",
            port=5432)
    return conn

teste = get_db_connection()
if teste:
    print("Conectado ao banco de dados com sucesso!")

class User:
    @staticmethod
    def find_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    if username is None or password is None:
        return render_template("error.html", message="Bad username or password")

    token_data = http_request.post("http://localhost:5000/token", json={"username": username, "password": password})
    if token_data.status_code != 200:
        return render_template("error.html", message="Bad username or password")

    response = make_response(render_template("content.html"))
    set_access_cookies(response, token_data.json()['token'])
    return response

@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.find_by_email(username)
    if user is None or user[2] != password:  # Verifique a senha aqui
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user[0])
    return jsonify({"token": access_token, "user_id": user[0]})

@app.route("/user-register", methods=["GET"])
def user_register():
    return render_template("register.html")

@app.route("/user-login", methods=["GET"])
def user_login():
    return render_template("login.html")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{"id": user[0], "name": user[1], "email": user[2]} for user in users])

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s;", (id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({"id": user[0], "name": user[1], "email": user[2]})

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id;", (data["name"], data["email"], data["password"]))
    new_user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"id": new_user_id, "name": data["name"], "email": data["email"]})

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s RETURNING id;", (data["name"], data["email"], data["password"], id))
    updated_user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"id": updated_user_id, "name": data["name"], "email": data["email"]})

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s RETURNING id;", (id,))
    deleted_user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"id": deleted_user_id})

@app.route("/content", methods=["GET"])
@jwt_required()
def content():
    return render_template("content.html")

@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
