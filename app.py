from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


def get_db():
    return sqlite3.connect("students.db")


def create_table():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        grade TEXT,
        section TEXT,
        photo TEXT
    )
    """)
    conn.close()


create_table()


# LOGIN PAGE
@app.route('/login', methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect("/")
    
    return """
    <html>
    <head>
    <title>Login</title>

    <link rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">

    </head>

    <body class="bg-primary">

    <div class="container mt-5">

    <div class="card p-4">

    <h3>Login</h3>

    <form method="POST">

    <input class="form-control mb-2" name="username" placeholder="Username">

    <input class="form-control mb-2" name="password" type="password" placeholder="Password">

    <button class="btn btn-primary">Login</button>

    </form>

    </div>

    </div>

    </body>
    </html>
    """


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")


# DASHBOARD
@app.route('/')
def home():

    if "user" not in session:
        return redirect("/login")

    search = request.args.get("search","")

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ('%'+search+'%',)
    ).fetchall()

    total = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]

    conn.close()

    html = f"""
    <html>
    <head>

    <title>Student Dashboard</title>

    <link rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">

    </head>

    <body class="bg-primary">

    <div class="container mt-4">

    <h2 class="text-white">Student Management Dashboard</h2>

    <a href="/logout" class="btn btn-danger mb-3">Logout</a>

    <div class="card p-3">

    <h5>Total Students: {total}</h5>

    <form method="GET" class="mb-3">

    <input name="search" class="form-control" placeholder="Search student">

    </form>

    <h5>Add Student</h5>

    <form method="POST" action="/add">

    <input class="form-control mb-2" name="name" placeholder="Name">

    <input class="form-control mb-2" name="grade" placeholder="Grade">

    <input class="form-control mb-2" name="section" placeholder="Section">

    <input class="form-control mb-2" name="photo" placeholder="Photo URL">

    <button class="btn btn-primary">Add Student</button>

    </form>

    <hr>

    <table class="table table-bordered">

    <tr>
    <th>ID</th>
    <th>Photo</th>
    <th>Name</th>
    <th>Grade</th>
    <th>Section</th>
    <th>Action</th>
    </tr>
    """

    for s in students:

        html += f"""
        <tr>
        <td>{s[0]}</td>

        <td>
        <img src="{s[4]}" width="50">
        </td>

        <td>{s[1]}</td>
        <td>{s[2]}</td>
        <td>{s[3]}</td>

        <td>
        <a class="btn btn-warning btn-sm" href="/edit/{s[0]}">Edit</a>
        <a class="btn btn-danger btn-sm" href="/delete/{s[0]}">Delete</a>
        </td>

        </tr>
        """

    html += """
    </table>

    </div>

    </div>

    </body>
    </html>
    """

    return html


@app.route('/add', methods=["POST"])
def add():

    conn = get_db()

    conn.execute(
        "INSERT INTO students(name,grade,section,photo) VALUES(?,?,?,?)",
        (
            request.form["name"],
            request.form["grade"],
            request.form["section"],
            request.form["photo"]
        )
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route('/delete/<int:id>')
def delete(id):

    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


@app.route('/edit/<int:id>', methods=["GET","POST"])
def edit(id):

    conn = get_db()

    if request.method == "POST":

        conn.execute(
            "UPDATE students SET name=?,grade=?,section=?,photo=? WHERE id=?",
            (
                request.form["name"],
                request.form["grade"],
                request.form["section"],
                request.form["photo"],
                id
            )
        )

        conn.commit()
        conn.close()

        return redirect("/")

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return f"""
    <html>
    <head>

    <link rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">

    </head>

    <body class="bg-primary">

    <div class="container mt-5">

    <div class="card p-3">

    <h3>Edit Student</h3>

    <form method="POST">

    <input class="form-control mb-2" name="name" value="{student[1]}">

    <input class="form-control mb-2" name="grade" value="{student[2]}">

    <input class="form-control mb-2" name="section" value="{student[3]}">

    <input class="form-control mb-2" name="photo" value="{student[4]}">

    <button class="btn btn-primary">Update</button>

    </form>

    </div>

    </div>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
