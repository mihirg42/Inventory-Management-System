from tkinter import *
from tkinter import ttk
import tkmacosx as tkm
from tkinter import messagebox
from employees import connect_database, treeview_data


def show_all(treeview, search_combobox, search_entry):
    treeview_data(treeview)
    search_combobox.set("Search By")
    search_entry.delete(0, END)


def search_product(search_combobox, search_entry, treeview):
    if search_combobox.get() == 'Search By':
        messagebox.showinfo('Error', 'Please select an option')
    elif search_entry.get() == '':
        messagebox.showinfo('Error', 'Please enter the value to search')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return;
        try:
            cursor.execute("use inventory_system")
            cursor.execute(f'SELECT * FROM product_data WHERE {search_combobox.get()} LIKE "%{search_entry.get()}%"')
            records = cursor.fetchall()
            if (len(records) == 0):
                messagebox.showinfo('Error', 'No products found')
                return
            treeview.delete(*treeview.get_children())
            for row in records:
                treeview.insert('', END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Error due to {e}")
        finally:
            cursor.close()
            connection.close()


def clear_fields(category_combobox, supplier_combobox, name_entry,
                 price_entry, quantity_entry, status_combobox, treeview):
    treeview.selection_remove(treeview.selection())
    category_combobox.set("Select")
    supplier_combobox.set("Select")
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)
    status_combobox.set("Select")


def delete_product(treeview):
    index = treeview.selection()
    dict = treeview.item(index)
    content = dict['values']
    id = content[0]
    if not index:
        messagebox.showerror("Error", "You need to select a product.")
        return
    ans = messagebox.askyesno("Delete Product", "Do you really want to delete this product?")
    if ans:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute("use inventory_system")
            cursor.execute("delete from product_data where id = %s", (id,))
            connection.commit()
            treeview_data(treeview)
            messagebox.showinfo("Success", "Record successfully deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to {e}")
        finally:
            cursor.close()
            connection.close()


def update_product(category, supplier, name, price, quantity, status, treeview):
    index = treeview.selection()
    dict = treeview.item(index)
    content = dict['values']
    id = content[0]
    if not index:
        messagebox.showerror(title="Error", message="No item selected")
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("use inventory_system")
        cursor.execute("select * from product_data where id = %s", id)
        current_data = cursor.fetchone()
        current_data = current_data[1:]
        current_data = list(current_data)
        current_data[3] = str(current_data[3])
        current_data[4] = str(current_data[4])
        current_data = tuple(current_data)
        new_data = (category, supplier, name, price, quantity, status)
        if current_data == new_data:
            messagebox.showerror("Error", "No changes detected.")
            return
        cursor.execute(
            "UPDATE product_data SET category = %s, supplier = %s, name = %s, price = %s, quantity = %s, status = %s WHERE id = %s",
            (category, supplier, name, price, quantity, status, id))
        connection.commit()
        messagebox.showinfo("Success", "Data is updated.")
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror("Error", f"Error due to {e}")
    finally:
        cursor.close()
        connection.close()


def select_data(event, treeview, category_combobox, supplier_combobox, name_entry,
                price_entry, quantity_entry, status_combobox):
    index = treeview.selection()
    dict = treeview.item(index)
    content = dict['values']

    name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)

    category_combobox.set(content[1])
    supplier_combobox.set(content[2])
    name_entry.insert(0, content[3])
    price_entry.insert(0, content[4])
    quantity_entry.insert(0, content[5])
    status_combobox.set(content[6])


def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system;')
        cursor.execute('SELECT * from product_data;')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for row in records:
            treeview.insert('', END, values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Error due to {e}")
    finally:
        cursor.close()
        connection.close()


def fetch_supplier_category(category_combobox, supplier_combobox):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        category_option = []
        supplier_option = []
        cursor.execute("use inventory_system")
        cursor.execute("select name from category_data")
        names = cursor.fetchall()
        if (len(names) > 0):
            category_combobox.set("Select")
            for name in names:
                category_option.append(name[0])
            category_combobox.config(value=category_option)

        cursor.execute("select name from supplier_data")
        names = cursor.fetchall()
        if (len(names) > 0):
            supplier_combobox.set("Select")
            for name in names:
                supplier_option.append(name[0])
            supplier_combobox.config(value=supplier_option)
    except Exception as e:
        messagebox.showerror("Error", f"Error due to {e}")
    finally:
        cursor.close()
        connection.close()


def add_product(category, supplier, name, price, quantity, status, treeview):
    if category == 'Empty':
        messagebox.showerror('Error', 'Please add a category')
    elif supplier == 'Empty':
        messagebox.showerror('Error', 'Please add a supplier')
    elif category == 'Select' or supplier == 'Select' or name == '' or price == '' or quantity == '' or status == 'Select':
        messagebox.showerror('Error', 'Please fill all fields')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute("USE inventory_system")
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS product_data
                (
                    id
                    INT
                    AUTO_INCREMENT
                    PRIMARY
                    KEY,
                    category
                    VARCHAR
                   (
                    100
                   ), supplier varchar
                   (
                       100
                   ), name varchar
                   (
                       100
                   ),price DECIMAL
                   (
                       10,
                       2
                   ), quantity INT, status VARCHAR
                   (
                       50
                   ))""")
            cursor.execute("SELECT * FROM product_data WHERE category=%s and supplier = %s and name = %s",
                           (category, supplier, name))
            existing_product = cursor.fetchone()
            if existing_product:
                messagebox.showerror('Error', 'Product already exists')
                return

            cursor.execute(
                "INSERT INTO product_data (category, supplier, name, price, quantity, status) VALUES(%s, %s, %s, %s, %s, %s)",
                (category, supplier, name, price, quantity, status))
            connection.commit()
            messagebox.showinfo('Success', 'Product added successfully')
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror("Error", f"Error due to {e}")
        finally:
            cursor.close()
            connection.close()


def product_form(window):
    product_frame = Frame(window, width=1070, height=567, bg="white")
    product_frame.place(x=200, y=100)

    back_image = PhotoImage(file="images/back_button.png")
    back_button = tkm.Button(product_frame, bg="white", image=back_image, bd=0, cursor="hand2", borderless=1,
                             command=lambda: product_frame.place_forget())
    back_button.place(x=10, y=5)

    left_frame = Frame(product_frame, bg="white", bd=2, relief=RIDGE)
    left_frame.place(x=20, y=40)

    heading_label = Label(left_frame, text="Manage Product Details", font=("Helvetica", 16, "bold"), bg="#0f4d7d",
                          fg="white")
    heading_label.grid(row=0, columnspan=2, sticky="we")

    category_label = Label(left_frame, text="Category", font=("Helvetica", 14, "bold"), bg="white", fg="black")
    category_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')
    category_combobox = ttk.Combobox(left_frame, font=("Helvetica", 14, "bold"),
                                     width=18,
                                     state='readonly')
    category_combobox.set("Empty")
    category_combobox.grid(row=1, column=1, pady=40)

    supplier_label = Label(left_frame, text="Supplier", font=("Helvetica", 14, "bold"), bg="white", fg="black")
    supplier_label.grid(row=2, column=0, padx=20, sticky='w')
    supplier_combobox = ttk.Combobox(left_frame, font=("Helvetica", 14, "bold"),
                                     width=18,
                                     state='readonly')
    supplier_combobox.set("Empty")
    supplier_combobox.grid(row=2, column=1)

    name_label = Label(left_frame, text='Product Name', font=('helvetica', 14, 'bold'), bg="white", fg="black")
    name_label.grid(row=3, column=0, padx=20, pady=40, sticky='w')
    name_entry = Entry(left_frame, font=('helvetica', 14, 'bold'), bg="lightyellow", fg="black")
    name_entry.grid(row=3, column=1)

    price_label = Label(left_frame, text='Price', font=('helvetica', 14, 'bold'), bg="white", fg="black")
    price_label.grid(row=4, column=0, padx=20, sticky='w')
    price_entry = Entry(left_frame, font=('helvetica', 14, 'bold'), bg="lightyellow", fg="black")
    price_entry.grid(row=4, column=1)

    quantity_label = Label(left_frame, text='Quantity', font=('helvetica', 14, 'bold'), bg="white", fg="black")
    quantity_label.grid(row=5, column=0, padx=20, pady=40, sticky='w')
    quantity_entry = Entry(left_frame, font=('helvetica', 14, 'bold'), bg="lightyellow", fg="black")
    quantity_entry.grid(row=5, column=1)

    status_label = Label(left_frame, text="Status", font=("Helvetica", 14, "bold"), bg="white", fg="black")
    status_label.grid(row=6, column=0, padx=20, sticky='w')
    status_combobox = ttk.Combobox(left_frame, values=("Active", "Inactive"), font=("Helvetica", 14, "bold"),
                                   width=18,
                                   state='readonly')
    status_combobox.set("Select")
    status_combobox.grid(row=6, column=1)

    button_frame = Frame(left_frame, bg="white")
    button_frame.grid(row=7, columnspan=2, pady=(30, 10))

    add_button = tkm.Button(button_frame, width=80, height=30, text='Add', font=("Helvetica", 14),
                            cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                            command=lambda: add_product(category_combobox.get(), supplier_combobox.get(),
                                                        name_entry.get(), price_entry.get(), quantity_entry.get(),
                                                        status_combobox.get(), treeview))
    add_button.grid(row=0, column=0, padx=10)

    update_button = tkm.Button(button_frame, width=80, height=30, text='Update', font=("Helvetica", 14),
                               cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                               command=lambda: update_product(category_combobox.get(), supplier_combobox.get(),
                                                              name_entry.get(), price_entry.get(), quantity_entry.get(),
                                                              status_combobox.get(), treeview))
    update_button.grid(row=0, column=1, padx=10)

    delete_button = tkm.Button(button_frame, width=80, height=30, text='Delete', font=("Helvetica", 14),
                               cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                               command=lambda: delete_product(treeview))
    delete_button.grid(row=0, column=2, padx=10)

    clear_button = tkm.Button(button_frame, width=80, height=30, text='Clear', font=("Helvetica", 14),
                              cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                              command=lambda: clear_fields(category_combobox, supplier_combobox, name_entry,
                                                           price_entry, quantity_entry, status_combobox, treeview))
    clear_button.grid(row=0, column=3, padx=10)

    search_frame = LabelFrame(product_frame, text="Search Product", font=("Helvetica", 14), bg="white", fg="black")
    search_frame.place(x=480, y=30)

    search_combobox = ttk.Combobox(search_frame, values=("Category", "Supplier", "Name", "Status"),
                                   font=("Helvetica", 14, "bold"),
                                   width=16,
                                   state='readonly')
    search_combobox.set("Search By")
    search_combobox.grid(row=0, column=0, padx=10)

    search_entry = Entry(search_frame, font=('helvetica', 14, 'bold'), bg="lightyellow", fg="black", width=16)
    search_entry.grid(row=0, column=1, padx=10)

    search_button = tkm.Button(search_frame, width=95, height=30, text='Search', font=("Helvetica", 14),
                               cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                               command=lambda: search_product(search_combobox, search_entry, treeview))
    search_button.grid(row=0, column=2, padx=10, pady=10)

    show_button = tkm.Button(search_frame, width=95, height=30, text='Show All', font=("Helvetica", 14),
                             cursor="hand2", fg="white", bg="#0f4d7d", borderless=1,
                             command=lambda: show_all(treeview, search_combobox, search_entry))
    show_button.grid(row=0, column=3, padx=10)

    treeview_frame = Frame(product_frame, bg="white")
    treeview_frame.place(x=480, y=125, width=570, height=430)

    horizontal_scrollbar = Scrollbar(treeview_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(treeview_frame, orient=VERTICAL)
    treeview = ttk.Treeview(treeview_frame,
                            column=('id', 'category', 'supplier', 'name', 'price', 'quantity', 'status'),
                            show='headings',
                            xscrollcommand=horizontal_scrollbar.set,
                            yscrollcommand=vertical_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)
    treeview.heading("id", text="ID")
    treeview.heading('category', text='Category Name')
    treeview.heading('supplier', text='Supplier')
    treeview.heading('name', text='Product Name')
    treeview.heading('price', text='Price')
    treeview.heading('quantity', text='Quantity')
    treeview.heading('status', text='Status')

    fetch_supplier_category(category_combobox, supplier_combobox)
    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',
                  lambda event: select_data(event, treeview, category_combobox, supplier_combobox, name_entry,
                                            price_entry, quantity_entry, status_combobox))
    return product_frame
