from flask import Flask, render_template, json, request
from manager import ClientManager, UserManager

app = Flask(__name__, template_folder='templates')

client = ClientManager()
user = UserManager()


@app.route('/')
@app.route('/main')
def main_page():
    return render_template("main_page.html",
                           title='Welcome!')


@app.route('/country_stat')
def country_stat():
    _country_stat = user.get_country_stat()
    return render_template('country_stat.html',
                           countries_stat=_country_stat)


@app.route('/specific_country_stat')
def specific_country_stat():
    country = 'Russia'
    stat_by_country = user.get_stat_by_country(country)
    return render_template('specific_country_stat.html', country=country,
                           specific_country_stat=stat_by_country)


@app.route('/get_stat_by_country', methods=['POST'])
def get_stat_by_country():
    country = request.form['country']
    stat_by_country = user.get_stat_by_country(country)
    return {'visits_count': stat_by_country}


@app.route('/pages')
def pages_stat():
    pages = user.get_pages_stat()
    return render_template('pages.html', pages=pages, website_name='<link>')


@app.route('/unique_users')
def unique_users_stat():
    unique_users = user.get_stat_about_unique_users()
    return render_template('unique_users.html',
                           unique_users=unique_users)


@app.route('/authorized_users')
def authorized_users_stat():
    #  authorized_users = client.get_stat_about_registered_users()
    return render_template('authorized_users.html')


@app.route('/registered_users')
def registered_users_stat():
    registered_users = client.get_stat_about_registered_users()
    return render_template('registered_users.html',
                           registered_users=registered_users)


@app.route('/half_hour_stat')
def stat_by_last_half_hour():
    half_hour_stat = user.get_stat_by_last_half_hour()
    return render_template('half_hour_stat.html',
                           half_hour=half_hour_stat)


@app.route('/today_stat')
def stat_by_last_day():
    today_stat = user.get_stat_by_last_day()
    count_of_visits = sum(today_stat.values())
    data = json.dumps(list(today_stat.values()))
    labels = json.dumps(list(today_stat.keys()))
    return render_template('last_day_stat.html', day=count_of_visits,
                           data=data, labels=labels)


@app.route('/month_stat')
def stat_by_last_month():
    month_stat = user.get_stat_by_last_month()
    count_of_visits = sum(month_stat.values())
    data = json.dumps(list(month_stat.values()))
    labels = json.dumps(list(month_stat.keys()))
    return render_template('last_month_stat.html', month=count_of_visits,
                           data=data, labels=labels)


@app.route('/downloads_stat')
def downloads_stat():
    # downloads = user.get_stat_about_unique_users()
    return render_template('downloads_stat.html')


@app.route('/user_likes')
def user_likes_stat():
    #  user_likes = user.get_stat_about_unique_users()
    return render_template('user_likes.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
