from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MoonStar@130925",
    database="employee_db"
)

cursor = db.cursor(buffered=True)


@app.route('/')
def login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def check_login():

    username = request.form['username']
    password = request.form['password']

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )

    user = cursor.fetchone()

    if user:
        return redirect('/dashboard')
    else:
        return "Invalid Login"


@app.route('/dashboard')
def dashboard():

    cursor.execute("SELECT COUNT(*) FROM employee")
    total_emp = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leave_requests")
    total_leave = cursor.fetchone()[0]

    return render_template(
        "dashboard.html",
        total_emp=total_emp,
        total_leave=total_leave
    )


@app.route('/add_employee')
def add_employee():
    return render_template("add_employee.html")


@app.route('/save_employee', methods=['POST'])
def save_employee():

    name = request.form['name']
    email = request.form['email']
    department = request.form['department']
    salary = request.form['salary']

    cursor.execute(
        "INSERT INTO employee(name,email,department,salary) VALUES(%s,%s,%s,%s)",
        (name, email, department, salary)
    )

    db.commit()

    return redirect('/view_employee')


@app.route('/view_employee')
def view_employee():

    search = request.args.get('search')

    if search:
        cursor.execute(
            "SELECT * FROM employee WHERE name LIKE %s OR department LIKE %s",
            ('%' + search + '%', '%' + search + '%')
        )
    else:
        cursor.execute("SELECT * FROM employee")

    employees = cursor.fetchall()

    return render_template("report.html", employees=employees)


@app.route('/delete/<int:id>')
def delete_employee(id):

    cursor.execute("DELETE FROM employee WHERE id=%s", (id,))
    db.commit()

    return redirect('/view_employee')


@app.route('/edit/<int:id>')
def edit_employee(id):

    cursor.execute("SELECT * FROM employee WHERE id=%s", (id,))
    employee = cursor.fetchone()

    return render_template("update_employee.html", employee=employee)


@app.route('/update/<int:id>', methods=['POST'])
def update_employee(id):

    name = request.form['name']
    email = request.form['email']
    department = request.form['department']
    salary = request.form['salary']

    cursor.execute(
        "UPDATE employee SET name=%s,email=%s,department=%s,salary=%s WHERE id=%s",
        (name, email, department, salary, id)
    )

    db.commit()

    return redirect('/view_employee')


@app.route('/leave')
def leave():
    return render_template("leave.html")


@app.route('/apply_leave', methods=['POST'])
def apply_leave():

    emp_name = request.form['emp_name']
    from_date = request.form['from_date']
    to_date = request.form['to_date']
    reason = request.form['reason']

    cursor.execute(
        "INSERT INTO leave_requests(emp_name,from_date,to_date,reason) VALUES(%s,%s,%s,%s)",
        (emp_name, from_date, to_date, reason)
    )

    db.commit()

    return redirect('/dashboard')


@app.route('/leave_report')
def leave_report():

    cursor.execute("SELECT * FROM leave_requests")
    leaves = cursor.fetchall()

    return render_template("leave_report.html", leaves=leaves)


if __name__ == '__main__':
    app.run(debug=True)