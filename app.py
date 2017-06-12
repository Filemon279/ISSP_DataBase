#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################
#	IMPORT BIBLIOTEK				#
#####################################
import os
from datetime import datetime
from flask import Flask, render_template, jsonify, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import time

#####################################
#		KONFIGURACJA				#
#####################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

db = SQLAlchemy(app)

#####################################
#	AKTUALIZACJA REKORDU			#
#####################################
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

#####################################
#	DODAWANIE ZDJĘCIA				#
#####################################
def addPhoto(id_number,db,photo_URL):
   projectToUpdate = projects.query.filter_by(id=id_number).first()
   if (projectToUpdate.pictures==""): projectToUpdate.pictures += photo_URL
   else: projectToUpdate.pictures += ","+photo_URL
   db.session.commit()

#####################################
#	USUWANIE REKORDU				#
#####################################
def deleteRecord(id_number,db):
   projectToUpdate = projects.query.filter_by(id=id_number).first()
   projectToUpdate.deleteDate = time.strftime("%H:%M:%S")
   db.session.commit()

#####################################
#	MODEL PROJEKTU DO BAZY DANYCH	#
#####################################
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

######################################
#TEMPLATE - INDEX PRZEKAZUJE WSZYSTKO#
######################################
@app.route('/')
def show_all():
   return render_template('show_all.html', projects = projects.query.all() )


#####################################
#	PRZEKAZYWANIE PLIKU DO FOLDERU 	#
#####################################
@app.route('/upload/<int:id_number>', methods=['POST'])
def upload(id_number):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.now()
            if not os.path.exists(app.config['UPLOAD_FOLDER']+"/"+str(id_number)):
               os.makedirs(app.config['UPLOAD_FOLDER']+"/"+str(id_number))
            filename = os.path.join(app.config['UPLOAD_FOLDER']+"/"+str(id_number), "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))
            file.save(filename)
            addPhoto(id_number,db,filename)
            return jsonify({"success":True})

#####################################
#	NAZWA ORAZ ROZSZERZENIE			#
#####################################
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#####################################
#	TEMPLATE DODAWANIA REKORDU		#
#####################################
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
         #flash('Record was successfully added')
         return redirect(url_for('upload_Photos',id_number=project.id))
   return render_template('new.html')


#####################################
#	DODAWANIE ZDJECIA TEMPLATE		#
#####################################
@app.route('/uploadPhotos/<int:id_number>', methods = ['GET', 'POST'])
def upload_Photos(id_number):
   if request.method == 'POST':
      if not request.form['name'] or not request.form['authors'] or not request.form['subjectName'] or not request.form['description'] or not request.form['tags'] or not request.form['links']:
         flash('Please enter all the fields', 'error')
      else:
         updateRecord(id_number,db)
         flash('Record was successfully updated')
         return redirect(url_for('show_all'))
   return render_template('uploadPhotos.html', project = projects.query.filter_by(id=id_number).first() )


#####################################
#	EDYTOWANIE WPISU				#
#####################################
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
   projectObject = projects.query.filter_by(id=id_number).first(); 
   pics_array = projectObject.pictures.split(",")
   print(pics_array)
   return render_template('edit.html', project =projectObject , pictures=pics_array )

#####################################
#	USUWANIE PROJEKTU				#
#####################################
@app.route('/delete_project/<int:id_number>', methods = ['GET', 'POST'])
def delete_project(id_number):
   if request.method == 'POST': 
      if request.form['submit']=="YES":
         deleteRecord(id_number,db)
      return redirect(url_for('show_all'))
   return render_template('delete_project.html', project = projects.query.filter_by(id=id_number).first()  )

#####################################
#	USUWANIE ZDJECIA Z BAZY			#
#####################################
@app.route('/delete_pic/<int:id_number>/<picture>', methods = ['GET','POST'])
def delete_pic(id_number,picture):
   projectToUpdate = projects.query.filter_by(id=id_number).first()
   pics_array = projectToUpdate.pictures.split(",")
   del pics_array[int(picture)]
   projectToUpdate.pictures = ",".join(pics_array)
   db.session.commit()
   return redirect(url_for('edit_project',id_number=id_number))




#####################################
#	IMPORT BIBLIOTEK				#
#####################################
if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)

#####################################
#	WEZ JEDEN PROJEKT				#
#####################################
def getProject(id_number):
   return projects.query.filter_by(id=id_number).first()

#####################################
#	WEZ PROJEKTY OD INDEXU + LICZBA	#
#####################################
def getProjects(index,amount):
   return projects.query.filter_by(id>=index and id<(index+abount))
