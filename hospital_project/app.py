from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",  
    database="hospital_compare"
)

@app.route('/')
def home():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM hospitals")
    data = cursor.fetchall()
    return render_template("index.html", hospitals=data)


@app.route('/add', methods=['GET', 'POST'])
def add_hospital():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        treatment = request.form['treatment']
        cost = request.form['cost']
        rating = request.form['rating']
        icu = request.form['icu']
        ambulance = request.form['ambulance']

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO hospitals 
            (hospital_name, city, treatment, avg_cost, rating, icu_available, ambulance_available)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, city, treatment, cost, rating, icu, ambulance))

        db.commit()
        return redirect('/')

    return render_template("add.html")


@app.route('/delete/<int:id>')
def delete_hospital(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM hospitals WHERE id = %s", (id,))
    db.commit()
    return redirect('/')
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_hospital(id):
    cursor = db.cursor()
    
    # GET request → show form with existing data
    if request.method == 'GET':
        cursor.execute("SELECT * FROM hospitals WHERE id = %s", (id,))
        data = cursor.fetchone()
        return render_template("edit.html", hospital=data)

    # POST request → update data
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        treatment = request.form['treatment']
        cost = request.form['cost']
        rating = request.form['rating']
        icu = request.form['icu']
        ambulance = request.form['ambulance']

        cursor.execute("""
            UPDATE hospitals 
            SET hospital_name=%s, city=%s, treatment=%s, avg_cost=%s, rating=%s, icu_available=%s, ambulance_available=%s
            WHERE id=%s
        """, (name, city, treatment, cost, rating, icu, ambulance, id))

        db.commit()
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)