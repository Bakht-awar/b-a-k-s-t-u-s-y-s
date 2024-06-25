import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

# Function to create the database and tables if they do not exist
def create_database_and_tables():
    try:
        conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", autocommit=True)
        curr = conn.cursor()

        # Create database if not exists
        curr.execute("CREATE DATABASE IF NOT EXISTS scss")
        curr.execute("USE scss")

        # Create student table
        curr.execute("""
            CREATE TABLE IF NOT EXISTS student (
                rollno INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                class VARCHAR(50) NOT NULL,
                section VARCHAR(10)
            )
        """)

        # Create records table
        curr.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                rollno INT,
                fathersnm VARCHAR(100),
                address VARCHAR(255),
                dob DATE,
                contact VARCHAR(15),
                gender VARCHAR(10),
                FOREIGN KEY (rollno) REFERENCES student(rollno)
            )
        """)

        conn.close()
    except pymysql.Error as e:
        print(f"An error occurred while creating database and tables: {e}")
        messagebox.showerror("Database Error", f"An error occurred while creating database and tables: {e}")

# Function to fetch students from the database
def fetch_students():
    try:
        conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="scss")
        curr = conn.cursor()
        curr.execute("SELECT * FROM student")
        rows = curr.fetchall()
        if len(rows) != 0:
            student_records_table.delete(*student_records_table.get_children())
            for row in rows:
                student_records_table.insert('', tk.END, values=row)
        conn.close()
    except pymysql.Error as e:
        print(f"An error occurred while fetching students: {e}")
        messagebox.showerror("Database Error", f"An error occurred while fetching students: {e}")

# Function to fetch records from the database
def fetch_records():
    try:
        conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="scss")
        curr = conn.cursor()
        curr.execute("SELECT rollno, fathersnm, address, dob, contact, gender FROM records")
        rows = curr.fetchall()
        if len(rows) != 0:
            general_records_table.delete(*general_records_table.get_children())
            for row in rows:
                general_records_table.insert('', tk.END, values=row)
        conn.close()
    except pymysql.Error as e:
        print(f"An error occurred while fetching records: {e}")
        messagebox.showerror("Database Error", f"An error occurred while fetching records: {e}")

# Function to add student and records to the database
def add_student():
    try:
        conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="scss")
        curr = conn.cursor()

        # Insert data into student table
        student_query = "INSERT INTO student (name, class, section) VALUES (%s, %s, %s)"
        curr.execute(student_query, (name_var.get(), class_var.get(), section_var.get()))

        # Get the last inserted rollno
        rollno = curr.lastrowid

        # Insert data into records table
        records_query = "INSERT INTO records (rollno, fathersnm, address, dob, contact, gender) VALUES (%s, %s, %s, %s, %s, %s)"
        curr.execute(records_query, (rollno, fathersnm_var.get(), address_var.get(), dob_var.get(), contact_var.get(), gender_var.get()))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student added successfully!")
        fetch_students()
        fetch_records()
        clear_fields()

    except pymysql.Error as e:
        print(f"An error occurred while adding student: {e}")
        messagebox.showerror("Database Error", f"An error occurred while adding student: {e}")

# Function to update student and records in the database
def update_student():
    try:
        # Get selected item in student_records_table
        selected_item = student_records_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to update.")
            return
        
        # Get rollno from selected item
        roll_number = student_records_table.item(selected_item, "values")[0]

        # Connect to database
        conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="scss")
        curr = conn.cursor()

        # Update data in student table
        curr.execute("UPDATE student SET name=%s, class=%s, section=%s WHERE rollno=%s",
                     (name_var.get(), class_var.get(), section_var.get(), roll_number))

        # Update data in records table
        curr.execute("UPDATE records SET fathersnm=%s, address=%s, dob=%s, contact=%s, gender=%s WHERE rollno=%s",
                     (fathersnm_var.get(), address_var.get(), dob_var.get(), contact_var.get(), gender_var.get(), roll_number))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student updated successfully!")
        fetch_students()
        fetch_records()
        clear_fields()

    except pymysql.Error as e:
        print(f"An error occurred while updating student: {e}")
        messagebox.showerror("Database Error", f"An error occurred while updating student: {e}")

# Function to delete student and records from the database
def delete_student():
    try:
        # Get selected item in student_records_table
        selected_item = student_records_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to delete.")
            return
        
        # Get rollno from selected item
        roll_number = student_records_table.item(selected_item, "values")[0]

        # Connect to database
        conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="scss")
        curr = conn.cursor()

        # Delete record from records table
        curr.execute("DELETE FROM records WHERE rollno=%s", (roll_number,))

        # Delete record from student table
        curr.execute("DELETE FROM student WHERE rollno=%s", (roll_number,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student deleted successfully!")
        fetch_students()
        fetch_records()
        clear_fields()

    except pymysql.Error as e:
        print(f"An error occurred while deleting student: {e}")
        messagebox.showerror("Database Error", f"An error occurred while deleting student: {e}")

# Function to search for students by roll number
def search_student():
    try:
        rollno_to_search = rollno_var.get()
        if not rollno_to_search:
            messagebox.showerror("Error", "Please enter a Roll No. to search.")
            return

        conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="scss")
        curr = conn.cursor()

        curr.execute("SELECT * FROM student WHERE rollno=%s", (rollno_to_search,))
        row = curr.fetchone()

        if row:
            name_var.set(row[1])
            class_var.set(row[2])
            section_var.set(row[3])

            # Fetch corresponding record from records table
            curr.execute("SELECT * FROM records WHERE rollno=%s", (rollno_to_search,))
            record = curr.fetchone()

            if record:
                fathersnm_var.set(record[1])
                address_var.set(record[2])
                dob_var.set(record[3])
                contact_var.set(record[4])
                gender_var.set(record[5])
        else:
            messagebox.showinfo("Not Found", f"No student found with Roll No. {rollno_to_search}")

        conn.close()

    except pymysql.Error as e:
        print(f"An error occurred while searching for student: {e}")
        messagebox.showerror("Database Error", f"An error occurred while searching for student: {e}")

# Function to show all students
def show_all_students():
    fetch_students()

# Function to clear entry fields
def clear_fields():
    rollno_var.set("")
    name_var.set("")
    class_var.set("")
    section_var.set("")
    fathersnm_var.set("")
    address_var.set("")
    dob_var.set("")
    contact_var.set("")
    gender_var.set("")

# Function to exit the application
def exit_application():
    win.destroy()

# GUI Setup
win = tk.Tk()
win.geometry("1350x700+0+0")
win.title("Student Management System")

# Labels and Entry Widgets
tk.Label(win, text="Student Management System", font=("Arial", 30, "bold"), border=12, bg="lightblue", relief=tk.GROOVE).pack(side=tk.TOP, fill=tk.X)

detail_frame = tk.LabelFrame(win, text="Enter Details", font=("Arial", 25), bg="lightblue", bd=12, relief=tk.GROOVE)
detail_frame.place(x=20, y=90, width=420, height=575)

# Entry variables
fields = ["Roll no", "Name", "Class", "Section", "Father's Name", "Address", "D.O.B", "Contact No", "Gender"]
variables = ["rollno_var", "name_var", "class_var", "section_var", "fathersnm_var", "address_var", "dob_var", "contact_var", "gender_var"]
globals().update({var: tk.StringVar() for var in variables})

# Entries and Combo Box
for i in range(0, len(fields)):
    tk.Label(detail_frame, text=fields[i], font=("Arial", 15), bg="lightblue").grid(row=i, column=0, padx=10, pady=10, sticky="w")
    if fields[i] == "Gender":
        gender_combo = ttk.Combobox(detail_frame, font=("Arial", 15), state="readonly", textvariable=globals()[variables[i]])
        gender_combo['values'] = ('Male', 'Female', 'Other')
        gender_combo.grid(row=i, column=1, padx=10, pady=10, sticky="w")
    else:
        ent = tk.Entry(detail_frame, font=("Arial", 15), bd=5, relief=tk.RIDGE, textvariable=globals()[variables[i]])
        ent.grid(row=i, column=1, padx=10, pady=10, sticky="w")
        ent.bind("<Tab>", lambda e, i=i+1: detail_frame.grid_slaves()[i].focus_set())

# Buttons Frame
btn_frame = tk.Frame(win, bg="lightblue", bd=12, relief=tk.GROOVE)
btn_frame.place(x=460, y=90, width=880, height=70)

# Buttons
buttons = [
    ("Add", lambda: add_student()),
    ("Update", lambda: update_student()),
    ("Delete", lambda: delete_student()),
    ("Clear", lambda: clear_fields()),
    ("Exit", lambda: exit_application()),
    ("Search", lambda: search_student()),
    ("Show All", lambda: show_all_students())
]

for btn_text, cmd in buttons:
    tk.Button(btn_frame, text=btn_text, font=("Arial", 15, "bold"), width=10, command=cmd).grid(row=0, column=buttons.index((btn_text, cmd)), padx=10, pady=10)

# Student Records Frame
records_frame = tk.LabelFrame(win, text="Student Records", font=("Arial", 25), bg="lightblue", bd=12, relief=tk.GROOVE)
records_frame.place(x=460, y=170, width=880, height=270)

# Scrollbar for student records table
scroll_y = tk.Scrollbar(records_frame, orient=tk.VERTICAL)
scroll_x = tk.Scrollbar(records_frame, orient=tk.HORIZONTAL)

# Treeview - Student Records Table
student_records_table = ttk.Treeview(records_frame, columns=("rollno", "name", "class", "section"),
                                     yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

# Configure scrollbar and pack student_records_table
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
scroll_y.config(command=student_records_table.yview)
scroll_x.config(command=student_records_table.xview)

student_records_table.heading("rollno", text="Roll No.")
student_records_table.heading("name", text="Name")
student_records_table.heading("class", text="Class")
student_records_table.heading("section", text="Section")
student_records_table['show'] = 'headings'

student_records_table.column("rollno", width=100)
student_records_table.column("name", width=150)
student_records_table.column("class", width=100)
student_records_table.column("section", width=100)

student_records_table.pack(fill=tk.BOTH, expand=1)

# General Records Frame
general_records_frame = tk.LabelFrame(win, text="General Records", font=("Arial", 25), bg="lightblue", bd=12, relief=tk.GROOVE)
general_records_frame.place(x=460, y=450, width=880, height=215)

# Treeview - General Records Table
general_records_table = ttk.Treeview(general_records_frame, columns=("rollno", "fathersnm", "address", "dob", "contact", "gender"),
                                     height=5, show="headings")

general_records_table.heading("rollno", text="Roll No.")
general_records_table.heading("fathersnm", text="Father's Name")
general_records_table.heading("address", text="Address")
general_records_table.heading("dob", text="D.O.B")
general_records_table.heading("contact", text="Contact No")
general_records_table.heading("gender", text="Gender")

general_records_table.column("rollno", width=100)
general_records_table.column("fathersnm", width=150)
general_records_table.column("address", width=250)
general_records_table.column("dob", width=100)
general_records_table.column("contact", width=120)
general_records_table.column("gender", width=80)

general_records_table.pack(fill=tk.BOTH, expand=1)

# Initialize database and tables if not exists
create_database_and_tables()

# Fetch existing students and records
fetch_students()
fetch_records()

win.mainloop()
