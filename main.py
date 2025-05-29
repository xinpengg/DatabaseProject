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
        print(row)
        # print(f"Assignment: {row[2]}")
        # print(f"Grade: {row[4]}")
        # print("-" * 40)

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
        print(f"Student Name: {row[1]}")
        print(f"Student Grade Assignment: {row[2]}")
        print("-" * 40)
    cursor.close()
    connection.close()
def add_assignment(name, assignment_type, course_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = f"CALL AddAssignment('{name}', {assignment_type}, {course_id});"
    cursor.execute(query)
    connection.commit()

    print(f"\nAssignment '{name}' added successfully!\n" + "-" * 30)

    cursor.close()
    connection.close()

def update_grade(student_id, course_id, assignment_id, grade):
    connection = create_connection()
    cursor = connection.cursor()

    query = f"CALL UpdateGrade({student_id}, {course_id}, {assignment_id}, '{grade}');"
    cursor.execute(query)
    connection.commit()

    print(f"\nGrade updated for Student {student_id}, Assignment {assignment_id}!\n" + "-" * 30)

    cursor.close()
    connection.close()


def main():
    print("Welcome! Please log in.")

    while True:
        user_type = input("Are you a Teacher or a Student? (Type 'exit' to quit) ").strip().lower()

        if user_type == "exit":
            print("Goodbye!")
            break

        if user_type not in ["teacher", "student"]:
            print("Invalid input. Please enter 'Teacher' or 'Student'.")
            continue

        user_id = input(f"Enter your {user_type.capitalize()} ID: ")
        get_schedule(user_type, user_id)

        if user_type == "student":
            course_id = int(input("Enter Course ID: "))
            get_assignment_grades(user_id, course_id)
            get_final_grade(user_id, course_id)
            get_total_average(user_id)

        elif user_type == "teacher":
            while True:
                print("\nTeacher Options:")
                print("1. View Assignments")
                print("2. Add an Assignment")
                print("3. Update a Grade")
                print("4. Exit")
                option = input("Select an option: ").strip()

                if option == "4":
                    print("Returning to main menu...")
                    break

                course_id = int(input("Enter Course ID: "))

                if option == "1":
                    assignments = get_course_assignments(course_id)
                    if assignments:
                        assignment_id = int(input("Enter Assignment ID to view student grades: "))
                        get_student_assignment_grades(course_id, assignment_id)

                elif option == "2":
                    assignment_name = input("Enter Assignment Name: ")
                    assignment_type = int(input("Enter Assignment Type ID (1 = Minor, 2 = Major): "))
                    add_assignment(assignment_name, assignment_type, course_id)

                elif option == "3":
                    student_id = int(input("Enter Student ID: "))
                    assignment_id = int(input("Enter Assignment ID: "))
                    grade = input("Enter New Grade: ")
                    update_grade(student_id, course_id, assignment_id, grade)

                else:
                    print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
