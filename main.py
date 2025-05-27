import mysql.connector


def create_connection():
    return mysql.connector.connect(user='xinpengg',
                                   password='221199375',
                                   host='10.8.37.226',
                                   database='xinpengg_db')


def get_final_grade(student_id, course_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = f"CALL CalculateFinalGrade({student_id}, {course_id});"
    cursor.execute(query)

    print("\nFinal Grade:\n" + "-" * 30)
    for row in cursor:
        print(f"Student ID: {row[0]}")
        print(f"Course ID: {row[1]}")
        print(f"Overall Grade: {round(row[2])}")
        print("-" * 30)

    cursor.close()
    connection.close()


def get_schedule(user_type, user_id):
    connection = create_connection()
    cursor = connection.cursor()

    if user_type.lower() == "teacher":
        query = f"CALL GetTeacherCourses({user_id});"
    else:
        query = f"CALL GetStudentSchedule({user_id});"
    cursor.execute(query)

    print("\nSchedule:\n" + "-" * 30)
    if user_type.lower() == "student":
        for row in cursor:
            print(f"Course ID: {row[0]}")
            print(f"Course: {row[1]}")
            print(f"Period: {row[2]}")
            print(f"Room: {row[3]}")
            print(f"Teacher: {row[4]}")
            print("-" * 30)

    else:
        for row in cursor:
            print(f"Course ID: {row[0]}")
            print(f"Course: {row[1]}")
            print(f"Period: {row[2]}")
            print("-" * 30)

    cursor.close()
    connection.close()


def get_assignment_grades(student_id, course_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = f"CALL GetAssignmentGrades({student_id}, {course_id});"
    cursor.execute(query)

    print("\nAssignment Grades:\n" + "-" * 40)
    for row in cursor:
        print(f"Assignment: {row[2]}")
        print(f"Grade: {row[4]}")
        print("-" * 40)

    cursor.close()
    connection.close()


def get_total_average(student_id):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        query = f"CALL CalculateTotalAverage({student_id});"
        cursor.execute(query)

        for row in cursor.fetchall():
            print(f"Student ID: {row[0]}")
            print(f"Weighted GPA: {round(row[1], 2)}")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")


def get_course_assignments(course_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = f"CALL GetCourseAssignments({course_id});"
    cursor.execute(query)

    assignments = []
    print("\nAssignments:\n" + "-" * 40)
    for row in cursor:
        print(f"Assignment ID: {row[0]}")
        print(f"Assignment Name: {row[1]}")
        print(f"Assignment Type: {row[2]}")
        print("-" * 40)
        assignments.append(row[0])

    cursor.close()
    connection.close()

    return assignments


def get_students_in_course(course_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = f"CALL GetStudentsInCourse({course_id});"
    cursor.execute(query)

    students = []
    print("\nStudents Enrolled:\n" + "-" * 40)
    for row in cursor:
        print(f"Student ID: {row[0]}")
        students.append(row[0])

    cursor.close()
    connection.close()

    return students


def get_student_assignment_grades(course_id, assignment_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = f"CALL GetStudentAssignmentGrades({course_id}, {assignment_id});"
    cursor.execute(query)

    print("\nStudent Assignment Grades:\n" + "-" * 40)
    for row in cursor:
        print(f"Student ID: {row[0]}")
        print(f"Grade: {row[1]}")
        print("-" * 40)

    cursor.close()
    connection.close()


def main():
    print("Welcome! Please log in.")
    user_type = input("Are you a Teacher or a Student? ").strip().lower()

    if user_type not in ["teacher", "student"]:
        print("Invalid input. Please restart and enter 'Teacher' or 'Student'.")
        return

    user_id = input(f"Enter your {user_type.capitalize()} ID: ")
    get_schedule(user_type, user_id)

    if user_type == "student":
        course_id = int(input("Enter Course ID: "))
        get_assignment_grades(user_id, course_id)
        get_final_grade(user_id, course_id)
        get_total_average(user_id)

    elif user_type == "teacher":
        course_id = int(input("Enter Course ID to view assignments: "))
        assignments = get_course_assignments(course_id)

        if assignments:
            assignment_id = int(input("Enter Assignment ID to view student grades: "))
            get_student_assignment_grades(course_id, assignment_id)


if __name__ == "__main__":
    main()
