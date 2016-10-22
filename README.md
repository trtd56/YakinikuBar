# init

## Init

### DB setting

~~~
$ sqlite3 flaskr.db < schema.sql
$ python
>>> from yakiniku import init_db
>>> init_db()
~~~

### ChartJs setting

~~~
$ cd static/js
$ git clone https://github.com/chartjs/Chart.js.git
~~~

### Command setting

- add .bashrc

~~~
export YAKINIKU_SERVER={URL}
export YAKINIKU_USER={USER NAME}
function ay () {
    command curl $YAKINIKU_SERVER/push/$YAKINIKU_USER/$1
    }
function ry () {
    command curl $YAKINIKU_SERVER/reset/$YAKINIKU_USER
}
~~~

## How to use

- start app

~~~
$ python yakiniku.py
~~~

- add yakiniku point

~~~
$ curl {SERVER URL}/push/{USER NAME}/{POINT(1~3)}
$ ay {POINT(1~3)}
~~~

- reset yakiniku point

~~~
$ curl {SERVER URL}/reset/{USER NAME}
$ ry
~~~

## Ref

- http://jsdo.it/shuuuuun/oEji
