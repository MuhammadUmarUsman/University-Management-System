import tkinter as tk
import pymysql
from prettytable import PrettyTable


db = pymysql.connect(
    host="localhost",
    user="root",
    password="<your password>",
    database="<your db>"
)


cursor = db.cursor()


def style_button(button):
    button.config(
        bg="#0074D9", 
        fg="white",
        font=("Helvetica", 10),
        relief=tk.RAISED,  
        cursor="hand2",  
        padx=3,
        pady=3
    )

def authenticate(username, password):
   
    hardcoded_username = "admin"
    hardcoded_password = "password"

    if username == hardcoded_username and password == hardcoded_password:
        return True
    else:
        return False

def open_main_window():
    login_window.destroy()  
    main_window()


def login():
    username = username_entry.get()
    password = password_entry.get()

    if authenticate(username, password):
        login_window.destroy()
        main_window()
    else:
        error_label.config(text="Invalid credentials")


def main_window():
    window = tk.Tk()
    window.title("DASHBOARD")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    desired_width = screen_width
    desired_height = screen_height

    window.geometry(f"{desired_width}x{desired_height}")


    buttons_frame = tk.Frame(window)
    buttons_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nw")


    def show_students():
        cursor.execute("""
            SELECT s.student_id, s.student_name, s.cgpa, s.student_age, s.date_of_birth, p.prog_name, d.dep_name
            FROM Students s
            INNER JOIN Programs p ON s.program_id = p.program_id
            INNER JOIN Departments d ON p.department_id = d.department_id
        """)
        result = cursor.fetchall()
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)

        table = PrettyTable()
        table.field_names = ["Student ID", "Name", "CGPA", "Age", "Date of Birth", "Program", "Department"]

        for row in result:
            table.add_row(row)

        result_text.insert(tk.END, str(table))
        result_text.config(state=tk.DISABLED)


    def add_student():
        top = tk.Toplevel(window)
        top.title("Add New Student")
        top_width = 400
        top_height = 400
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_position = (screen_width - top_width) // 2
        y_position = (screen_height - top_height) // 2
        top.geometry(f"{top_width}x{top_height}+{x_position}+{y_position}")

        name_label = tk.Label(top, text="Name:")
        name_entry = tk.Entry(top)
        gpa_label = tk.Label(top, text="GPA:")
        gpa_entry = tk.Entry(top)
        age_label = tk.Label(top, text="Age:")
        age_entry = tk.Entry(top)
        dob_label = tk.Label(top, text="Date of Birth:")
        dob_entry = tk.Entry(top)
        program_label = tk.Label(top, text="Program id:")
        program_entry = tk.Entry(top)

        def add_student_to_db():
            student_name = name_entry.get()
            student_gpa = gpa_entry.get()
            student_age = age_entry.get()
            student_dob = dob_entry.get()
            program_name = program_entry.get()

            try:
                sql_call_procedure = "CALL AddStudent(%s, %s, %s, %s, %s)"
                values = (student_name, student_gpa, student_age, student_dob, program_name)
                cursor.execute(sql_call_procedure, values)
                db.commit()
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "Student added successfully!\n")
            except pymysql.err.OperationalError as e:
                error_message = str(e).split(",")[1]
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, error_message + '\n')
            finally:
                result_text.config(state=tk.DISABLED)
                top.destroy()

        add_button = tk.Button(top, text="Add Student", command=add_student_to_db)

        name_label.pack()
        name_entry.pack()
        gpa_label.pack()
        gpa_entry.pack()
        age_label.pack()
        age_entry.pack()
        dob_label.pack()
        dob_entry.pack()
        program_label.pack()
        program_entry.pack()
        add_button.pack(pady=10)


    def delete_student():
        top = tk.Toplevel(window)
        top.title("Delete Student")
        top_width = 400 
        top_height = 100  
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_position = (screen_width - top_width) // 2
        y_position = (screen_height - top_height) // 2
        top.geometry(f"{top_width}x{top_height}+{x_position}+{y_position}")

        id_label = tk.Label(top, text="Student ID:")
        id_entry = tk.Entry(top)

        def delete_student_from_db():
            student_id = id_entry.get()

            sql_delete_student = """
            DELETE FROM students
            WHERE student_id = %s
            """

            values = (student_id,)

            cursor.execute(sql_delete_student, values)
            db.commit()

            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Student deleted successfully!\n")
            result_text.config(state=tk.DISABLED)

            top.destroy()

        delete_button = tk.Button(top, text="Delete Student", command=delete_student_from_db)

        id_label.pack()
        id_entry.pack()
        delete_button.pack(pady=10)
    
    def update_student():
        top = tk.Toplevel(window)
        top.title("Update Student")
        top_width = 400 
        top_height = 170  
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_position = (screen_width - top_width) // 2
        y_position = (screen_height - top_height) // 2
        top.geometry(f"{top_width}x{top_height}+{x_position}+{y_position}")

        id_label = tk.Label(top, text="Student ID:")
        id_entry = tk.Entry(top)
        name_label = tk.Label(top, text="New Name:")
        name_entry = tk.Entry(top)
        gpa_label = tk.Label(top, text="New GPA:")
        gpa_entry = tk.Entry(top)

        def update_student_in_db():
            student_id = id_entry.get()
            new_name = name_entry.get()
            new_gpa = gpa_entry.get()

            sql_update_student = """
            UPDATE students
            SET student_name = %s, cgpa = %s
            WHERE student_id = %s
            """

            values = (new_name, new_gpa, student_id)

            cursor.execute(sql_update_student, values)
            db.commit()

            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Student updated successfully!\n")
            result_text.config(state=tk.DISABLED)

            top.destroy()

        update_button = tk.Button(top, text="Update Student", command=update_student_in_db)

        id_label.pack()
        id_entry.pack()
        name_label.pack()
        name_entry.pack()
        gpa_label.pack()
        gpa_entry.pack()
        update_button.pack(pady=10)

    def show_department():
        top = tk.Toplevel(window)
        top.title("Show Department")
        top_width = 400 
        top_height = 100  
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_position = (screen_width - top_width) // 2
        y_position = (screen_height - top_height) // 2
        top.geometry(f"{top_width}x{top_height}+{x_position}+{y_position}")

        id_label = tk.Label(top, text="Student ID:")
        id_entry = tk.Entry(top)

        def show_department_for_student():
            student_id = id_entry.get()

            sql_select_department = """
            SELECT s.student_name, d.dep_name
            FROM students as s
            INNER JOIN Programs as p
            ON s.program_id = p.program_id
            INNER JOIN Departments as d
            ON p.department_id = d.department_id
            WHERE s.student_id = %s
            """

            cursor.execute(sql_select_department, (student_id,))
            result = cursor.fetchone()

            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)

            if result:
                table_data = [["Student Name", "Department"]]
                table_data.append([result[0], result[1]])

                table = PrettyTable()
                table.field_names = table_data[0]
                table.add_row(table_data[1])

                result_text.insert(tk.END, str(table))
            else:
                result_text.insert(tk.END, f"Student with ID {student_id} not found.")

            result_text.config(state=tk.DISABLED)
            top.destroy()


        show_button = tk.Button(top, text="Show Department", command=show_department_for_student)

        id_label.pack()
        id_entry.pack()
        show_button.pack(pady=10)

    def run_custom_query():
        top = tk.Toplevel(window)
        top.title("Custom Query")
        top_width = 400 
        top_height = 100  
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_position = (screen_width - top_width) // 2
        y_position = (screen_height - top_height) // 2
        top.geometry(f"{top_width}x{top_height}+{x_position}+{y_position}")


        query_label = tk.Label(top, text="Enter your SQL query:")
        query_entry = tk.Entry(top, width=50)

        def execute_query():
            query = query_entry.get()
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)

                if result:
                    columns = [desc[0] for desc in cursor.description]
                    table = PrettyTable(columns)

                    for row in result:
                        table.add_row(row)

                    result_text.insert(tk.END, str(table))
                else:
                    result_text.insert(tk.END, "No results found.")

                result_text.config(state=tk.DISABLED)
            except Exception as e:
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "An error occurred: " + str(e))
                result_text.config(state=tk.DISABLED)

            top.destroy()


        execute_button = tk.Button(top, text="Execute Query", command=execute_query)

        query_label.pack(pady=5)
        query_entry.pack(pady=5)
        execute_button.pack(pady=5)

    def show_faculty_teaching_students():
        top = tk.Toplevel(window)
        top.title("Faculty Teaching Students")
        top_width = 400 
        top_height = 100  
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_position = (screen_width - top_width) // 2
        y_position = (screen_height - top_height) // 2
        top.geometry(f"{top_width}x{top_height}+{x_position}+{y_position}")

        faculty_label = tk.Label(top, text="Enter Faculty ID:")
        faculty_entry = tk.Entry(top)


        def display_faculty_students():
            faculty_id = faculty_entry.get()
            try:
                sql_query = """
                SELECT s.student_name AS Student,
            c.course_name AS Course,
            f.faculty_name AS Faculty
            FROM Takes_Course AS tc
            INNER JOIN Students s 
            ON tc.student_id = s.student_id
            INNER JOIN Courses c 
            ON tc.course_id = c.course_id
            INNER JOIN Teaches_Course AS t 
            ON tc.course_id = t.course_id
            INNER JOIN Faculty AS f 
            ON t.faculty_id = f.faculty_id
            WHERE t.faculty_id = %s;
                """
                cursor.execute(sql_query, (faculty_id))
                result = cursor.fetchall()
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)

                if result:
                    table_data = [["Student", "Course","Faculty"]]  
                    for row in result:
                        table_data.append([row[0], row[1],row[2]]) 

                    table = PrettyTable()
                    table.field_names = table_data[0]
                    for row in table_data[1:]:
                        table.add_row(row)

                    result_text.insert(tk.END, str(table))
                else:
                    result_text.insert(tk.END, "No students found for the given faculty ID.")

                result_text.config(state=tk.DISABLED)
            except Exception as e:
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "An error occurred: " + str(e))
                result_text.config(state=tk.DISABLED)

            top.destroy()


        display_button = tk.Button(top, text="Show Students", command=display_faculty_students)
        faculty_label.pack(pady=5)
        faculty_entry.pack(pady=5)
        display_button.pack(pady=5)

    def show_students_taking_course():
        top = tk.Toplevel(window)
        top.title("Students Taking Course")
        top_width = 400
        top_height = 100
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_position = (screen_width - top_width) // 2
        y_position = (screen_height - top_height) // 2
        top.geometry(f"{top_width}x{top_height}+{x_position}+{y_position}")

        course_id_label = tk.Label(top, text="Course ID:")
        course_id_entry = tk.Entry(top)

        def display_students_taking_course():
            course_id = course_id_entry.get()
            try:
                sql_query = """
            SELECT s.student_name, c.course_name
            FROM Students s
            INNER JOIN Takes_Course tc ON s.student_id = tc.student_id
            INNER JOIN Courses c ON tc.course_id = c.course_id
            WHERE c.course_id = %s
            """
                cursor.execute(sql_query, (course_id,))
                result = cursor.fetchall()
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)

                if result:
                    table_data = [["Student Name", "Course"]]
                    for row in result:
                        table_data.append([row[0], row[1]])

                    table = PrettyTable()
                    table.field_names = table_data[0]
                    for row in table_data[1:]:
                        table.add_row(row)

                    result_text.insert(tk.END, str(table))
                else:
                    result_text.insert(tk.END, f"No students found for the given course ID.")

                result_text.config(state=tk.DISABLED)
            except Exception as e:
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "An error occurred: " + str(e))
                result_text.config(state=tk.DISABLED)

            top.destroy()

        display_button = tk.Button(top, text="Show Students Taking Course", command=display_students_taking_course)
        course_id_label.pack(pady=5)
        course_id_entry.pack(pady=5)
        display_button.pack(pady=5)

    def enroll_student():
        top = tk.Toplevel(window)
        top.title("Enroll Student")
        top_width = 400 
        top_height = 150  
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_position = (screen_width - top_width) // 2
        y_position = (screen_height - top_height) // 2
        top.geometry(f"{top_width}x{top_height}+{x_position}+{y_position}")

        student_id_label = tk.Label(top, text="Student ID:")
        student_id_entry = tk.Entry(top)
        course_id_label = tk.Label(top, text="Course ID:")
        course_id_entry = tk.Entry(top)

        def enroll_student_in_course():
            student_id = student_id_entry.get()
            course_id = course_id_entry.get()

            try:
           
                sql_check_enrollment = "SELECT * FROM Takes_Course WHERE student_id = %s AND course_id = %s"
                values = (student_id, course_id)
                cursor.execute(sql_check_enrollment, values)
                already_enrolled = cursor.fetchone()

                if already_enrolled:
                    result_text.config(state=tk.NORMAL)
                    result_text.delete("1.0", tk.END)
                    result_text.insert(tk.END, "Student is already enrolled in the course.\n")
                else:
                    sql_insert_enrollment = "INSERT INTO Takes_Course (student_id, course_id) VALUES (%s, %s)"
                    cursor.execute(sql_insert_enrollment, values)
                    db.commit()
                    result_text.config(state=tk.NORMAL)
                    result_text.delete("1.0", tk.END)
                    result_text.insert(tk.END, "Student enrolled successfully!\n")

           
                sql_get_student_and_course = """
                SELECT s.student_name, c.course_name
                FROM Students s
                INNER JOIN Courses c ON s.student_id = %s AND c.course_id = %s
                """
                cursor.execute(sql_get_student_and_course, values)
                enrollment_info = cursor.fetchone()
                if enrollment_info:
                    result_text.insert(tk.END, f"Student: {enrollment_info[0]}, Enrolled in: {enrollment_info[1]}\n")
            except Exception as e:
                error_message = str(e).split(",")[1]
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, error_message + '\n')
            finally:
                result_text.config(state=tk.DISABLED)
                top.destroy()

        enroll_button = tk.Button(top, text="Enroll Student", command=enroll_student_in_course)

        student_id_label.pack()
        student_id_entry.pack()
        course_id_label.pack()
        course_id_entry.pack()
        enroll_button.pack(pady=10)


    def get_high_scorers():
        try:
            sql_query = """
        SELECT 
            d.dep_name AS 'Department',
            s.student_name AS 'Student Name',
            s.cgpa AS 'CGPA'
            FROM Students s
            INNER JOIN Programs p ON s.program_id = p.program_id
            INNER JOIN Departments d ON p.department_id = d.department_id
            WHERE (s.cgpa, p.department_id) IN (
                SELECT MAX(s.cgpa), p.department_id
                FROM Students s
                INNER JOIN Programs p ON s.program_id = p.program_id
                GROUP BY p.department_id
            );
            """
            cursor.execute(sql_query)
            result = cursor.fetchall()

            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)

            if result:
                table = PrettyTable(["Department", "Student Name", "CGPA"])  
                for row in result[1:]:
                    table.add_row(row)
                result_text.insert(tk.END, str(table))
            else:
                result_text.insert(tk.END, "No high scorers found.")

        except Exception as e:
            error_message = str(e).split(",")[1]
            result_text.insert(tk.END, error_message + '\n')
        finally:
            result_text.config(state=tk.DISABLED)

    
    def show_student_courses():
        top = tk.Toplevel(window)
        top.title("Show Student Courses")
        top_width = 400 
        top_height = 150  
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_position = (screen_width - top_width) // 2
        y_position = (screen_height - top_height) // 2
        top.geometry(f"{top_width}x{top_height}+{x_position}+{y_position}")

        student_id_label = tk.Label(top, text="Student ID:")
        student_id_entry = tk.Entry(top)

        def display_student_courses():
            student_id = student_id_entry.get()
            try:
                sql_query = """
            SELECT s.student_name, c.course_name
            FROM Students s
            INNER JOIN Takes_Course tc ON s.student_id = tc.student_id
            INNER JOIN Courses c ON tc.course_id = c.course_id
            WHERE s.student_id = %s
            """
                cursor.execute(sql_query, (student_id))
                result = cursor.fetchall()
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)

                if result:
                    table = PrettyTable(["Student Name", "Enrolled Course"])
                    student_name = result[0][0]
                    for row in result:
                        table.add_row([student_name, row[1]])
                    result_text.insert(tk.END, str(table))
                else:
                    result_text.insert(tk.END, f"No student found with the given ID.")

                result_text.config(state=tk.DISABLED)

            except Exception as e:
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "An error occurred: " + str(e))
                result_text.config(state=tk.DISABLED)

            top.destroy()

        display_button = tk.Button(top, text="Show Student Courses", command=display_student_courses)
        student_id_label.pack(pady=5)
        student_id_entry.pack(pady=5)
        display_button.pack(pady=5)

    def show_student_fees():
        top = tk.Toplevel(window)
        top.title("Student Fees")
        top_width = 400 
        top_height = 100  
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_position = (screen_width - top_width) // 2
        y_position = (screen_height - top_height) // 2
        top.geometry(f"{top_width}x{top_height}+{x_position}+{y_position}")

        id_label = tk.Label(top, text="Student ID:")
        id_entry = tk.Entry(top)

        def display_student_fees():
            student_id = id_entry.get()
            try:
                sql_query = """
                SELECT s.student_name AS Student,
                f.amount AS Fee
                FROM Students s
                INNER JOIN fee_bill f
                ON s.student_id = f.student_id
                WHERE s.student_id = %s
                """
                cursor.execute(sql_query, (student_id))
                result = cursor.fetchall()
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)

                if result:
                    table_data = [["Student", "Fee"]]
                    for row in result:
                        table_data.append([row[0], row[1]])

                    table = PrettyTable()
                    table.field_names = table_data[0]
                    for row in table_data[1:]:
                        table.add_row(row)

                    result_text.insert(tk.END, str(table))
                else:
                    result_text.insert(tk.END, "No fees found for the given student ID.")

                result_text.config(state=tk.DISABLED)
            except Exception as e:
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "An error occurred: " + str(e))
                result_text.config(state=tk.DISABLED)

            top.destroy()

        display_button = tk.Button(top, text="Show Fees", command=display_student_fees)
        id_label.pack(pady=5)
        id_entry.pack(pady=5)
        display_button.pack(pady=5)
        
    def make_payment():
        top = tk.Toplevel(window)
        top.title("Make Payment")
        top_width = 400
        top_height = 200
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_position = (screen_width - top_width) // 2
        y_position = (screen_height - top_height) // 2
        top.geometry(f"{top_width}x{top_height}+{x_position}+{y_position}")

        student_id_label = tk.Label(top, text="Student ID:")
        student_id_entry = tk.Entry(top)
        payment_amount_label = tk.Label(top, text="Payment Amount:")
        payment_amount_entry = tk.Entry(top)

        def process_payment():
            student_id = student_id_entry.get()
            payment_amount = payment_amount_entry.get()

            try:
                sql_call_procedure = "CALL MakePayment(%s, %s)"
                values = (student_id, payment_amount)
                cursor.execute(sql_call_procedure, values)
                db.commit()

                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "Payment processed successfully!\n")
            except pymysql.err.OperationalError as e:
                error_message = str(e).split(",")[1]
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, error_message + '\n')
            finally:
                result_text.config(state=tk.DISABLED)
                top.destroy()

        make_payment_button = tk.Button(top, text="Make Payment", command=process_payment)

        student_id_label.pack()
        student_id_entry.pack()
        payment_amount_label.pack()
        payment_amount_entry.pack()
        make_payment_button.pack(pady=10)

    
    def clear_result_window():
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        welcome_message = "Welcome to University Management System Dashboard\n\n"
        result_text.tag_configure("center", justify="center")
        result_text.tag_configure("big", font=("Helvetica", 20))
        result_text.insert("1.0", welcome_message, ("center", "big"))
        result_text.config(state=tk.DISABLED)
   
    show_students_button = tk.Button(buttons_frame, text="Show All Students", command=show_students)
    add_student_button = tk.Button(buttons_frame, text="Add New Student", command=add_student)
    delete_student_button = tk.Button(buttons_frame, text="Delete Student", command=delete_student)
    update_student_button = tk.Button(buttons_frame, text="Update Student", command=update_student)
    show_faculty_students_button = tk.Button(buttons_frame, text="Show Faculty Teaching Students", command=show_faculty_teaching_students)
    show_students_taking_course_button = tk.Button(buttons_frame, text="Course Taken By Students", command=show_students_taking_course)
    show_department_button = tk.Button(buttons_frame, text="Show Department", command=show_department)
    enroll_student_button = tk.Button(buttons_frame, text="Enroll Student", command=enroll_student)
    show_student_courses_button = tk.Button(buttons_frame, text="Show Student Courses", command=show_student_courses)
    show_student_fees_button = tk.Button(buttons_frame, text="Show Student Fees", command=show_student_fees)
    make_payment_button = tk.Button(buttons_frame, text="Make Payment", command=make_payment)
    get_high_scorers_button = tk.Button(buttons_frame, text="Get High Scorers", command=get_high_scorers)
    custom_query_button = tk.Button(buttons_frame, text="Run Custom Query", command=run_custom_query)
    clear_button = tk.Button(buttons_frame, text="Clear", command=clear_result_window,bg="#f39c12", fg="black",font=("Helvetica", 10),relief=tk.RAISED, cursor="hand2", padx=3,pady=3)
    exit_button = tk.Button(buttons_frame, text="Exit", command=window.quit,bg="#e74c3c", fg="black",font=("Helvetica", 10),relief=tk.RAISED, cursor="hand2", padx=3,pady=3)


   
    result_text = tk.Text(window, height=40, width=130)
    result_text.config(state=tk.NORMAL)
    welcome_message = "Welcome to University Management System Dashboard\n\n"
    result_text.tag_configure("center", justify="center")
    result_text.tag_configure("big", font=("Helvetica", 20))
    result_text.insert("1.0", welcome_message, ("center", "big"))
    result_text.config(state=tk.DISABLED)
    result_text.grid(row=0, column=1, padx=20, pady=20, sticky="ne")


    show_students_button.grid(row=0, column=0, pady=5, sticky="w")
    add_student_button.grid(row=1, column=0, pady=5, sticky="w")
    delete_student_button.grid(row=2, column=0, pady=5, sticky="w")
    update_student_button.grid(row=3, column=0, pady=5, sticky="w")
    show_faculty_students_button.grid(row=4, column=0, pady=5, sticky="w")
    show_department_button.grid(row=5, column=0, pady=5, sticky="w")
    show_student_fees_button.grid(row=6, column=0, pady=5, sticky="w")
    enroll_student_button.grid(row=7, column=0, pady=5, sticky="w")
    show_student_courses_button.grid(row=8, column=0, pady=5, sticky="w")
    show_students_taking_course_button.grid(row=9, column=0, pady=5, sticky="w")
    make_payment_button.grid(row=10, column=0, pady=5, sticky="w")
    get_high_scorers_button.grid(row=11, column=0, pady=5, sticky="w")
    custom_query_button.grid(row=12, column=0, pady=5, sticky="w")
    clear_button.grid(row=13, column=0, pady=5, sticky="w")
    exit_button.grid(row=14, column=0, pady=5, sticky="w")
 
    style_button(show_students_button)
    style_button(add_student_button)
    style_button(delete_student_button)
    style_button(update_student_button)
    style_button(show_department_button)
    style_button(show_faculty_students_button)
    style_button(enroll_student_button)
    style_button(show_student_courses_button)
    style_button(show_student_fees_button)
    style_button(show_students_taking_course_button)
    style_button(custom_query_button)
    style_button(make_payment_button)
    style_button(get_high_scorers_button)
    
    window.mainloop()


login_window = tk.Tk()
login_window.title("University Management System Login")
login_window.geometry("500x200")

username_label = tk.Label(login_window, text="Username:")
username_entry = tk.Entry(login_window)
password_label = tk.Label(login_window, text="Password:")
password_entry = tk.Entry(login_window, show="*")  
login_button = tk.Button(login_window, text="Login", command=login)
error_label = tk.Label(login_window, text="", fg="red")


username_label.pack(pady=5, padx=10)
username_entry.pack(pady=5, padx=10)
password_label.pack(pady=5, padx=10)
password_entry.pack(pady=5, padx=10)
login_button.pack(pady=5, padx=10)
error_label.pack(padx=10)

style_button(login_button)

login_window.mainloop()
