from tkinter import *
from tkinter import ttk
import tkmacosx as tkm
from tkinter import messagebox
from employees import connect_database


def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system;')
        cursor.execute('SELECT * from category_data;')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for row in records:
            treeview.insert('', END, values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Error due to {e}")
    finally:
        cursor.close()
        connection.close()


def add_category(id, name, description, treeview):
    if id == '' or name == '' or description == '':
        messagebox.showerror(title='Error', message='Please fill all fields')
        return
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            messagebox.showerror(title='Error', message='Database connection failed')
            return
        try:
            cursor.execute('use inventory_system;')
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS category_data (id INT PRIMARY KEY, name VARCHAR(100), description TEXT)")

            cursor.execute('SELECT * from category_data WHERE id=%s', id)
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id already exists')
                return

            cursor.execute("INSERT INTO category_data VALUES (%s, %s, %s)",
                           (id, name, description))
            connection.commit()
            messagebox.showinfo("Success", "Supplier added")
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror("Error", f"Error due to {e}")
        finally:
            cursor.close()
            connection.close()

def delete_category(treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror("Error", "You need to select a category.")
        return
    content = treeview.item(index)
    id = content['values'][0]

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("use inventory_system")
        cursor.execute("delete from category_data where id = %s", id)
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo("Success", "Record successfully deleted.")
    except Exception as e:
        messagebox.showerror("Error", f"Error due to {e}")
    finally:
        cursor.close()
        connection.close()

def clear(id_entry, category_name_entry, description_text):
    id_entry.delete(0, END)
    category_name_entry.delete(0, END)
    description_text.delete(1.0, END)


def category_form(window):
    global back_image, logo
    category_frame = Frame(window, width=1070, height=567, bg="white")
    category_frame.place(x=200, y=100)

    heading_label = Label(category_frame, text="Manage Category Details", font=("Helvetica", 16, "bold"), bg="#0f4d7d",
                          fg="white")
    heading_label.place(x=0, y=0, relwidth=1)
    back_image = PhotoImage(file="images/back_button.png")

    back_button = tkm.Button(category_frame, bg="white", image=back_image, bd=0, cursor="hand2", borderless=1,
                             command=lambda: category_frame.place_forget())
    back_button.place(x=10, y=30)

    logo = PhotoImage(file="images/categories.png")
    label = Label(category_frame, image=logo, bg="white")
    label.place(x=100, y=125)

    details_frame = Frame(category_frame, bg="white")
    details_frame.place(x=500, y=60)

    id_label = Label(details_frame, text='ID', font=('helvetica', 14, 'bold'), bg="white", fg="black")
    id_label.grid(row=0, column=0, padx=20, sticky='w')
    id_entry = Entry(details_frame, font=('helvetica', 14, 'bold'), bg="lightyellow", fg="black")
    id_entry.grid(row=0, column=1)

    category_name_label = Label(details_frame, text='Category Name', font=('helvetica', 14, 'bold'), bg="white",
                                fg="black")
    category_name_label.grid(row=1, column=0, padx=(20, 40), sticky='w')
    category_name_entry = Entry(details_frame, font=('helvetica', 14, 'bold'), bg="lightyellow", fg="black")
    category_name_entry.grid(row=1, column=1, pady=20)

    description_label = Label(details_frame, text='Description', font=('helvetica', 14, 'bold'), bg="white",
                              fg="black")
    description_label.grid(row=2, column=0, padx=(20, 40), sticky='nw')
    description_text = Text(details_frame, font=('helvetica', 14, 'bold'), bg="lightyellow", fg="black", height=6,
                            width=20, bd=2)
    description_text.grid(row=2, column=1)

    button_frame = Frame(category_frame, bg="white")
    button_frame.place(x=580, y=280)

    add_button = tkm.Button(button_frame, width=80, height=30, text='Add', font=("Helvetica", 14),
                            cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                            command=lambda: add_category(id_entry.get(), category_name_entry.get(),
                                                         description_text.get(1.0, END).strip(), treeview))
    add_button.grid(row=0, column=0, padx=20)

    delete_button = tkm.Button(button_frame, width=80, height=30, text='Delete', font=("Helvetica", 14),
                               cursor="hand2", fg="white", bg="#0f4d7d", borderless=1, command = lambda :delete_category(treeview))
    delete_button.grid(row=0, column=1, padx=20)

    clear_button = tkm.Button(button_frame, width=80, height=30, text='Clear', font=("Helvetica", 14),
                              cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                              command=lambda: clear(id_entry, category_name_entry, description_text))
    clear_button.grid(row=0, column=2, padx=20)

    treeview_frame = Frame(category_frame, bg="white")
    treeview_frame.place(x=500, y=340, height=200, width=500)

    horizontal_scrollbar = Scrollbar(treeview_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(treeview_frame, orient=VERTICAL)
    treeview = ttk.Treeview(treeview_frame, column=('id', 'name', 'description'), show='headings',
                            xscrollcommand=horizontal_scrollbar.set,
                            yscrollcommand=vertical_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)
    treeview.heading('name', text='Category Name')
    treeview.heading('id', text='ID')
    treeview.heading('description', text='Description')
    treeview.column('id', width=80)
    treeview.column('name', width=140)
    treeview.column('description', width=300)

    treeview_data(treeview)
    return category_frame