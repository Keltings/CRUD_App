#a class that allows us to create an app
from flask import Flask, render_template

# creates an app that gets named after the name of our file
app = Flask(__name__)

#our goal is to allow a user to visit our homepage and see
# a list of to dos
#set up a rout that listens to our home page
@app.route('/')
#call the route handler index
def index():
    # return a template html 
    return render_template('index.html', data=[
       {'description': 'Todo 1'},
       {'description': 'Todo 2'},
       {'description': 'Todo 3'},
       {'description': 'Todo 4'}])



















if __name__ == '__main__':
   app.run(host="0.0.0.0")       