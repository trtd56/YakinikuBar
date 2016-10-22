# -*- coding: utf-8 -*-

import os
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

# setting
DATABASE = 'yakiniku.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('YAKINIKU_SETTINGS', silent=True)


def point_check(point):
    point = int(point)
    if not 0 < point < 4:
        raise ValueError
    return point

def get_latest(name):
    cur = g.db.execute('select name, feeling from entries order by id desc')
    datas = [dict(name=row[0], feeling=row[1]) for row in cur.fetchall()]
    res = False
    for d in datas:
        if d['name'] == name:
            feeling = d["feeling"]
            res = {"name":name,"feeling":feeling}
    return res


# connect DB
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# init DB
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# before request
@app.before_request
def before_request():
    g.db = connect_db()

# adter request
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    cur = g.db.execute('select name, feeling from entries order by id desc')
    datas = [dict(name=row[0], feeling=row[1]) for row in cur.fetchall()]
    # index.htmlにcontensを引数に渡して実行。
    return render_template("index.html", contents=datas)

@app.route('/push/<name>/<point>')
def add_yakiniku_point(name, point):
    try:
        add_point = point_check(point)
    except ValueError:
        return "ValueError:\nThe range of values which the Yakiniku Point can take should be larger than 1 and no more than 3.\n"
    res = get_latest(name)
    if res:
        new_p = add_point + int(res["feeling"])
        g.db.execute('UPDATE entries SET feeling=? WHERE name=?',(new_p, str(name)))
        g.db.commit()
    else:
        g.db.execute('insert into entries (name, feeling) values (?, ?)',[name, point])
        g.db.commit()
    return "UPDATE YAKINIKU POINT!!\n"

@app.route('/reset/<name>')
def reset_yakiniku_point(name):
    res = get_latest(name)
    if res:
        g.db.execute('UPDATE entries SET feeling=? WHERE name=?',(0, str(name)))
        g.db.commit()
        return "Good!!\n"
    else:
        return "The user is not registered.\n"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
