from flask import Flask, jsonify

app = Flask(__name__)

# Sample student data
students = [
    {"id": 1, "name": "John Michael Dela Peña", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "Maria Santos", "grade": 10, "section": "Faith"},
    {"id": 3, "name": "Juan Cruz", "grade": 10, "section": "Hope"}
]

# Home Route
@app.route('/')
def home():
    return """
    <h1>Student API</h1>
    <p>Available Routes:</p>
    <ul>
        <li>/students - View Student Table</li>
        <li>/api/students - View JSON API</li>
    </ul>
    """

# JSON API route
@app.route('/api/students')
def get_students():
    return jsonify(students)

# Student Table Page
@app.route('/students')
def student_table():

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Table</title>
        <style>
            body{
                font-family: Arial;
                background: linear-gradient(135deg,#667eea,#764ba2);
                color:white;
                text-align:center;
                padding:40px;
            }

            table{
                margin:auto;
                border-collapse: collapse;
                background:white;
                color:black;
                width:60%;
                box-shadow:0 5px 10px rgba(0,0,0,0.2);
            }

            th, td{
                padding:12px;
                border:1px solid #ddd;
            }

            th{
                background:#667eea;
                color:white;
            }

            tr:hover{
                background:#f2f2f2;
            }

            h1{
                margin-bottom:20px;
            }
        </style>
    </head>
    <body>

    <h1>Student List</h1>

    <table>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Grade</th>
            <th>Section</th>
        </tr>
    """

    for s in students:
        html += f"""
        <tr>
            <td>{s['id']}</td>
            <td>{s['name']}</td>
            <td>{s['grade']}</td>
            <td>{s['section']}</td>
        </tr>
        """

    html += """
    </table>

    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(debug=True)
