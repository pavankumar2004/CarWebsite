import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('carInfo.db')
c = conn.cursor()

# Create a table to store car records
c.execute('''
    CREATE TABLE cars ( body number,final_drive varchar(40),spec_region varchar(10),engine_type varchar(10), model_year number,model_grade varchar(20),fuel_type varchar(20)
);
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
