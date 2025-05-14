import mysql.connector

def create_connection():
    return mysql.connector.connect(user='xinpengg',
                                   password='221199375',
                                   host='10.8.37.226',
                                   database='xinpengg_db')

def get_schedule(user_type, user_id):
    connection = create_connection()
    cursor = connection.cursor()

    if user_type.lower() == "teacher":
        query = f"CALL GetTeacherCourses({user_id});"
    else:
        query = f"CALL GetStudentSchedule({user_id});"

    cursor.execute(query)

    print("\nSchedule:\n" + "-"*30)
    if user_type.lower() == "student":
        for row in cursor:
            print(f"Period: {row[1]}")
            print(f"Course: {row[0]}")
            print(f"Room: {row[2]}")
            print(f"Teacher: {row[3]}")
            print("-" * 30)

    else:
        for row in cursor:
            print(f"Course: {row[0]}")
            print(f"Period: {row[1]}")
            print("-" * 30)

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

if __name__ == "__main__":
    main()
