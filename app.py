#a class that allows us to create an app
from flask import Flask, render_template, request, redirect, url_for, jsonify
#start using the db objects
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys


# creates an app that gets named after the name of our file
app = Flask(__name__)

#configure the flask app to connectto a database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:#Datascience1@localhost:5432/mine1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#define a db object which links sqlaclemy tou the flsak app
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#create a class todo item with column id and description
class Todo(db.Model):
    #specify the name of the table
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)

    # useful debugging statements when printing the objects
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

#sync our model with te database
db.create_all()
#this ensures the tables are created for all the models

#define a route that listens todos/create and listens to
#requests that come in with a method post
@app.route('/todos/create', methods=['POST'])
def create_todo():
    body = {}
    error=False
    try:
        #description = request.form.get('description', '') or
        description = request.get_json()['description'] # fetches the json body that was sent to it
        #create a new todo object
        todo = Todo(description=description, completed=False) 
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['completed'] = todo.completed
        body['description'] = todo.description

    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
    if not error:
        #redirect to the index route and reshow the indexpage 
        #return redirect(url_for('index'))or
        return jsonify(body)
        # or return render_template('index.html', data=Todo.query.all())

#defining a handler for the route that listens to a post request
# that comes in
#grab the todo id from the route itself
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))            



#our goal is to allow a user to visit our homepage and see
# a list of to dos
#set up a rout that listens to our home page
@app.route('/')
#call the route handler index
def index():
    # return a template html 
    #modify our dummy data to include data that comes from
    #the database
    return render_template('index.html', data=Todo.query.order_by('id').all())



















if __name__ == '__main__':
   app.run(host="0.0.0.0")       