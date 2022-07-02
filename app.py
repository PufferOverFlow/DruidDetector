import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import os
import json
from functools import wraps
from flask import Flask, render_template, redirect, request, url_for, flash, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import main
import hashlib
import uuid
import shutil

app = Flask(__name__)
app.secret_key = 'DruidDetector'
app.config.from_object('config')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'DruidDetector'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['Upload'] = ['.apk']
mysql = MySQL(app)

class RegisterForm(Form):
    fullname = StringField('Full name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.data_required(),
        validators.equal_to('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')

def get_hash(filepath):
    with open(filepath,"rb") as f:
        f_byte= f.read()
        result = hashlib.sha256(f_byte)
    return result.hexdigest()

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route("/")
def init():
    return render_template('home.html')

@app.route("/file", methods=['POST'])
@is_logged_in
def load_apk():
    f = request.files['file']
    apkname = f.filename
    apkpath = f"loaded_apk/{apkname}"
    f.save(apkpath)
    genuuid = str(uuid.uuid4())
    sha256hash = get_hash(apkpath)
    app_permissions,permission_predictions, dex_predictions, ensimbled_prediction, round_to_tenths,img_path = main.flask_call(apkpath)
    result = "Benign" if ensimbled_prediction[0] > ensimbled_prediction[1] else "Malware"
    model_permission_result = "Benign" if permission_predictions[0][0] > permission_predictions[0][1] else "Malware"
    model_dex_result = "Benign" if dex_predictions[0][0] > dex_predictions[0][1] else "Malware"
    permissions = json.dumps(app_permissions)
    dex_image_name = img_path
    # dst = "static/dex_images"
    # shutil.copy(dex_image_name, dst)
    uploader = session['username']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO reports(procid, apkname, sha256hash, result, model_permission_result,model_dex_result,permissions,dex_image_name,uploader) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (genuuid, apkname, sha256hash, result, model_permission_result,model_dex_result,permissions,dex_image_name,uploader))
    mysql.connection.commit()
    cur.close()
    
    flash('Analysing APK Finished', 'success')
    return redirect(url_for('showResult',uuid=genuuid))

@app.route("/result/<uuid>", methods=['GET'])
@is_logged_in
def showResult(uuid):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM reports WHERE procid = %s", [uuid])
    if result > 0:
        data = cur.fetchone()
        perm=json.loads(data['permissions'])
    return render_template('result.html',data=data,perms=perm)


@app.route('/aboutus')
def about():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        fullname = form.fullname.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(fullname,username,email, password) VALUES (%s,%s,%s,%s)",
                    (fullname, username, email, password))
        mysql.connection.commit()
        cur.close()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('uploadApk'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            cur.close()
        else:
            error = "username not found"
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route('/upload')
@is_logged_in
def uploadApk():
    return render_template('upload_apk.html')


@app.route('/recent', methods=['GET'])
@is_logged_in
def recentscan():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM reports")
    if result > 0:
        data = cur.fetchall()
    return render_template('recent.html',data=data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port, threaded = True,debug=True)
