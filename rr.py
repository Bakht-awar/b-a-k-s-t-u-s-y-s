import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

win = tk.Tk()
win.geometry("1350x700+0+0")
win.title("Student Management System")

title_label = tk.Label(win, text="Student Management System", font=("Arial", 30, "bold"), border=12, bg="lightblue", relief=tk.GROOVE,)
title_label.pack(side=tk.TOP, fill=tk.X)


detail_frame = tk.LabelFrame(win, text="Enter Details", font=("Arial", 25), bg="lightblue", bd=12, relief=tk.GROOVE)
detail_frame.place(x=20, y=90, width=420, height=575)

data_frame = tk.Frame(win, bd=12, bg="lightblue", relief=tk.GROOVE)
data_frame.place(x=475, y=90, width=810, height=575)


#===============Variable==============#
 
rollno = tk.StringVar()
name = tk.StringVar()
class_var = tk.StringVar()
section = tk.StringVar()
contact = tk.StringVar()
fathersnm = tk.StringVar()
address = tk.StringVar()
gender = tk.StringVar()
dob = tk.StringVar()

search_by = tk.StringVar()
 

# Entry Widgets
entries = {}
fields = ["Roll no", "Name", "Class", "Section", "Contact", "Father's Name", "Address", "Gender", "D.O.B"]
string_vars = [rollno, name, class_var, section, contact, fathersnm, address, gender, dob]
for i, field, var in zip(range(len(fields)), fields, string_vars):
    label = tk.Label(detail_frame, text=field, font=("Arial", 15), bg="lightblue")
   
    label.grid(row=i, column=0, padx=2, pady=2)
    entry = tk.Entry(detail_frame, bd=7, font=("Arial", 15), textvariable=var)
    entry.grid(row=i, column=1, padx=2, pady=2)
    entries[field] = entry


gender_ent = ttk.Combobox(detail_frame, font=("Arial", 15), state="readonly", values=["Male", "Female", "Others"],
                           textvariable=gender)
gender_ent.grid(row=7, column=1, padx=2, pady=2)

#=============== Functions ============#

def fetch_students():
    
    conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="sms")

    curr = conn.cursor()
    curr.execute("SELECT * FROM student")
    rows = curr.fetchall()
    if len(rows) != 0:
        student_records_table.delete(*student_records_table.get_children())
        for row in rows:
            student_records_table.insert('', tk.END, values=row)
        conn.commit()
    conn.close()

def fetch_records():
    
    conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="sms")

    curr = conn.cursor()
    curr.execute("SELECT * FROM records")  # Assuming the table name is 'records'
    rows = curr.fetchall()
    if len(rows) != 0:
        general_records_table.delete(*general_records_table.get_children())
        for row in rows:
            general_records_table.insert('', tk.END, values=row)
        conn.commit()
    conn.close()
    
def add_futc():
       
    if not all([rollno.get(), name.get(), class_var.get()]):
        messagebox.showerror("Error!", "Please fill all the required fields!")
        return

try:
    # Establish database connection
    conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="sms")
    curr = conn.cursor()

    # Insert data into the student table
    
    student_query = "INSERT INTO student (`Roll no`, name, class, section) VALUES (%s, %s, %s, %s)"
    curr.execute(student_query, (rollno.get(), name.get(), class_var.get(), section.get()))
    
    # Insert data into the records table
    
    records_query = "INSERT INTO records (`Roll no`, fathersnm, address, dob, contact, gender) VALUES (%s, %s, %s, %s, %s, %s)"
    curr.execute(records_query, (rollno.get(), fathersnm.get(), address.get(), dob.get(), contact.get(), gender.get()))


    # Commit changes
    conn.commit()
    print("Changes committed successfully.")

    # Close database connection
    conn.close()
    print("Database connection closed.")

    # Refresh displayed data
    fetch_students()  # Refresh student records
    fetch_records()   # Refresh general records

    # Clear entry fields after adding
    clear_func()
    
    # Show success message
    messagebox.showinfo("Success!", "Data added successfully!")

except pymysql.Error as e:
    print("An error occurred:", e)
    messagebox.showerror("Error", f"An error occurred: {e}")



def get_cursor_records(event):
    
   
    cursor_row_records = general_records_table.focus()
    content_records = general_records_table.item(cursor_row_records)
    row_records = content_records.get("values")

    if row_records:  # Check if row_records is not empty
        if len(row_records) >= 6:  # Ensure row_records has at least 6 elements
            fathersnm.set(row_records[1])
            address.set(row_records[2])
            dob.set(row_records[3])
            gender.set(row_records[4])
            contact.set(row_records[5])
        else:
            messagebox.showerror("Error", "Incomplete record data.")
    else:
        messagebox.showerror("Error", "No record selected.")

def get_cursor(event):
    cursor_row = student_records_table.focus()
    content = student_records_table.item(cursor_row)
    row = content.get("values")

    if row:  # Check if row is not empty
        if len(row) >= 4:  # Ensure row has at least 4 elements
            rollno.set(row[0])
            name.set(row[1])
            class_var.set(row[2])
            section.set(row[3])
        else:
            messagebox.showerror("Error", "Incomplete record data.")
    else:
        messagebox.showerror("Error", "No record selected.")

   

        

def clear_func():
    #==this function will clear entry boxes==#
    rollno.set("")
    name.set("")
    class_var.set("")
    section.set("")
    fathersnm.set("")
    address.set("")
    dob.set("")
    contact.set("")
    gender.set("")
   

def update_func():  
   #=== this function will update data according to user====#
    
    try:
        # Establish database connection
        conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="sms")
        curr = conn.cursor()

        # Update data in the student table
        curr.execute("UPDATE student SET name=%s, class=%s, section=%s WHERE `Roll no`=%s",
                     (name.get(), class_var.get(), section.get(), rollno.get()))

        
        # Update data in the records table
        curr.execute("UPDATE records SET fathersnm=%s, address=%s, dob=%s, gender=%s, contact=%s WHERE `Roll no`=%s",
                     (fathersnm.get(), address.get(), dob.get(), gender.get(), contact.get(), rollno.get()))

        
        # Commit changes
        conn.commit()
        
        # Close database connection
        conn.close() 

        # Refresh displayed data
        fetch_students()
        fetch_records()
        clear_func()

        # Show success message
        messagebox.showinfo("Success!", "Data updated successfully!")
    except pymysql.Error as e:
        # Show error message if an error occurs
        messagebox.showerror("Error", f"An error occurred: {e}")

    
    
def delete_record():   
   
    # Get the selected row in the student records table
    selected_item = student_records_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to delete.")
        return

    # Get the roll number of the selected record
    roll_number = student_records_table.item(selected_item, "values")[0]

    try:
        # Connect to the database
        conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password=" ", database="sms")
        curr = conn.cursor()

        # Delete the record from the 'student' table
        curr.execute("DELETE FROM student WHERE rollno = %s", (roll_number,))

        # Delete the corresponding record from the 'records' table
        curr.execute("DELETE FROM records WHERE rollno = %s", (roll_number,))

        # Commit the changes
        conn.commit()

        # Refresh the student records table after deletion
        fetch_students()
        fetch_records()

        # Close the database connection
        conn.close()

        messagebox.showinfo("Success", "Record deleted successfully.")
    except pymysql.Error as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    

# Button Widgets
btn_frame = tk.Frame(detail_frame, bg="lightblue", bd=10, relief=tk.GROOVE)
btn_frame.place(x=18, y=390, width=340, height=120)

add_btn = tk.Button(btn_frame, text="Add", bd=7, font=("Arial", 13), width=15,command=add_futc, bg="white", fg="black")
add_btn.grid(row=0, column=0, padx=2, pady=2)

update_btn = tk.Button(btn_frame, text="Update", bd=7, font=("Arial", 13), width=15,command=update_func, bg="white", fg="black")
update_btn.grid(row=0, column=1, padx=3, pady=2)

delete_btn = tk.Button(btn_frame, text="Delete", bd=7, font=("Arial", 13), width=15, command=delete_record ,bg="white", fg="black")
delete_btn.grid(row=1, column=0, padx=2, pady=2, sticky='we')  # Add sticky parameter


clear_btn = tk.Button(btn_frame, text="Clear", bd=7, font=("Arial", 13), width=15,command=clear_func, bg="white", fg="black")
clear_btn.grid(row=1, column=1, padx=3, pady=2)


def search_records():
    # Get the selected search criteria
    selected_criteria = search_by.get()

    # Get the search keyword
    keyword = entries[selected_criteria].get()

    # Check if keyword is empty
    if not keyword:
        messagebox.showerror("Error", "Please enter a search keyword.")
        return

    # Establish database connection
    conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="sms")
    curr = conn.cursor()

    # Perform search in 'student' table
    student_query = f"SELECT * FROM student WHERE {selected_criteria} = %s"
    curr.execute(student_query, (keyword,))
    student_rows = curr.fetchall()

    # Perform search in 'records' table
    records_query = f"SELECT rollno, fathersnm, address, dob, contact, gender FROM records WHERE {selected_criteria} = %s"
    curr.execute(records_query, (keyword,))
    records_rows = curr.fetchall()

    # Clear existing data in the student records table
    student_records_table.delete(*student_records_table.get_children())
    general_records_table.delete(*general_records_table.get_children())

    # Insert the search results into the student records table
    for row in student_rows:
        student_records_table.insert('', tk.END, values=row)

    # Insert the search results into the general records table
    for row in records_rows:
        general_records_table.insert('', tk.END, values=row)

    # Commit changes and close the connection
    conn.commit()
    conn.close()




def show_all_records():
    # Refresh displayed data
    fetch_students()
    fetch_records()


# Search Widgets
search_frame = tk.Frame(data_frame, bg="lightblue", bd=10, relief=tk.GROOVE)
search_frame.pack(side=tk.TOP, fill=tk.X)

search_lbl = tk.Label(search_frame, text="Search", bg="lightblue", font=("Arial", 14))
search_lbl.grid(row=0, column=0, padx=12, pady=2)

search_in = ttk.Combobox(search_frame, font=("Arial", 14), state="readonly", textvariable=search_by, values=("Name", "Roll no", "Contact", "Father's Name", "Class", "Section", "D.O.B"))
search_in.grid(row=0, column=1, padx=12, pady=2)

search_btn = tk.Button(search_frame, text="Search", font=("Arial", 13), bd=9, width=14,command=search_records, bg="white", fg="black")
search_btn.grid(row=0, column=2, padx=12, pady=2)

showall_btn = tk.Button(search_frame, text="Show All", font=("Arial", 13), bd=9, width=14,command=show_all_records, bg="white", fg="black")
showall_btn.grid(row=0, column=3, padx=12, pady=2)

# Function to exit the program gracefully
def exit_program():
    win.destroy()

# Create an exit button
exit_button = tk.Button(win, text="Exit", command=exit_program)
exit_button.pack(side=tk.BOTTOM)


# Student Records Table
student_records_frame = tk.LabelFrame(data_frame, text="Student Records", font=("Arial", 15), bg= "lightblue", bd=12,
                                      relief=tk.GROOVE)

student_records_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

student_records_table = ttk.Treeview(student_records_frame,
                                      columns=("Roll No", "Name", "Class", "Section"),
                                      show="headings")

student_records_table.heading("Roll No", text="Roll No")
student_records_table.heading("Name", text="Name")
student_records_table.heading("Class", text="Class")
student_records_table.heading("Section", text="Section")

student_records_table.column("Roll No", width=100)
student_records_table.column("Name", width=200)
student_records_table.column("Class", width=100)
student_records_table.column("Section", width=100)

student_records_table.pack(fill=tk.BOTH, expand=True)





# General Records Table
general_records_frame = tk.LabelFrame(data_frame, text="General Records", font=("Arial", 15), bg="lightblue", bd=12,
                                      relief=tk.GROOVE)
general_records_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

general_records_table = ttk.Treeview(general_records_frame,
                                      columns=("Roll No", "Father's Name", "Address", "Date of Birth","Contact","Gender"),
                                      show="headings")

general_records_table.heading("Roll No", text="Roll No")
general_records_table.heading("Father's Name", text="Father's Name")
general_records_table.heading("Address", text="Address")
general_records_table.heading("Date of Birth", text="Date of Birth")
general_records_table.heading("Contact", text="Contact")
general_records_table.heading("Gender", text="Gender")


general_records_table.column("Roll No", width=100)
general_records_table.column("Father's Name", width=200)
general_records_table.column("Address", width=100)
general_records_table.column("Date of Birth", width=100)
general_records_table.column("Contact", width=100)
general_records_table.column("Gender", width=100)


general_records_table.pack(fill=tk.BOTH, expand=True)

fetch_students()
fetch_records()

student_records_table.bind("<Button-1>", get_cursor)
general_records_table.bind("<Button-1>", get_cursor_records)


win.mainloop()
