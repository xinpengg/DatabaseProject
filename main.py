import mysql.connector


def create_connection():
    return mysql.connector.connect(user='xinpengg',
                                   password='221199375',
                                   host='10.8.37.226',
                                   database='xinpengg_db')
def get_student_schedule(student_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = f"CALL GetStudentSchedule('{student_id}');"
    cursor.execute(query)

    for row in cursor:
        print("\n")
        print(f"Period: {row[1]}")
        print(f"Course: {row[0]}")
        print(f"Room: {row[2]}")
        print(f"Teacher: {row[3]}")

    cursor.close()
    connection.close()
def main():
    student_id = int(input("Enter a student ID: "))
    get_student_schedule(student_id)


if __name__ == "__main__":
    main()
