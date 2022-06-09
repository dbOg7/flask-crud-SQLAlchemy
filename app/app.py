from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __str__(self):
        return f'<Student {self.name}>'


def create_db():
    db.create_all()
    return create_db


@app.route('/')
def home():
    create_db()
    return render_template('crud/home.html', students = Students.query.all())


@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        
        student = Students(name=name)
        db.session.add(student)
        db.session.commit()


        return redirect(url_for('home'))
    return render_template('crud/create.html')


@app.route('/<int:id>/update/',methods = ['GET','POST'])
def update(id):
    students = Students.query.filter_by(id=id).first()
    if request.method == 'POST':
        if students:
            db.session.delete(students)
            db.session.commit()
 
            name = request.form['name']
            
            students = Students(name=name)
 
            db.session.add(students)
            db.session.commit()

            return redirect('/')
 
    return render_template('crud/update.html', students = students)


@app.route('/<int:id>/delete/', methods=['GET','POST'])
def delete(id):
    students = Students.query.filter_by(id=id).first()
    if request.method == 'POST':
        if students:
            db.session.delete(students)
            db.session.commit()
            return redirect('/')
 
    return render_template('crud/delete.html', students = students)
