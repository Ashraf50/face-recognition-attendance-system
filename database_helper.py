import sqlite3

# Function to create the database table if it doesn't exist
def create_table():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
            (student_id TEXT PRIMARY KEY, name TEXT)''')  # Specify student_id as the PRIMARY KEY
    conn.commit()
    conn.close()

# Function to insert student data into the database
def insert_student(new_name, student_id):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    
    # Check if the student ID already exists in the database
    c.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
    existing_student = c.fetchone()
    if existing_student:
        print("Student ID already exists in the database.")
        print("Student Name Updated")
        c.execute("UPDATE students SET name=? WHERE student_id=?", (new_name, student_id))
        conn.commit()
        conn.close()
        return
    
    # If the student ID doesn't exist, insert the student data into the database
    c.execute("INSERT INTO students (name, student_id) VALUES (?, ?)", (new_name, student_id))
    conn.commit()
    conn.close()

# Function to retrieve a student by ID from the database
def get_student_by_id(student_id):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
    student = c.fetchone()
    conn.close()
    return student

def get_Name_by_id(face_id):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    names = []

    # If face_id is a list, iterate over each ID
    if isinstance(face_id, list):
        for id in face_id:
            c.execute("SELECT name FROM students WHERE student_id=?", (id,))
            student = c.fetchone()
            if student:
                names.append(student[0])
    
    # If face_id is a single ID, execute the query directly
    else:
        c.execute("SELECT name FROM students WHERE student_id=?", (face_id,))
        student = c.fetchone()
        if student:
            names.append(student[0])

    conn.close()
    return names

def get_student_id_by_name(name):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()

    # Execute SQL query to retrieve student ID by name
    c.execute("SELECT student_id FROM students WHERE name=?", (name,))
    student = c.fetchone()  # Fetch the first result
    conn.close()

    if student:
        return student[0]  # Return the student ID
    else:
        return None  # Return None if student not found


def remove_all_students():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    
    # Execute SQL command to delete all rows from the students table
    c.execute("DELETE FROM students")
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

def get_all_students():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return students

# insert_student("Ali5","56524")
# print(get_student_by_id(56523))
# print (get_all_students())
# Example usage:

