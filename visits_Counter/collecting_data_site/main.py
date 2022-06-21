from flask import Flask
from routes import routes

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'cc3f74cd316a4153a9441e9e1e862b44'
app.register_blueprint(routes, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
