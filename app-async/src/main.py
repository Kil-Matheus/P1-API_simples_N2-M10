from flask import Flask, jsonify, request, render_template, make_response, redirect
import asyncpg
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests as http_request
import asyncio
import time

app = Flask(__name__, template_folder="templates")

# Configuração do JWT
app.config["JWT_SECRET_KEY"] = "goku-vs-vegeta"
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

jwt = JWTManager(app)

# Função assíncrona para obter conexão com o banco de dados
async def get_db_connection():
    return await asyncpg.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="db",
        port=5432
    )

# Testando a conexão com o banco de dados
async def test_db_connection():
    conn = await get_db_connection()
    if conn:
        print("Conectado ao banco de dados com sucesso!")
    await conn.close()

class User:
    @staticmethod
    async def find_by_email(email):
        conn = await get_db_connection()
        user = await conn.fetchrow("SELECT * FROM users WHERE email = $1;", email)
        await conn.close()
        return user

@app.route('/inicio')
async def banco_inicio():
    conn = await get_db_connection()
    try:
        rows = await conn.fetch('SELECT * FROM bloco')
        tasks = [dict(row) for row in rows]
        return jsonify(tasks)
    finally:
        await conn.close()


@app.route('/insert', methods=['POST'])
async def banco_insert():
    nome = request.form.get('nome')
    valor = request.form.get('valor')

    conn = await get_db_connection()
    try:
        await conn.execute('INSERT INTO bloco (title, contents) VALUES ($1, $2)', nome, valor)
        return redirect('/inicio')
    finally:
        await conn.close()

@app.route('/delete', methods=['POST'])
async def banco_delete():
    data = request.json
    id_to_delete = data.get('id')

    conn = await get_db_connection()
    try:
        await conn.execute('DELETE FROM bloco WHERE id = $1', id_to_delete)
        return redirect('/inicio')
    finally:
        await conn.close()

@app.route('/edit', methods=['POST'])
async def banco_edit():
    title = request.form.get('title')
    new_title = request.form.get('new_title')
    new_contents = request.form.get('new_contents')

    conn = await get_db_connection()
    try:
        await conn.execute('UPDATE bloco SET title = $1, contents = $2 WHERE title = $3', new_title, new_contents, title)
    finally:
        await conn.close()


@app.route("/login", methods=["POST"])
async def login():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    if username is None or password is None:
        return render_template("error.html", message="Bad username or password")

    token_data = await http_request.post("http://localhost:5000/token", json={"username": username, "password": password})
    if token_data.status_code != 200:
        return render_template("error.html", message="Bad username or password")

    response = make_response(render_template("content.html"))
    set_access_cookies(response, token_data.json()['token'])
    return response

@app.route("/token", methods=["POST"])
async def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = await User.find_by_email(username)
    if user is None or user['password'] != password:  # Verifique a senha aqui
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user['id'])
    return jsonify({"token": access_token, "user_id": user['id']})

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
async def get_users():
    conn = await get_db_connection()
    users = await conn.fetch("SELECT * FROM users;")
    await conn.close()
    return jsonify([{"id": user['id'], "name": user['name'], "email": user['email']} for user in users])

@app.route("/users/<int:id>", methods=["GET"])
async def get_user(id):
    conn = await get_db_connection()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1;", id)
    await conn.close()
    return jsonify({"id": user['id'], "name": user['name'], "email": user['email']})

@app.route("/users", methods=["POST"])
async def create_user():
    data = request.json
    conn = await get_db_connection()
    new_user_id = await conn.fetchval("INSERT INTO users (name, email, password) VALUES ($1, $2, $3) RETURNING id;", data["name"], data["email"], data["password"])
    await conn.close()
    return jsonify({"id": new_user_id, "name": data["name"], "email": data["email"]})

@app.route("/users/<int:id>", methods=["PUT"])
async def update_user(id):
    data = request.json
    conn = await get_db_connection()
    updated_user_id = await conn.fetchval("UPDATE users SET name = $1, email = $2, password = $3 WHERE id = $4 RETURNING id;", data["name"], data["email"], data["password"], id)
    await conn.close()
    return jsonify({"id": updated_user_id, "name": data["name"], "email": data["email"]})

@app.route("/users/<int:id>", methods=["DELETE"])
async def delete_user(id):
    conn = await get_db_connection()
    deleted_user_id = await conn.fetchval("DELETE FROM users WHERE id = $1 RETURNING id;", id)
    await conn.close()
    return jsonify({"id": deleted_user_id})

@app.route("/content", methods=["GET"])
@jwt_required()
def content():
    return render_template("content.html")

@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_db_connection())
    app.run(host="0.0.0.0", port=5000, debug=True)