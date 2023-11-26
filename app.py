from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing'

# app.config['MONGO_dbname'] = 'users'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'

mongo = PyMongo(app)

@app.route("/")
@app.route("/main")
def main():
    return render_template('index.html')


@app.route("/studentsignup", methods=['POST', 'GET'])
def studentsignup():
    if request.method == 'POST':
        student = mongo.db.student
        signup_user = student.find_one({'username': request.form['username']})

        if signup_user:
            flash(request.form['username'] + ' username is already exist')
            return redirect(url_for('studentsignup'))

      #   hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
        student.insert_one({'username': request.form['username'], 'password': request.form['password'], 'email': request.form['email']})

        return redirect(url_for('studentsignin'))

    return render_template('studentsignup.html')

@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])

    return render_template('index.html')

@app.route('/studentsignin', methods=['GET', 'POST'])
def studentsignin():
    if request.method == 'POST':
        student = mongo.db.student
        signin_user = student.find_one({'username': request.form['username']})

        if signin_user:
            # if bcrypt.hashpw(request.form['password'].encode('utf-8'), signin_user['password'].encode('utf-8')) == \
                  #   signin_user['password'].encode('utf-8'):
                if signin_user['password']==request.form['password']:
                  session['username'] = request.form['username']
                  return redirect(url_for('index'))

      #   flash('Username and password combination is wrong')
        return render_template('studentsignin.html')

    return render_template('studentsignin.html')

@app.route('/teacherlogin', methods=['GET', 'POST'])
def teacherlogin():
    if request.method == 'POST':
        teacher = mongo.db.teacher
        signin_user = teacher.find_one({'username': request.form['username']})

        if signin_user:
            # if bcrypt.hashpw(request.form['password'].encode('utf-8'), signin_user['password'].encode('utf-8')) == \
                  #   signin_user['password'].encode('utf-8'):
                if signin_user['password']==request.form['password']:
                  session['username'] = request.form['username']
                  return redirect(url_for('index'))

      #   flash('Username and password combination is wrong')
        return render_template('teacherlogin.html')

    return render_template('teacherlogin.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
    app.run()