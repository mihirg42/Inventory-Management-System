from tkinter import *
from tkinter import ttk
import tkmacosx as tkm
from tkcalendar import DateEntry
import pymysql
from tkinter import messagebox


def connect_database():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="Boeing@#747")
        cursor = connection.cursor()
    except:
        messagebox.showerror("Error", "Database connectivity issue, open MySQL command line client")
        return None, None
    return cursor, connection


def create_database_table():
    cursor, connection = connect_database()
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
    cursor.execute('USE inventory_system')
    cursor.execute('''CREATE TABLE IF NOT EXISTS employee_data
    (
        empid
        INT
        PRIMARY
        KEY,
        name
        VARCHAR
                      (
        100
                      ),
        email VARCHAR
                      (
                          100
                      ),
        gender VARCHAR
                      (
                          50
                      ),
        dob VARCHAR
                      (
                          30
                      ),
        contact VARCHAR
                      (
                          30
                      ),
        employment_type VARCHAR
                      (
                          50
                      ),
        education VARCHAR
                      (
                          50
                      ),
        work_shift VARCHAR
                      (
                          50
                      ),
        address VARCHAR
                      (
                          100
                      ),
        doj VARCHAR
                      (
                          30
                      ),
        salary VARCHAR
                      (
                          50
                      ),
        usertype VARCHAR
                      (
                          50
                      ),
        password VARCHAR
                      (
                          50
                      ))''')


def treeview_data():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    try:
        cursor.execute("SELECT * FROM employee_data")
        employee_records = cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())
        for record in employee_records:
            employee_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror("Error", f"Error due to {e}")
    finally:
        cursor.close()
        connection.close()


def select_data(event, empid_entry, name_entry, email_entry,
                gender_combobox,
                dob_date_entry, contact_entry,
                employment_type_combobox,
                education_combobox, shift_combobox,
                address_text, doj_date_entry, salary_entry,
                usertype_combobox, password_entry):
    index = employee_treeview.selection()
    content = employee_treeview.item(index)
    row = content['values']
    clear_fields(empid_entry, name_entry, email_entry,
                 gender_combobox,
                 dob_date_entry, contact_entry,
                 employment_type_combobox,
                 education_combobox, shift_combobox,
                 address_text, doj_date_entry, salary_entry,
                 usertype_combobox, password_entry, False)
    empid_entry.insert(0, row[0])
    name_entry.insert(0, row[1])
    email_entry.insert(0, row[2])
    gender_combobox.set(row[3])
    dob_date_entry.set_date(row[4])
    contact_entry.insert(0, row[5])
    employment_type_combobox.set(row[6])
    education_combobox.set(row[7])
    shift_combobox.set(row[8])
    address_text.insert(1.0, row[9])
    doj_date_entry.set_date(row[10])
    salary_entry.insert(0, row[11])
    usertype_combobox.set(row[12])
    password_entry.insert(0, row[13])


def add_employee(empid, name, email, gender, dob, contact, employment_type,
                 education, work_shift, address, doj, salary, user_type, password):
    if (empid == '' or name == '' or email == '' or gender == 'Select Gender' or
            contact == '' or employment_type == 'Select type' or education == 'Select Education' or
            work_shift == 'Select Shift' or address.strip() == '' or salary == '' or
            user_type == 'Select User Type' or password == ''):
        messagebox.showerror("Error", "Please fill all fields")
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        try:
            address = address.strip()
            cursor.execute('''INSERT INTO employee_data
                              (empid, name, email, gender, dob, contact, employment_type, education,
                               work_shift, address, doj, salary, usertype, password)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                           (empid, name, email, gender, dob, contact, employment_type, education,
                            work_shift, address, doj, salary, user_type, password))

            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", "Employee added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to {e}")
        finally:
            cursor.close()
            connection.close()


def clear_fields(empid_entry, name_entry, email_entry,
                 gender_combobox,
                 dob_date_entry, contact_entry,
                 employment_type_combobox,
                 education_combobox, shift_combobox,
                 address_text, doj_date_entry, salary_entry, usertype_combobox, password_entry, check):
    empid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    gender_combobox.set("Select Gender")
    from datetime import date
    dob_date_entry.set_date(date.today())
    contact_entry.delete(0, END)
    employment_type_combobox.set("Select Type")
    education_combobox.set("Select Education")
    shift_combobox.set("Select Shift")
    address_text.delete(1.0, END)
    doj_date_entry.set_date(date.today())
    salary_entry.delete(0, END)
    usertype_combobox.set("Select User Type")
    password_entry.delete(0, END)
    if check:
        employee_treeview.selection_remove(employee_treeview.selection())


def update_employee(empid, name, email, gender, dob, contact, employment_type,
                    education, work_shift, address, doj, salary, user_type, password):
    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror("Error", "No row is selected")
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute('''SELECT *
                              FROM employee_data
                              WHERE empid = %s''', (empid,))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            address = address.strip()
            new_data = (name, email, gender, dob, contact, employment_type,
                        education, work_shift, address, doj, salary, user_type, password)
            if current_data == new_data:
                messagebox.showinfo("Information", "No changes detected")
                return
            cursor.execute(
                'UPDATE employee_data SET name=%s, email=%s, gender=%s, dob=%s, contact=%s, employment_type=%s,'
                'education=%s, work_shift=%s, address=%s, doj=%s, salary=%s, usertype=%s, password=%s WHERE empid=%s',
                (name, email, gender, dob, contact, employment_type,
                 education, work_shift, address, doj, salary, user_type, password, empid)
            )
            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", "Employee updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to {e}")
        finally:
            cursor.close()
            connection.close()


def delete_employee(empid, ):
    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror("Error", "No row is selected")
    else:
        result = messagebox.askyesno("Confirm", "Do you really want to delete the record?")
        if result:
            cursor, connection = connect_database()
            if not cursor or not connection:
                return
            try:
                cursor.execute('use inventory_system')
                cursor.execute('DELETE FROM employee_data WHERE empid = %s', (empid,))
                connection.commit()
                treeview_data()
                messagebox.showinfo("Success", "Employee deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Error due to {e}")
            finally:
                cursor.close()
                connection.close()


def search_employee(search_option, value):
    if search_option == "Search By":
        messagebox.showerror("Error", "No option is selected")
    elif value == '':
        messagebox.showerror("Error", "Enter the value to search")
    else:
        search_option = search_option.replace(" ", "_")
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute(f'SELECT * FROM employee_data WHERE {search_option} LIKE %s', f"%{value}%")
            records = cursor.fetchall()
            employee_treeview.delete(*employee_treeview.get_children())
            for record in records:
                employee_treeview.insert('', END, value=record)
        except Exception as e:
            messagebox.showerror("Error", f"Error due to {e}")
        finally:
            cursor.close()
            connection.close()


def show_all(search_entry, search_combobox):
    treeview_data()
    search_entry.delete(0, END)
    search_combobox.set('Search By')


def employee_form(window):
    global back_image, employee_treeview
    employee_frame = Frame(window, width=1070, height=567, bg="white")
    employee_frame.place(x=200, y=100)
    heading_label = Label(employee_frame, text="Manage Employee Details", font=("Helvetica", 16, "bold"), bg="#0f4d7d",
                          fg="white")
    heading_label.place(x=0, y=0, relwidth=1)
    back_image = PhotoImage(file="images/back_button.png")

    top_frame = Frame(employee_frame, bg="white")
    top_frame.place(x=0, y=40, relwidth=1, height=235)

    back_button = tkm.Button(top_frame, bg="white", image=back_image, bd=0, cursor="hand2", borderless=1,
                             command=lambda: employee_frame.place_forget())
    back_button.place(x=10, y=0)

    search_frame = Frame(top_frame, bg="white")
    search_frame.pack()

    search_combobox = ttk.Combobox(search_frame, values=('EmpId', 'Name', 'Email', 'Gender', 'Date of Birth', 'Contact',
                                                         'Employment Type', 'Education'
                                                             , 'Work Shift', 'Address', 'Date of Joining', 'Salary',
                                                         'User Type'), font=("Helvetica", 12),
                                   state='readonly')
    search_combobox.set("Search By")
    search_combobox.grid(row=0, column=0, padx=20)

    search_entry = Entry(search_frame, font=("Helvetica", 12), bg="lightyellow", fg = "black")
    search_entry.grid(row=0, column=1)

    search_button = tkm.Button(search_frame, width=100, height=30, text='Search', font=("Helvetica", 12),
                               cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                               command=lambda: search_employee(search_combobox.get(), search_entry.get()))
    search_button.grid(row=0, column=2, padx=20)

    show_button = tkm.Button(search_frame, text='Show All', width=100, height=30, font=("Helvetica", 12),
                             cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                             command=lambda: show_all(search_entry, search_combobox))
    show_button.grid(row=0, column=3)

    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)
    employee_treeview = ttk.Treeview(top_frame,
                                     columns=('empid', 'name', 'email', 'gender', 'dob', 'contact', 'employment_type',
                                              'education', 'work_shift',
                                              'address', 'doj', 'salary', 'usertype'), show='headings',
                                     xscrollcommand=horizontal_scrollbar.set,
                                     yscrollcommand=vertical_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar.config(command=employee_treeview.xview)
    vertical_scrollbar.config(command=employee_treeview.yview)
    employee_treeview.pack(pady=(10, 0))
    employee_treeview.heading('empid', text='EmpId')
    employee_treeview.heading('name', text='Name')
    employee_treeview.heading('email', text='Email')
    employee_treeview.heading('gender', text='Gender')
    employee_treeview.heading('dob', text='Date of Birth')
    employee_treeview.heading('contact', text='Contact')
    employee_treeview.heading('employment_type', text='Employment Type')
    employee_treeview.heading('education', text='Education')
    employee_treeview.heading('work_shift', text='Work Shift')
    employee_treeview.heading('address', text='Address')
    employee_treeview.heading('doj', text='Date of Joining')
    employee_treeview.heading('salary', text='Salary')
    employee_treeview.heading('usertype', text='User Type')
    employee_treeview.column('empid', width=80)
    employee_treeview.column('name', width=160)
    employee_treeview.column('email', width=200)
    employee_treeview.column('gender', width=80)
    employee_treeview.column('dob', width=120)
    employee_treeview.column('contact', width=120)
    employee_treeview.column('employment_type', width=120)
    employee_treeview.column('education', width=120)
    employee_treeview.column('work_shift', width=120)
    employee_treeview.column('address', width=300)
    employee_treeview.column('doj', width=120)
    employee_treeview.column('salary', width=120)
    employee_treeview.column('usertype', width=120)

    treeview_data()

    detail_frame = Frame(employee_frame, bg="white")
    detail_frame.place(x=70, y=295)

    empid_label = Label(detail_frame, text="EmpId", font=("Helvetica", 12), bg="white", fg="black")
    empid_label.grid(row=0, column=0, padx=20, pady=10)
    empid_entry = Entry(detail_frame, font=("Helvetica", 12), bg="lightyellow", fg = "black")
    empid_entry.grid(row=0, column=1, padx=20, pady=10)

    name_label = Label(detail_frame, text="Name", font=("Helvetica", 12), bg="white", fg="black")
    name_label.grid(row=0, column=2, padx=20, pady=10)
    name_entry = Entry(detail_frame, font=("Helvetica", 12), bg="lightyellow", fg = "black")
    name_entry.grid(row=0, column=3, padx=20, pady=10)

    email_label = Label(detail_frame, text="Email", font=("Helvetica", 12), bg="white", fg="black")
    email_label.grid(row=0, column=4, padx=20, pady=10)
    email_entry = Entry(detail_frame, font=("Helvetica", 12), bg="lightyellow", fg = "black")
    email_entry.grid(row=0, column=5, padx=20, pady=10)

    gender_label = Label(detail_frame, text="Gender", font=("Helvetica", 12), bg="white", fg="black")
    gender_label.grid(row=1, column=0, padx=20, pady=10)
    gender_combobox = ttk.Combobox(detail_frame, values=("Male", "Female", "Other"), font=("Helvetica", 12), width=18,
                                   state='readonly')
    gender_combobox.set("Select Gender")
    gender_combobox.grid(row=1, column=1, padx=20, pady=10)

    dob_label = Label(detail_frame, text="Date of Birth", font=("Helvetica", 12), bg="white", fg="black")
    dob_label.grid(row=1, column=2, padx=20, pady=10)
    dob_date_entry = DateEntry(detail_frame, width=18, font=("Helvetica", 12), date_pattern="dd/mm/yyyy")
    dob_date_entry.grid(row=1, column=3, padx=20, pady=10)

    contact_label = Label(detail_frame, text="Contact", font=("Helvetica", 12), bg="white", fg="black")
    contact_label.grid(row=1, column=4, padx=20, pady=10)
    contact_entry = Entry(detail_frame, font=("Helvetica", 12), bg="lightyellow", fg = "black")
    contact_entry.grid(row=1, column=5, padx=20, pady=10)

    employment_type_label = Label(detail_frame, text="Employment Type", font=("Helvetica", 12), bg="white", fg="black")
    employment_type_label.grid(row=2, column=0, padx=20, pady=10)
    employment_type_combobox = ttk.Combobox(detail_frame,
                                            values=("Full Time", "Part Time", "Casual", 'Contract', 'Intern'),
                                            font=("Helvetica", 12), width=18, state='readonly')
    employment_type_combobox.set("Select Type")
    employment_type_combobox.grid(row=2, column=1, padx=20, pady=10)

    education_label = Label(detail_frame, text="Education", font=("Helvetica", 12), bg="white", fg="black")
    education_label.grid(row=2, column=2, padx=20, pady=10)
    education_options = ["B.Tech", "B.Com", "M.Tech", "M.Com", "B.Sc", "M.Sc", "BBA", "MBA", "LLB", "LLM", "B.Arch",
                         "M.Arch"]
    education_combobox = ttk.Combobox(detail_frame,
                                      values=education_options,
                                      font=("Helvetica", 12), width=18, state='readonly')
    education_combobox.set("Select Education")
    education_combobox.grid(row=2, column=3, padx=20, pady=10)

    shift_label = Label(detail_frame, text="Work Shift", font=("Helvetica", 12), bg="white", fg="black")
    shift_label.grid(row=2, column=4, padx=20, pady=10)
    shift_combobox = ttk.Combobox(detail_frame, values=("Morning", "Evening", "Night"), font=("Helvetica", 12),
                                  width=18,
                                  state='readonly')
    shift_combobox.set("Select Work Shift")
    shift_combobox.grid(row=2, column=5, padx=20, pady=10)

    address_label = Label(detail_frame, text="Address", font=("Helvetica", 12), bg="white", fg="black")
    address_label.grid(row=3, column=0, padx=20, pady=10)
    address_text = Text(detail_frame, width=20, height=4, font=("Helvetica", 12), bg="lightyellow", fg = "black")
    address_text.grid(row=3, column=1, rowspan=2)

    doj_label = Label(detail_frame, text="Date of Joining", font=("Helvetica", 12), bg="white", fg="black")
    doj_label.grid(row=3, column=2, padx=20, pady=10)
    doj_date_entry = DateEntry(detail_frame, width=18, font=("Helvetica", 12), date_pattern="dd/mm/yyyy")
    doj_date_entry.grid(row=3, column=3, padx=20, pady=10)

    usertype_label = Label(detail_frame, text="User Type", font=("Helvetica", 12), bg="white", fg="black")
    usertype_label.grid(row=4, column=2, padx=20, pady=10)
    usertype_combobox = ttk.Combobox(detail_frame, values=("Admin", "Employee"), font=("Helvetica", 12),
                                     width=18,
                                     state='readonly')
    usertype_combobox.set("Select User Type")
    usertype_combobox.grid(row=4, column=3, padx=20, pady=10)

    salary_label = Label(detail_frame, text="Salary", font=("Helvetica", 12), bg="white", fg="black")
    salary_label.grid(row=3, column=4, padx=20, pady=10)
    salary_entry = Entry(detail_frame, font=("Helvetica", 12), bg="lightyellow", fg = "black")
    salary_entry.grid(row=3, column=5, padx=20, pady=10)

    password_label = Label(detail_frame, text="Password", font=("Helvetica", 12), bg="white", fg="black")
    password_label.grid(row=4, column=4, padx=20, pady=10)
    password_entry = Entry(detail_frame, font=("Helvetica", 12), bg="lightyellow", fg = "black")
    password_entry.grid(row=4, column=5, padx=20, pady=10)

    button_frame = Frame(employee_frame, bg="white")
    button_frame.place(x=200, y=525)

    add_button = tkm.Button(button_frame, width=100, height=30, text='Add', font=("Helvetica", 12),
                            cursor="hand2", fg="white", bg="#0f4d7d", borderless=1, command=lambda: add_employee(
            empid_entry.get(), name_entry.get(), email_entry.get(), gender_combobox.get(),
            dob_date_entry.get(), contact_entry.get(), employment_type_combobox.get(),
            education_combobox.get(), shift_combobox.get(), address_text.get(1.0, END),
            doj_date_entry.get(), salary_entry.get(), usertype_combobox.get(), password_entry.get()))
    add_button.grid(row=0, column=0, padx=20)

    update_button = tkm.Button(button_frame, width=100, height=30, text='Update', font=("Helvetica", 12),
                               cursor="hand2", fg="white", bg="#0f4d7d", borderless=1, command=lambda: update_employee(
            empid_entry.get(), name_entry.get(), email_entry.get(), gender_combobox.get(),
            dob_date_entry.get(), contact_entry.get(), employment_type_combobox.get(),
            education_combobox.get(), shift_combobox.get(), address_text.get(1.0, END),
            doj_date_entry.get(), salary_entry.get(), usertype_combobox.get(), password_entry.get()))
    update_button.grid(row=0, column=1, padx=20)

    delete_button = tkm.Button(button_frame, width=100, height=30, text='Delete', font=("Helvetica", 12),
                               cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                               command=lambda: delete_employee(empid_entry.get()))
    delete_button.grid(row=0, column=2, padx=20)

    clear_button = tkm.Button(button_frame, width=100, height=30, text='Clear', font=("Helvetica", 12),
                              cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                              command=lambda: clear_fields(empid_entry, name_entry, email_entry,
                                                           gender_combobox,
                                                           dob_date_entry, contact_entry,
                                                           employment_type_combobox,
                                                           education_combobox, shift_combobox,
                                                           address_text, doj_date_entry, salary_entry,
                                                           usertype_combobox, password_entry, True))
    clear_button.grid(row=0, column=3, padx=20)
    employee_treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, empid_entry, name_entry, email_entry,
                                                                          gender_combobox,
                                                                          dob_date_entry, contact_entry,
                                                                          employment_type_combobox,
                                                                          education_combobox, shift_combobox,
                                                                          address_text, doj_date_entry, salary_entry,
                                                                          usertype_combobox, password_entry))
    create_database_table()
    return employee_frame
