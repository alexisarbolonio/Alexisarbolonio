from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Temporary database
students = [
    {
        "id": 1,
        "name": "John Michael Dela Peña",
        "grade": 10,
        "section": "Zechariah",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
]

# Home Route
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Enhanced Flask Student API",
        "total_students": len(students),
        "routes": {
            "View All Students": "GET /students",
            "Get Student by ID": "GET /students/<id>",
            "Search Student": "GET /students/search?name=juan",
            "Add Student": "POST /students",
            "Update Student": "PUT /students/<id>",
            "Delete Student": "DELETE /students/<id>"
        }
    })


# Get all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({
        "total": len(students),
        "students": students
    })


# Get student by ID
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    for student in students:
        if student["id"] == id:
            return jsonify(student)

    return jsonify({
        "error": "Student not found"
    }), 404


# Search student
@app.route('/students/search', methods=['GET'])
def search_student():
    name = request.args.get("name")

    results = [
        s for s in students
        if name.lower() in s["name"].lower()
    ]

    if results:
        return jsonify(results)

    return jsonify({
        "message": "No matching student found"
    })


# Add student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.json

    if not data or not data.get("name"):
        return jsonify({
            "error": "Student name is required"
        }), 400

    new_student = {
        "id": len(students) + 1,
        "name": data.get("name"),
        "grade": data.get("grade"),
        "section": data.get("section"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    students.append(new_student)

    return jsonify({
        "message": "Student added successfully",
        "student": new_student
    }), 201


# Update student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.json

    for student in students:
        if student["id"] == id:

            student["name"] = data.get("name", student["name"])
            student["grade"] = data.get("grade", student["grade"])
            student["section"] = data.get("section", student["section"])

            return jsonify({
                "message": "Student updated successfully",
                "student": student
            })

    return jsonify({
        "error": "Student not found"
    }), 404


# Delete student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    for student in students:
        if student["id"] == id:
            students.remove(student)

            return jsonify({
                "message": "Student deleted successfully",
                "remaining_students": len(students)
            })

    return jsonify({
        "error": "Student not found"
    }), 404


# Run server
if __name__ == "__main__":
    app.run(debug=True)
