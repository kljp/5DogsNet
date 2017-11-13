# from __future__ import with_statement
# from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template,flash
import os
from werkzeug import secure_filename
from flask import send_from_directory
import time
import classifyLabel

DATABASE = os.path.abspath('tmp/flaskr.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
UPLOAD_FOLDER = os.path.abspath('upload')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object(__name__)

# def init_db():
#
#     with closing(connect_db()) as db:
#         with app.open_resource('schema.sql') as f:
#             db.cursor().executescript(f.read())
#         db.commit()


def connect_db():

    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():

    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):

    g.db.close()

@app.route('/', methods=['GET', 'POST'])
def show_entries():

    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    model = classifyLabel.build_model([64, 64, 3])
    model.load_weights('./model/dog-model.hdf5')

    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        now = time.localtime()
        timeFormat = "%04d-%02d-%02d_%02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        filename = timeFormat + '__' + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('New file was successfully uploaded')
        filename = os.path.abspath('upload/' + filename)
        flash(classifyLabel.main(model, filename))

    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():

    if not session.get('logged_in'):
        abort(401)

    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')

    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')

            return redirect(url_for('show_entries'))

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():

    session.pop('logged_in', None)
    flash('You were logged out')

    return redirect(url_for('show_entries'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form action="" method=post enctype=multipart/form-data>
    #   <p><input type=file name=file>
    #      <input type=submit value=Upload>
    # </form>
    # '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':

    app.run()
