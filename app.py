#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from flask import Flask, render_template, jsonify, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

db = SQLAlchemy(app)

def updateRecord(id_number,db):
   projectToUpdate = projects.query.filter_by(id=id_number).first()
   projectToUpdate.name = request.form['name']
   projectToUpdate.authors = request.form['authors']
   projectToUpdate.subjectName = request.form['subjectName']
   projectToUpdate.description = request.form['description']
   projectToUpdate.tags = request.form['tags']
   projectToUpdate.links = request.form['links']
   projectToUpdate.editDate = time.strftime("%H:%M:%S")
   db.session.commit()

def deleteRecord(id_number,db):
   projectToUpdate = projects.query.filter_by(id=id_number).first()
   projectToUpdate.deleteDate = time.strftime("%H:%M:%S")
   db.session.commit()

class projects(db.Model):
   id = db.Column('project_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   authors = db.Column(db.String(100))
   subjectName = db.Column(db.String(50)) 
   description = db.Column(db.String(1000))
   tags = db.Column(db.String(100))
   links = db.Column(db.String(100))
   pictures = db.Column(db.String(100))
   creationDate = db.Column(db.String(100))
   editDate = db.Column(db.String(100))
   deleteDate = db.Column(db.String(100))

   def __init__(self, name, authors,subjectName,description,tags,links):
      self.name = name
      self.authors = authors
      self.subjectName = subjectName
      self.description = description
      self.tags = tags
      self.links = links
      self.pictures = ""        #Upload zdjec i linki tutaj
      self.creationDate = time.strftime("%H:%M:%S");  #Wiem, Data, na razie jest godzina
      self.editDate =  time.strftime("%H:%M:%S");     #Wiem, Data, na razie jest godzina
      self.deleteDate = ""                            #Trzeba to przemyśleć.

@app.route('/')
def show_all():
   return render_template('show_all.html', projects = projects.query.all() )


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.now()
            filename = os.path.join(app.config['UPLOAD_FOLDER'], "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))
            file.save(filename)
            return jsonify({"success":True})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['authors'] or not request.form['subjectName'] or not request.form['description'] or not request.form['tags'] or not request.form['links']:
         flash('Please enter all the fields', 'error')
         return render_template('new.html', fields = request )
      else:
         project = projects(request.form['name'], request.form['authors'],request.form['subjectName'], request.form['description'],request.form['tags'], request.form['links'])
         db.session.add(project)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')


@app.route('/edit/<int:id_number>', methods = ['GET', 'POST'])
def edit_project(id_number):
   if request.method == 'POST':
      if not request.form['name'] or not request.form['authors'] or not request.form['subjectName'] or not request.form['description'] or not request.form['tags'] or not request.form['links']:
         flash('Please enter all the fields', 'error')
      else:
         updateRecord(id_number,db)
         #db.session.values(request.form['name'], request.form['authors'],request.form['subjectName'], request.form['description'],request.form['tags'], request.form['links'])
         flash('Record was successfully updated')
         return redirect(url_for('show_all'))
   return render_template('edit.html', project = projects.query.filter_by(id=id_number).first() )

@app.route('/delete_project/<int:id_number>', methods = ['GET', 'POST'])
def delete_project(id_number):
   if request.method == 'POST': 
      if request.form['submit']=="YES":
         deleteRecord(id_number,db)
      return redirect(url_for('show_all'))
   return render_template('delete_project.html', project = projects.query.filter_by(id=id_number).first()  )





if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)


def getProject(id_number):
   return projects.query.filter_by(id=id_number).first()


def getProjects(index,amount):
   return projects.query.filter_by(id>=index and id<(index+abount))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

