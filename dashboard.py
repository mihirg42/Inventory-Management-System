from tkinter import *
import tkmacosx as tkm
from employees import employee_form
from supplier import supplier_form
from category import category_form
from products import product_form
from employees import connect_database
import time


def update():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute("use inventory_system")
    cursor.execute("SELECT * from employee_data")
    records = cursor.fetchall()
    total_emp_count_label.config(text=str(len(records)))

    cursor.execute("SELECT * from supplier_data")
    records = cursor.fetchall()
    total_sup_count_label.config(text=str(len(records)))

    cursor.execute("SELECT * from category_data")
    records = cursor.fetchall()
    total_cat_count_label.config(text=str(len(records)))

    cursor.execute("SELECT * from product_data")
    records = cursor.fetchall()
    total_prod_count_label.config(text=str(len(records)))

    date_time = time.strftime("%I:%M:%S %p on %A, %d/%m/%Y")
    subtitleLabel.config(text=f"\t\t\tWelcome Admin\t\t\t\t {date_time}")
    subtitleLabel.after(1000, update)


current_frame = None


def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame = form_function(window)


window = Tk()
window.title("Dashboard")
window.geometry("1270x668+0+0")
window.resizable(width=0, height=0)
window.configure(background='white')

bg_image = PhotoImage(file='images/inventory.png')
titleLabel = Label(window, image=bg_image, compound=LEFT, text="  Inventory Management Status",
                   font=("helvetica", 40, "bold"), fg="white", bg="#010c48", anchor="w", padx=20)
titleLabel.place(x=0, y=0, relwidth=1)

logoutButton = tkm.Button(window, text="Logout", font=("helvetica", 20, "bold"), fg="#010c48")
logoutButton.place(x=1100, y=10)

subtitleLabel = Label(window, text="Welcome Admin\t\t Date: 07-08-2025\t\t Time: 12:36:17 pm", font=("helvetica", 15),
                      bg='#4d636d', fg='white')
subtitleLabel.place(x=0, y=70, relwidth=1)

leftFrame = Frame(window, bg="#bebebe")
leftFrame.place(x=0, y=102, width=200, height=567)

logoImage = PhotoImage(file='images/logo.png')
imageLabel = Label(leftFrame, image=logoImage, bg="#bebebe")
imageLabel.pack()

menuLabel = Label(leftFrame, text="Menu", font=("helvetica", 20), bg='#009688')
menuLabel.pack(fill=X)

employee_button = tkm.Button(leftFrame, cursor="hand2", text="Employees", font=("helvetica", 20, "bold"),
                             command=lambda: show_form(employee_form))
employee_button.pack(fill=X)

supplier_button = tkm.Button(leftFrame, cursor="hand2", text="Supplier", font=("helvetica", 20, "bold"),
                             command=lambda: show_form(supplier_form))
supplier_button.pack(fill=X)

category_button = tkm.Button(leftFrame, cursor="hand2", text="Category", font=("helvetica", 20, "bold"),
                             command=lambda: show_form(category_form))
category_button.pack(fill=X)
category_button.pack(fill=X)

products_button = tkm.Button(leftFrame, cursor="hand2", text="Products", font=("helvetica", 20, "bold"),
                             command=lambda: show_form(product_form))
products_button.pack(fill=X)

# sales_button = tkm.Button(leftFrame, cursor="hand2", text="Sales", font=("helvetica", 20, "bold"))
# sales_button.pack(fill=X)
#
# exit_button = tkm.Button(leftFrame, cursor="hand2", text="Exit", font=("helvetica", 20, "bold"))
# exit_button.pack(fill=X)

emp_frame = Frame(window, bg="#2c3e50", bd=3, relief=RIDGE)
emp_frame.place(x=400, y=200, width=280, height=170)
total_emp_icon = PhotoImage(file='images/total_emp.png')
total_emp_icon_label = Label(emp_frame, image=total_emp_icon, bg='#2C3E50')
total_emp_icon_label.pack(pady=5)
total_emp_label = Label(emp_frame, text='Total Employees', bg='#2C3E50', fg='white', font=('helvetica', 15, 'bold'))
total_emp_label.pack()
total_emp_count_label = Label(emp_frame, text='0', bg='#2C3E50', fg='white', font=('helvetica', 50, 'bold'))
total_emp_count_label.pack()

sup_frame = Frame(window, bg="#8e44ad", bd=3, relief=RIDGE)
sup_frame.place(x=800, y=200, width=280, height=170)
total_sup_icon = PhotoImage(file='images/total_sup.png')
total_sup_icon_label = Label(sup_frame, image=total_sup_icon, bg='#8e44ad')
total_sup_icon_label.pack(pady=5)
total_sup_label = Label(sup_frame, text='Total Suppliers', bg='#8e44ad', fg='white', font=('helvetica', 15, 'bold'))
total_sup_label.pack()
total_sup_count_label = Label(sup_frame, text='0', bg='#8e44ad', fg='white', font=('helvetica', 50, 'bold'))
total_sup_count_label.pack()

cat_frame = Frame(window, bg="#27ae60", bd=3, relief=RIDGE)
cat_frame.place(x=400, y=385, width=280, height=170)
total_cat_icon = PhotoImage(file='images/total_cat.png')
total_cat_icon_label = Label(cat_frame, image=total_cat_icon, bg='#27ae60')
total_cat_icon_label.pack(pady=5)
total_cat_label = Label(cat_frame, text='Total Categories', bg='#27ae60', fg='white', font=('helvetica', 15, 'bold'))
total_cat_label.pack()
total_cat_count_label = Label(cat_frame, text='0', bg='#27ae60', fg='white', font=('helvetica', 50, 'bold'))
total_cat_count_label.pack()

prod_frame = Frame(window, bg="#e74c3c", bd=3, relief=RIDGE)
prod_frame.place(x=800, y=385, width=280, height=170)
total_prod_icon = PhotoImage(file='images/total_prod.png')
total_prod_icon_label = Label(prod_frame, image=total_prod_icon, bg='#e74c3c')
total_prod_icon_label.pack(pady=5)
total_prod_label = Label(prod_frame, text='Total Products', bg='#e74c3c', fg='white', font=('helvetica', 15, 'bold'))
total_prod_label.pack()
total_prod_count_label = Label(prod_frame, text='0', bg='#e74c3c', fg='white', font=('helvetica', 50, 'bold'))
total_prod_count_label.pack()

# sales_frame = Frame(window, bg="#e74c3c", bd=3, relief=RIDGE)
# sales_frame.place(x=600, y=495, width=280, height=170)
# total_sales_icon = PhotoImage(file='images/total_sales.png')
# total_sales_icon_label = Label(sales_frame, image=total_sales_icon, bg='#e74c3c')
# total_sales_icon_label.pack(pady=5)
# total_sales_label = Label(sales_frame, text='Total Sales', bg='#e74c3c', fg='white', font=('helvetica', 15, 'bold'))
# total_sales_label.pack()
# total_sales_count_label = Label(sales_frame, text='0', bg='#e74c3c', fg='white', font=('helvetica', 50, 'bold'))
# total_sales_count_label.pack()

update()
window.mainloop()
