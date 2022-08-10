#a class that allows us to create an app
from flask import Flask, render_template
#start using the db objects
from flask_sqlalchemy import SQLAlchemy


# creates an app that gets named after the name of our file
app = Flask(__name__)

#configure the flask app to connectto a database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:#Datascience1@localhost:5432/mine'
#define a db object which links sqlaclemy tou the flsak app
db = SQLAlchemy(app)

#create a class todo item with column id and description
class Todo(db.Model):
    #specify the name of the table
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    # useful debugging statements when printing the objects
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

#sync our model with te database
db.create_all()
#this ensures the tables are created for all the models


#our goal is to allow a user to visit our homepage and see
# a list of to dos
#set up a rout that listens to our home page
@app.route('/')
#call the route handler index
def index():
    # return a template html 
    #modify our dummy data to include data that comes from
    #the database
    return render_template('index.html', data=Todo.query.all())



















if __name__ == '__main__':
   app.run(host="0.0.0.0")       