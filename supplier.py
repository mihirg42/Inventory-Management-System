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
        cursor.execute('SELECT * from supplier_data;')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for row in records:
            treeview.insert('', END, values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Error due to {e}")
    finally:
        cursor.close()
        connection.close()


def add_supplier(invoice, name, contact, description, treeview):
    if invoice == '' or name == '' or contact == '' or description.strip() == '':
        messagebox.showerror("Error", "Please fill all fields")
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system;')
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS supplier_data (invoice INT PRIMARY KEY, name VARCHAR(100), contact VARCHAR(15), description TEXT)")

            cursor.execute('SELECT * from supplier_data WHERE invoice=%s', invoice)
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id already exists')
                return

            cursor.execute("INSERT INTO supplier_data VALUES (%s, %s, %s, %s)",
                           (invoice, name, contact, description.strip()))
            connection.commit()
            messagebox.showinfo("Success", "Supplier added")
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror("Error", f"Error due to {e}")
        finally:
            cursor.close()
            connection.close()


def select_data(event, invoice_entry, name_entry, contact_entry, description_text, treeview):
    index = treeview.selection()
    content = treeview.item(index)
    actual_content = content['values']
    invoice_entry.delete(0, END)
    name_entry.delete(0, END)
    contact_entry.delete(0, END)
    description_text.delete(1.0, END)
    invoice_entry.insert(0, actual_content[0])
    name_entry.insert(0, actual_content[1])
    contact_entry.insert(0, actual_content[2])
    description_text.insert(1.0, actual_content[3])


def update_supplier(invoice, name, contact, description, treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror("Error", "You need to select a supplier.")
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("use inventory_system")
        cursor.execute("select * from supplier_data where invoice = %s", invoice)
        row = cursor.fetchone()
        row = row[1:]
        new_data = (name, contact, description)
        if row == new_data:
            messagebox.showerror("Error", "No changes detected.")
            return
        cursor.execute("UPDATE supplier_data SET name = %s, contact = %s, description = %s WHERE invoice = %s",
                       (name, contact, description, invoice))
        connection.commit()
        messagebox.showinfo("Success", "Data is updated.")
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror("Error", f"Error due to {e}")
    finally:
        cursor.close()
        connection.close()


def delete_supplier(invoice, treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror("Error", "You need to select a supplier.")
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("use inventory_system")
        cursor.execute("delete from supplier_data where invoice = %s", (invoice,))
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo("Success", "Record successfully deleted.")
    except Exception as e:
        messagebox.showerror("Error", f"Error due to {e}")
    finally:
        cursor.close()
        connection.close()


def clear(invoice_entry, name_entry, contact_entry, description_text, treeview):
    invoice_entry.delete(0, END)
    name_entry.delete(0, END)
    contact_entry.delete(0, END)
    description_text.delete(1.0, END)
    treeview.selection_remove(treeview.selection())


def search_supplier(invoice, treeview):
    if invoice == '':
        messagebox.showerror("Error", "Please enter invoice no.")
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("use inventory_system")
        cursor.execute("select * from supplier_data where invoice = %s", invoice)
        record = cursor.fetchone()
        if not record:
            messagebox.showerror("Error", "No record found.")
            cursor.close()
            connection.close()
            return
        treeview.delete(*treeview.get_children())
        treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror("Error", f"Error due to {e}")
    finally:
        cursor.close()
        connection.close()


def show_all(treeview):
    treeview_data(treeview)


def supplier_form(window):
    global back_image
    supplier_frame = Frame(window, width=1070, height=567, bg="white")
    supplier_frame.place(x=200, y=100)

    heading_label = Label(supplier_frame, text="Manage Supplier Details", font=("Helvetica", 16, "bold"), bg="#0f4d7d",
                          fg="white")
    heading_label.place(x=0, y=0, relwidth=1)
    back_image = PhotoImage(file="images/back_button.png")

    back_button = tkm.Button(supplier_frame, bg="white", image=back_image, bd=0, cursor="hand2", borderless=1,
                             command=lambda: supplier_frame.place_forget())
    back_button.place(x=10, y=30)

    left_frame = Frame(supplier_frame, bg="white")
    left_frame.place(x=10, y=100)

    invoice_label = Label(left_frame, text='Invoice No.', font=('helvetica', 14, 'bold'), bg="white", fg="black")
    invoice_label.grid(row=0, column=0, padx=(20, 40), sticky='w')
    invoice_entry = Entry(left_frame, font=('helvetica', 14, 'bold'), bg="lightyellow", fg="black")
    invoice_entry.grid(row=0, column=1)

    name_label = Label(left_frame, text='Supplier Name', font=('helvetica', 14, 'bold'), bg="white", fg="black")
    name_label.grid(row=1, column=0, padx=(20, 40), pady=25, sticky='w')
    name_entry = Entry(left_frame, font=('helvetica', 14, 'bold'), bg="lightyellow", fg="black")
    name_entry.grid(row=1, column=1)

    contact_label = Label(left_frame, text='Contact', font=('helvetica', 14, 'bold'), bg="white", fg="black")
    contact_label.grid(row=2, column=0, padx=(20, 40), sticky='w')
    contact_entry = Entry(left_frame, font=('helvetica', 14, 'bold'), bg="lightyellow", fg="black")
    contact_entry.grid(row=2, column=1)

    description_label = Label(left_frame, text='Description', font=('helvetica', 14, 'bold'), bg="white", fg="black")
    description_label.grid(row=3, column=0, padx=(20, 40), pady=25, sticky='nw')
    description_text = Text(left_frame, font=('helvetica', 14, 'bold'), bg="lightyellow", fg="black", height=6,
                            width=20, bd=2)
    description_text.grid(row=3, column=1, pady=25)

    button_frame = Frame(left_frame, bg="white", pady=20)
    button_frame.grid(row=4, columnspan=2)

    add_button = tkm.Button(button_frame, width=80, height=30, text='Add', font=("Helvetica", 14),
                            cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                            command=lambda: add_supplier(invoice_entry.get(), name_entry.get(), contact_entry.get(),
                                                         description_text.get(1.0, END), treeview))
    add_button.grid(row=0, column=0, padx=20)

    update_button = tkm.Button(button_frame, width=80, height=30, text='Update', font=("Helvetica", 14),
                               cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                               command=lambda: update_supplier(invoice_entry.get(), name_entry.get(),
                                                               contact_entry.get(),
                                                               description_text.get(1.0, END).strip(), treeview))
    update_button.grid(row=0, column=1)

    delete_button = tkm.Button(button_frame, width=80, height=30, text='Delete', font=("Helvetica", 14),
                               cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                               command=lambda: delete_supplier(invoice_entry.get(), treeview))
    delete_button.grid(row=0, column=2, padx=20)

    clear_button = tkm.Button(button_frame, width=80, height=30, text='Clear', font=("Helvetica", 14),
                              cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                              command=lambda: clear(invoice_entry, name_entry, contact_entry, description_text,
                                                    treeview))
    clear_button.grid(row=0, column=3)

    right_frame = Frame(supplier_frame, bg="white")
    right_frame.place(x=520, y=100, width=500, height=340)

    search_frame = Frame(right_frame, bg="white")
    search_frame.pack(pady=10)

    num_label = Label(search_frame, text='Invoice No.', font=('helvetica', 14, 'bold'), bg="white", fg="black")
    num_label.grid(row=0, column=0, padx=10, sticky='w')
    search_entry = Entry(search_frame, font=('helvetica', 14, 'bold'), bg="lightyellow", fg="black", width=10)
    search_entry.grid(row=0, column=1)

    search_button = tkm.Button(search_frame, width=80, height=30, text='Search', font=("Helvetica", 14),
                               cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                               command=lambda: search_supplier(search_entry.get(), treeview))
    search_button.grid(row=0, column=2, padx=10)

    show_button = tkm.Button(search_frame, width=80, height=30, text='Show All', font=("Helvetica", 14),
                             cursor="hand2", fg="white", bg="#0f4d7d", borderless=1, command=lambda: show_all(treeview))
    show_button.grid(row=0, column=3)

    horizontal_scrollbar = Scrollbar(right_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(right_frame, orient=VERTICAL)
    treeview = ttk.Treeview(right_frame, column=('invoice', 'name', 'contact', 'description'), show='headings',
                            xscrollcommand=horizontal_scrollbar.set,
                            yscrollcommand=vertical_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)
    treeview.heading('invoice', text='Invoice Id')
    treeview.heading('name', text='Supplier Name')
    treeview.heading('contact', text='Supplier Contact')
    treeview.heading('description', text='Description')
    treeview.column('invoice', width=80)
    treeview.column('name', width=160)
    treeview.column('contact', width=120)
    treeview.column('description', width=300)

    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',
                  lambda event: select_data(event, invoice_entry, name_entry, contact_entry, description_text,
                                            treeview))
    return supplier_frame
