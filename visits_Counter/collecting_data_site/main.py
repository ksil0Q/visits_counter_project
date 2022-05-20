from flask import Flask, render_template, request, make_response, \
    redirect, url_for, flash
from manager import UserManager, ClientManager
from models import DataError, ClientData, UserData, Cookies
from werkzeug.security import generate_password_hash

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'cc3f74cd316a4153a9441e9e1e862b44'

db_user = UserManager()
db_client = ClientManager()


@app.route('/')
@app.route('/main')
def main_page():
    cookies = Cookies(request)
    user = UserData(ip='159.65.207.71',
                    user_cookies_uuid=cookies.get_str_cookies_uuid(),
                    page=request.path)
    db_user.add_visits(user.get_user_info())

    return render_template("main_page.html", title='Welcome!')


@app.route('/registration', methods=['GET', 'POST'])
def register():
    cookies = Cookies(request)
    user = UserData(ip='159.65.207.71',
                    user_cookies_uuid=cookies.get_str_cookies_uuid(),
                    page=request.path)

    db_user.add_visits(user.get_user_info())

    if request.method == 'POST':
        nickname = request.form['name']
        email = request.form['email']
        psw = request.form['psw']
        psw2 = request.form['psw2']
        data_error = DataError()
        data_error.is_correct_data(nickname, email, psw, psw2)

        if data_error.validity:
            password_hash = generate_password_hash(psw)
            cookies_uuid = user.user_cookies_uuid
            client = ClientData(nickname, email, password_hash, cookies_uuid)

            db_client.add_client(client.get_client_info())

            server_response = make_response(redirect(url_for('vip_page')))

            server_response.set_cookie('usr',
                                       value=cookies.cookie['uuid'].value,
                                       domain=cookies.cookie['uuid']['domain'],
                                       path=cookies.cookie['uuid']['path'],
                                       secure=cookies.cookie['uuid']['secure'],
                                       httponly=cookies.cookie['uuid'][
                                           'httponly'],
                                       expires=cookies.cookie['uuid'][
                                           'expires'])
            flash(data_error.message)
            return server_response
        else:
            flash(data_error.message)
    return render_template('register.html', title='Log on')


@app.route('/login', methods=['GET', 'POST'])
def login():
    cookies = Cookies(request)
    user = UserData(ip='94.140.141.124',
                    user_cookies_uuid=cookies.get_str_cookies_uuid(),
                    page=request.path)

    db_user.add_visits(user.get_user_info())

    if request.method == 'POST':
        try:
            nickname = request.form.get('nickname')
            psw = request.form.get('psw')
            if db_client.is_registered(nickname, psw):
                return redirect(url_for('vip_page'))
            else:
                flash('Incorrect username or password ;(((')
        except OSError:
            flash('something wen`t wrong, try again..')
            return render_template('login.html', title='Log in')
    return render_template('login.html', title='Log in')


@app.route('/vip_page', methods=['GET', 'POST'])
def vip_page():
    if not request.cookies.get('usr'):
        cookies = Cookies(request)
        user = UserData(ip='94.140.141.124',
                        user_cookies_uuid=cookies.get_str_cookies_uuid(),
                        page=request.path)

        db_user.add_visits(user.get_user_info())
    elif not db_client.is_registered(request.cookies.get('usr')):
        redirect(url_for('register'))

    count_of_clients = db_client.number_of_logged_in_clients()
    return render_template('vip_page.html', title='Bump!',
                           count_of_clients=count_of_clients)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
