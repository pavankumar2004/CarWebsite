import streamlit as st
import sqlite3
import bcrypt
import pandas as pd

# Function to get database connection
def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

# Function to hash a password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to check if a password matches the hash
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Signup page
def signup():
    st.title('Signup')

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')

    if st.button('Signup'):
        if password != confirm_password:
            st.error('Passwords do not match!')
        else:
            conn = get_db_connection('users.db')
            hashed_password = hash_password(password)
            try:
                conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
                conn.commit()
                st.success('Signup successful!')
            except sqlite3.IntegrityError:
                st.error('Username already exists!')
            finally:
                conn.close()

    if st.button('Back to Login'):
        st.session_state['show_signup'] = False
        st.experimental_rerun()

# Login page
def login():
    st.title('Login')

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        conn = get_db_connection('users.db')
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password(password, user['password']):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success('Login successful!')
            st.experimental_rerun()
        else:
            st.error('Invalid username or password')

    if st.button("Don't have an account? Signup here"):
        st.session_state['show_signup'] = True
        st.experimental_rerun()

# Main application with authentication
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if 'show_signup' not in st.session_state:
        st.session_state['show_signup'] = False

    if st.session_state['logged_in']:
        st.sidebar.title(f"Welcome, {st.session_state['username']}")
        st.sidebar.button('Logout', on_click=logout)

        page = st.sidebar.selectbox('Select Page', ['Add Car', 'Update Car', 'Delete Car', 'View Cars'])

        if page == 'Add Car':
            add_car()
        elif page == 'Update Car':
            update_car()
        elif page == 'Delete Car':
            delete_car()
        elif page == 'View Cars':
            view_cars()
    else:
        if st.session_state['show_signup']:
            signup()
        else:
            login()

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.experimental_rerun()

# Add, Update, Delete, View Car Functions (as defined previously)
def add_car():
    st.title('Add New Car')

    body = st.text_input('Body')
    final_drive = st.text_input('Final Drive')
    spec_region = st.text_input('Spec Region')
    engine_type = st.text_input('Engine Type')
    model_year = st.number_input('Model Year', min_value=1886, max_value=2050, step=1)
    model_grade = st.text_input('Model Grade')
    fuel_type = st.text_input('Fuel Type')

    if st.button('Add Car'):
        conn = get_db_connection('carInfo.db')
        
        # Get the latest ID in the database
        latest_id = conn.execute('SELECT MAX(id) FROM cars').fetchone()[0]
        
        # Increment the ID for the new record
        new_id = 1 if latest_id is None else latest_id + 1

        # Insert the new car record with the generated ID
        conn.execute('INSERT INTO cars (id, body, final_drive, spec_region, engine_type, model_year, model_grade, fuel_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                     (new_id, body, final_drive, spec_region, engine_type, model_year, model_grade, fuel_type))
        conn.commit()
        conn.close()
        st.success('Car added successfully!')

def update_car():
    st.title('Update Car')

    conn = get_db_connection('carInfo.db')
    cars = conn.execute('SELECT * FROM cars').fetchall()
    conn.close()

    car_ids = [car['id'] for car in cars]
    selected_car_id = st.selectbox('Select Car ID', car_ids)

    if selected_car_id:
        selected_car = [car for car in cars if car['id'] == selected_car_id][0]

        body = st.text_input('Body', value=selected_car['body'])
        final_drive = st.text_input('Final Drive', value=selected_car['final_drive'])
        spec_region = st.text_input('Spec Region', value=selected_car['spec_region'])
        engine_type = st.text_input('Engine Type', value=selected_car['engine_type'])
        model_year = st.number_input('Model Year', min_value=1886, max_value=2050, step=1, value=selected_car['model_year'])
        model_grade = st.text_input('Model Grade', value=selected_car['model_grade'])
        fuel_type = st.text_input('Fuel Type', value=selected_car['fuel_type'])

        if st.button('Update Car'):
            conn = get_db_connection('carInfo.db')
            conn.execute('''
                UPDATE cars
                SET body = ?, final_drive = ?, spec_region = ?, engine_type = ?, model_year = ?, model_grade = ?, fuel_type = ?
                WHERE id = ?
            ''', (body, final_drive, spec_region, engine_type, model_year, model_grade, fuel_type, selected_car_id))
            conn.commit()
            conn.close()
            st.success('Car updated successfully!')

def delete_car():
    st.title('Delete Car')

    conn = get_db_connection('carInfo.db')
    cars = conn.execute('SELECT * FROM cars').fetchall()
    conn.close()

    car_ids = [car['id'] for car in cars]
    selected_car_id = st.selectbox('Select Car ID', car_ids)

    if st.button('Delete Car'):
        conn = get_db_connection('carInfo.db')
        conn.execute('DELETE FROM cars WHERE id = ?', (selected_car_id,))
        conn.commit()
        conn.close()
        st.success('Car deleted successfully!')

def view_cars():
    st.title('View All Cars')

    conn = get_db_connection('carInfo.db')
    cars = conn.execute('SELECT * FROM cars').fetchall()
    conn.close()

    if cars:
        # Convert the fetched data to a DataFrame
        df = pd.DataFrame(cars, columns=['id', 'body', 'final_drive', 'spec_region', 'engine_type', 'model_year', 'model_grade', 'fuel_type'])

        # Display the DataFrame as a table
        st.dataframe(df, width=1000, height=600)
    else:
        st.write("No cars found.")

if __name__ == '__main__':
    st.title('Car Inventory Admin Page')
    main()
