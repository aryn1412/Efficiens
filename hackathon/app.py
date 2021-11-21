from flask import Flask , render_template , url_for , redirect , request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "yoyoyoyo"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_BINDS'] = {'two' : 'sqlite:///tasks.sqlite3'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
userr = []
addd = 1
class User(db.Model):
    id = db.Column("id" , db.Integer , primary_key=True)
    user_name = db.Column(db.String(100))
    most = db.Column(db.String(100))
    mid = db.Column(db.String(100))
    least = db.Column(db.String(100))
    completed_tasks = db.Column(db.String(100))
    def __repr__(self):
        return f"User('{self.user_name}' , '{self.completed_tasks}' ,'{self.most}' , '{self.mid}' , '{self.least}' )"
class Tasks(db.Model):
    id = db.Column("id" , db.Integer , primary_key=True)
    name = db.Column(db.String(100))
    difficult = db.Column(db.String(100))
    suggested = db.Column(db.String(100))
    time = db.Column(db.String(100))
    def __repr__(self):
        return f"Tasks('{self.name}' , '{self.difficult}' , '{self.time}' , '{self.suggested}' )"

@app.route("/" , methods = ["POST" , "GET"])
def info():
    global userr
    if request.method == "POST":
        userr = User(user_name = request.form.get("user") , most = request.form.get("pt") , mid = request.form.get("pt3") , least = request.form.get("pt2") , completed_tasks = "0")
        db.session.add(userr)
        db.session.commit()
        print(request.form.get("user"))
        print(User.query.all())
        return redirect(url_for("start"))
    return render_template("info.html")

@app.route("/start" , methods = ["POST" , "GET"])
def start():
    return render_template("start.html" , data = Tasks.query.all())
    
@app.route("/add" , methods = ["POST" , "GET"])
def add():
    if request.method == "POST":
        task = Tasks(name = request.form.get("name") , difficult = request.form.get("difficulty") , suggested = request.form.get("dif") ,  time =request.form.get("Estimated_time"))
        db.session.add(task)
        db.session.commit()
        print(Tasks.query.all())
    return render_template("add.html")

@app.route("/taskz" , methods = ["POST" , "GET"])
def taskz():
    global addd
    if request.method == "POST":
        Tasks.query.filter_by(name = request.form.get("task_del")).delete()
        db.session.commit()
        User.query.all()[-1].completed_tasks = str(int(User.query.all()[-1].completed_tasks) + 1)
        db.session.commit()
        print(User.query.all())
    data_all = Tasks.query.all()
    print(data_all)
    return render_template("tasks.html" , all = data_all , timez = User.query.all()[-1])

@app.route("/track" , methods = ["POST" , "GET"])
def track():
    return render_template("track.html" , points = int(User.query.all()[-1].completed_tasks) )

if __name__ == "__main__":
    db.create_all()
    db.create_all(bind=['two'])
    app.run(debug = True)