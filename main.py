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
    row = cursor.fetchone()  # Fetch a single row
    if row:
        print(f"Grades for Student ID: {row[0]} and Course {row[1]}")
    for row in cursor:
        print(f"Assignment: {row[2]}")
        if (row[3] == 1):
            print("Minor Assessments")
        elif (row[3] == 2):
            print("Major Assessments")
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


def get_assignments_for_course(course_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = f"CALL GetAssignmentsForCourse({course_id});"
    cursor.execute(query)

    print("\nAssignments for Course ID:", course_id)
    print("-" * 40)
    for row in cursor:
        print(f"Assignment ID: {row[0]}")
        print(f"Assignment Name: {row[1]}")
        print("-" * 40)

    cursor.close()
    connection.close()

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


def add_student_to_class(student_id, course_period_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("CALL AddStudentToClass(%s, %s);", (student_id, course_period_id))
        connection.commit()
        print(f"Student {student_id} successfully added to Course {course_period_id}.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def remove_student_from_class(course_period_id, student_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("CALL RemoveStudentFromClass(%s, %s);", (course_period_id, student_id))
        connection.commit()
        print(f"Student {student_id} successfully removed from Course {course_period_id}.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


def create_new_class(period, teacher_id, room_id, course_id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(f"CALL CreateNewClass({period}, {teacher_id}, '{room_id}', {course_id});")
    message = cursor.fetchone()

    print("\nDatabase Response:\n" + "-" * 40)
    print(message[0])
    cursor.close()
    connection.close()
def get_available_teachers(period):
    connection = create_connection()
    cursor = connection.cursor()
    query_teachers = f"CALL GetAvailableTeachersForPeriod({period});"
    cursor.execute(query_teachers)
    teachers = cursor.fetchall()
    cursor.close()
    connection.close()
    return teachers

def get_available_rooms(period):
    connection = create_connection()
    cursor = connection.cursor()
    query_rooms = f"CALL GetAvailableRoomsForPeriod({period});"
    cursor.execute(query_rooms)
    rooms = cursor.fetchall()
    cursor.close()
    connection.close()
    return rooms

def show_courses():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("CALL ShowCourses();")
    courses = cursor.fetchall()
    print("\nAvailable Courses:\n" + "-" * 40)
    for course in courses:
        print(f"Course ID: {course[0]} | Course Name: {course[1]}")
    print("-" * 40)
    cursor.close()
    connection.close()
def main():
    print("Welcome! Please log in.")
    while True:
        user_type = input("Are you a Student, Teacher, or Administrator? (Type 'exit' to quit) ").strip().lower()

        if user_type == "exit":
            print("Goodbye!")
            break

        if user_type not in ["student", "teacher", "administrator"]:
            print("Invalid input. Please enter 'Student', 'Teacher', or 'Administrator'.")
            continue
        user_id = None
        if user_type in ["student", "teacher"]:
            user_id = input(f"Enter your {user_type.capitalize()} ID: ")

        if user_type == "student":
            while True:
                print("\nStudent Menu:")
                print("1. View Schedule")
                print("2. View Grades for a Class")
                print("3. View Final Grade")
                print("4. View Total Average")
                print("5. Exit")
                option = input("Select an option: ").strip()

                if option == "5":
                    print("Returning to main menu...")
                    break

                course_id = int(input("Enter Course ID: ")) if option in ["2", "3"] else None

                if option == "1":
                    get_schedule(user_type, user_id)
                elif option == "2":
                    get_assignment_grades(user_id, course_id)
                elif option == "3":
                    get_final_grade(user_id, course_id)
                elif option == "4":
                    get_total_average(user_id)
                else:
                    print("Invalid option. Try again.")

        elif user_type == "teacher":
            while True:
                print("\nTeacher Menu:")
                print("1. View Schedule")
                print("2. View Student Grades for Assignment")
                print("3. Add an Assignment")
                print("4. Update a Grade")
                print("5. Exit")
                option = input("Select an option: ").strip()

                if option == "5":
                    print("Returning to main menu...")
                    break
                get_schedule(user_type, user_id)
                course_id = int(input("Enter Course ID: ")) if option in ["2", "3", "4"] else None

                if option == "1":
                    get_schedule(user_type, user_id)
                elif option == "2":
                    get_assignments_for_course(course_id)
                    assignment_id = int(input("Enter Assignment ID: "))
                    get_student_assignment_grades(course_id, assignment_id)
                elif option == "3":
                    assignment_name = input("Enter Assignment Name: ")
                    assignment_type = int(input("Enter Assignment Type ID (1 = Minor, 2 = Major): "))
                    add_assignment(assignment_name, assignment_type, course_id)
                elif option == "4":
                    get_students_in_course(course_id)
                    student_id = int(input("Enter Student ID: "))
                    get_assignments_for_course(course_id)
                    assignment_id = int(input("Enter Assignment ID: "))
                    grade = input("Enter New Grade: ")
                    update_grade(student_id, course_id, assignment_id, grade)
                else:
                    print("Invalid option. Try again.")

        elif user_type == "administrator":
            while True:
                print("\nAdministrator Menu:")
                print("1. Add Student to Class")
                print("2. Remove Student from Class")
                print("3. Create New Class")
                print("4. Exit")
                option = input("Select an option: ").strip()
                if option == "4":
                    print("Returning to main menu...")
                    break

                if option == "1":
                    student_id = int(input("Enter Student ID: "))
                    course_period_id = int(input("Enter Course Period ID: "))
                    add_student_to_class(student_id, course_period_id)
                elif option == "2":
                    student_id = int(input("Enter Student ID: "))
                    course_period_id = int(input("Enter Course Period ID: "))
                    remove_student_from_class(course_period_id, student_id)
                elif option == "3":
                    period = int(input("Enter Period: "))
                    available_teachers = get_available_teachers(period)
                    available_rooms = get_available_rooms(period)
                    print("\nAvailable Teachers:\n" + "-" * 40)
                    for teacher in available_teachers:
                        print(f"Teacher ID: {teacher[0]} | Name: {teacher[1]}")
                    teacher_id = int(input("\nEnter Teacher ID from the list above: "))
                    print("\nAvailable Rooms:\n" + "-" * 40)
                    for room in available_rooms:
                        print(f"Room: {room[0]}")
                    print("-" * 40)
                    room_id = input("Enter Room ID from the list above: ")
                    show_courses()
                    course_id = int(input("Enter Course ID: "))
                    print("\nTeacher and Room are available. Creating the class...\n")
                    create_new_class(period, teacher_id, room_id, course_id)

if __name__ == "__main__":
    main()
