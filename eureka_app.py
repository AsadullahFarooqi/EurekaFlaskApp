import os
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
# from .user_form import UserForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///{}".format(
  os.path.join(os.path.dirname(os.path.abspath(__file__)),
   "users.db"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

@app.route("/", methods=['GET'])
def list_usrs():
  users_list = Users.query.all()
  title = "Eureka Users List"
  return render_template('list.html', users_list=users_list, title=title)

@app.route("/create/", methods=['GET', 'POST'])
def create_usr():
  if request.method == 'POST':
    user = Users(username=request.form.get("username"))
    db.session.add(user)
    db.session.commit()
    return redirect('/')
  title = "Add New User"
  return render_template('create.html', title=title)

@app.route("/edit/<user_id>/",  methods=['GET', 'POST'])
def edit_usr(user_id=None):
  user = db.session.query(Users).get(user_id)
  if request.method == 'POST':
    new_name = request.form.get("username")
    user = Users.query.filter_by(id=user_id).update(dict(username=new_name))
    db.session.commit()
    return redirect('/')
  title = "Edit User"
  return render_template("create.html", user=user, title=title)

@app.route("/delete/<user_id>/")
def delete_usr(user_id=None):
  user = db.session.query(Users).get(user_id)
  db.session.delete(user)
  db.session.commit()
  return redirect('/')

if __name__ == '__main__':
  db.create_all()
  app.run()