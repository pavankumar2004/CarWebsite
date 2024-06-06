from flask import Flask
from flask import render_template
import sqlite3
app = Flask(__name__)


#connect = sqlite3.connect('database.db') 
#connect.execute( 
#    'CREATE TABLE IF NOT EXISTS cars (image BLOB, marque TEXT,  modele TEXT, annee TEXT, kilometrage TEXT, carburant TEXT, puissance TEXT, moteur TEXT, boite TEXT, options TEXT)') 

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/listing')
def listing():
   # conn = sqlite3.connect('database.db') 
   # conn.execute('SELECT image FROM cars')
   # return render_template('listing.html')
   conn = sqlite3.connect('database.db')
   cursor = conn.cursor()
   cursor.execute('SELECT imagepath FROM cars')  # Assuming 'image' is the column name for the image paths
   cars = cursor.fetchall()
   conn.close()

    # Extract image paths from the result
   image_paths = [car[0] for car in cars if car[0] is not None]

   return render_template('listing.html', image_paths=image_paths)


@app.route('/contact')
def contact():
   return render_template('contact.html')



# @app.route('/hello/<name>')
# def hello_name(name):
#    return 'Hello %s!' % name

if __name__ == '__main__':
   app.run()
