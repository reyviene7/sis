from flask import Flask, jsonify, request, render_template
import sys
import psycopg2

# Database connection

db_connection = psycopg2.connect(
        dbname='apiDB',
        user='postgres',
        password='1234',
        host='localhost',
    )

app = Flask(__name__)

def spcall(qry, param, commit=False):
    try:
        cursor = db_connection.cursor()
        cursor.callproc(qry, param)
        res = cursor.fetchall()
        if commit:
            db_connection.commit()
        return res
    except:
        res = [("Error: " + str(sys.exc_info()[0]) +
                " " + str(sys.exc_info()[1]),)]
    return res

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courses', methods=['GET'])
def get_courses():
    try:
        courses=spcall('get_courses', param=None)[0][0]
        return jsonify({"status": "ok",
                        'data': courses})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/course', methods=['POST'])
def create_course():
    data = request.get_json()
    course = data.get('courseName')  # Adjust to match the key used in the JavaScript fetch request
    try:
        if course:
            res = spcall('insert_course', (course, ), commit=True)
            return jsonify({"status": "ok",
                            'message': 'course created successfully'})
        else:
            return jsonify({"status": "error", "message": "Course name is missing"})  # Handle missing course name
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# Get a specific course by ID
@app.route('/course/<int:course_id>', methods=['GET'])
def get_course(course_id):
    try:
        res = spcall('get_course_by_id', (course_id, ), commit=False)[0][0]
        return jsonify({"status": "ok",
                            'message': res})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Update a course by ID
@app.route('/course/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    try:
        data = request.get_json()
        course = data.get('course')
        print(course, course_id)
        
        if course:
            res = spcall('update_course_by_id', (course_id, course), commit=True)
            return jsonify({"status": "ok", 
                'message': 'course updated successfully'})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Delete a course by ID
@app.route('/course/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        res = spcall('delete_course_by_id', (course_id, ), commit=True)
        return jsonify({"status": "ok",
                        'message': 'course deleted successfully'})
    except:
        return {"status":"error", "message":str(sys.exc_info()[0]) +
                " " + str(sys.exc_info()[1])}



if __name__ == '__main__':
    app.run(debug=True)