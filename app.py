from flask import Flask, jsonify, request
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

students = [
    {
        "id": 1,
        "name": "John Michael Dela Peña",
        "grade": 10,
        "section": "Zechariah",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
]

@app.route('/')
def home():
    return jsonify({
        "message": "Student Management API",
        "status": "Running",
        "total_students": len(students)
    })


# GET all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)


# GET one student
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    for student in students:
        if student["id"] == id:
            return jsonify(student)

    return jsonify({"error": "Student not found"}), 404


# ADD student
@app.route('/students', methods=['POST'])
def add_student():

    data = request.json

    if not data or not data.get("name"):
        return jsonify({"error": "Name is required"}), 400

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
    })


# UPDATE student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):

    data = request.json

    for student in students:
        if student["id"] == id:

            student["name"] = data.get("name", student["name"])
            student["grade"] = data.get("grade", student["grade"])
            student["section"] = data.get("section", student["section"])

            return jsonify({
                "message": "Student updated",
                "student": student
            })

    return jsonify({"error": "Student not found"}), 404


# DELETE student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):

    for student in students:
        if student["id"] == id:
            students.remove(student)

            return jsonify({
                "message": "Student deleted"
            })

    return jsonify({"error": "Student not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
