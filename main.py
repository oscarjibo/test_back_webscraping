from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from controller import web_scrapping_process

# Configurar la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
# Configurar Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Configurar usuarios (esto debería venir de una base de datos en un caso real)
users = {'oscar': {'password': 'password123'}, 'test_tus_datos': {'password': 'password123'}}

# Crear el modelo de usuario
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['password']
        user_info = users.get(username)
        if user_info and user_info['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Inicio de sesión inválido. Por favor verifique su nombre de usuario y contraseña.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/buscar', methods=['GET'])
@login_required
def buscar():
        id_documento = str(request.args.get('url'))
        response = web_scrapping_process(id_documento)
        print(response, type(response), len(response))
        print("=========== RESPONSE ===========")
        if len(response[0]) == 0:
            response_api = {"data": [], "status": "400", "detail": "No data"}
        else:
            response_api = {"data": response, "status": "200", "detail": "Execution complete"}
        if request.args.get('format') == 'json':
            return jsonify(response_api)
        return render_template('buscar.html', id_documento=id_documento, status_consulta=response[1], dataframe=response[0].to_html(classes='data', header="true"))


if __name__ == '__main__':
    app.run(debug=True, port=5000)