# sqlite Database Test
from tkinter import*
from tkinter import messagebox
import sqlite3
import webbrowser
from tkinter import ttk
import sys
import os
import random
from email.message import EmailMessage
import smtplib

if sys.platform == 'win32':
    base64 = "Win32GUI"

root = Tk()
root.geometry('600x600')
root.title("Student Records")
root.resizable(False, False)

name = StringVar()
adm = StringVar()
gender = StringVar()
age = IntVar()
stream = StringVar()

searchB = StringVar()
searchtext = StringVar()

label1 = Label(root, text="NAME")
label1.grid(column=0, row=0, sticky=W)
entry1 = Entry(root, bd=3, textvariable=name)
entry1.grid(column=1, row=0)

label2 = Label(root, text="ADM")
label2.grid(column=0, row=1, sticky=W)
entry2 = Entry(root, bd=3, textvariable=adm)
entry2.grid(column=1, row=1)

label3 = Label(root, text="GENDER")
label3.grid(column=0, row=2, sticky=W)
entry3 = Entry(root, bd=3, textvariable=gender)
entry3.grid(column=1, row=2)

label4 = Label(root, text="AGE")
label4.grid(column=0, row=3, sticky=W)
entry4 = Entry(root, bd=3, textvariable=age)
entry4.grid(column=1, row=3)

label4 = Label(root, text="STREAM")
label4.grid(column=0, row=4, sticky=W)
entry4 = Entry(root, bd=3, textvariable=stream)
entry4.grid(column=1, row=4)

FromEntry = ttk.Combobox(root, width=18, textvariable=searchB, font=('Verdana', 12, 'bold'))
FromEntry['value'] = ('Adm', 'Stream', 'Name')
FromEntry.current(0)
FromEntry.grid(column=2, row=1)
entry4 = Entry(root, bd=3, textvariable=searchtext)
entry4.grid(column=3, row=1)


def register():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students(
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        NAME TEXT NOT NULL,
        ADM INTEGER NOT NULL,
        GENDER TEXT NOT NULL,
        AGE INTEGER NOT NULL,
        STREAM TEXT NOT NULL    
        )''')

    insert = "INSERT INTO students(NAME, ADM, GENDER, AGE, STREAM) VALUES(?,?,?,?,?)"
    VAL = (name.get(),
           adm.get(),
           gender.get(),
           age.get(),
           stream.get()
           )
    cursor.execute(insert, VAL)
    connect.commit()
    display()
    connect.close()
    messagebox.showinfo("Success", "Record saved successfully", parent=root)


def browse():
    webbrowser.open("www.facebook.com")


style = ttk.Style(root)
style.configure("Treeview.Heading", font=('verdana', 11, 'bold'), foreground="red")
records = ttk.Treeview(root, height=100,
                       selectmode=BROWSE,
                       columns=('ID',
                                "Name",
                                "Adm",
                                "Gender",
                                "Age",
                                "Stream",
                                ""
                                ))

# ======================Displaying the records============================================


def get_cursor(ev=""):
    global ID;
    global row;
    cursor_row = records.focus()
    content = records.item(cursor_row)
    row = content["values"]

    ID = row[0]
    name.set(row[1]),
    adm.set(row[2]),
    gender.set(row[3]),
    age.set(row[4]),
    stream.set(row[5])
    button2.config(state=NORMAL)
    button3.config(state=NORMAL)


X_scroller = Scrollbar(records, orient=HORIZONTAL, command=records.xview)
Y_scroller = Scrollbar(records, orient=VERTICAL, command=records.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

records.configure(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

records.heading('ID', text='ID', anchor=CENTER)
records.heading('Name', text='Name', anchor=CENTER)
records.heading('Adm', text='Adm', anchor=CENTER)
records.heading('Gender', text='Gender', anchor=CENTER)
records.heading('Age', text='Age', anchor=CENTER)
records.heading('Stream', text='Stream', anchor=CENTER)
records.heading('', text='', anchor=CENTER)

records.column('#0', width=0, stretch=NO)
records.column('#1', width=40, stretch=NO)
records.column('#2', width=140, stretch=NO)
records.column('#3', width=80, stretch=NO)
records.column('#4', width=80, stretch=NO)
records.column('#5', width=80, stretch=NO)
records.column('#6', width=100, stretch=NO)
records.place(y=170, x=30, relwidth=0.9, relheight=0.6, relx=0)
records.bind("<ButtonRelease-1>", get_cursor)


def display():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute("select * from students")
    row = cursor.fetchall()
    if len(row) != 0:
        records.delete(*records.get_children())
        for i in row:
            records.insert("", END, values=i)
        connect.commit()
    cursor.close()


def update():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE students set "
                   "NAME=?,"
                   " ADM=?,"
                   " GENDER=?,"
                   " AGE=?,"
                   " STREAM=?"
                   " WHERE ID=?",
                   (
        name.get(),
        adm.get(),
        gender.get(),
        age.get(),
        stream.get(),
        ID
    ))
    connect.commit()
    display()
    connect.close()
    messagebox.showinfo("Success", "Update Successful")


def delete():
    if records.selection():
        warn = messagebox.askquestion("Delete", "Are you sure to delete this record?", icon="warning")
        if warn == 'yes':
            connect = sqlite3.connect('Data.db')
            cursor = connect.cursor()
            cursor.execute("DELETE from students WHERE ID=%d" % row[0])
            connect.commit()
            display()
            connect.close()
        else:
            display()
    else:
        messagebox.showerror("Error", "Please select a record to delete")


def search():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * from students WHERE adm LIKE ?", (searchtext.get()))
    row = cursor.fetchall()
    if len(row) != 0:
        records.delete(*records.get_children())
        for i in row:
            records.insert("", END, values=i)
        connect.commit()
    cursor.close()


button = Button(root, text="SAVE", command=register)
button.grid(column=1, row=5)
button1 = Button(root, text="BROWSE", command=browse)
button1.grid(column=2, row=5)
button2 = Button(root, text="UPDATE RECORD", command=update, state=DISABLED)
button2.grid(column=2, row=0)
button3 = Button(root, text="DELETE RECORD", command=delete)
button3.grid(column=3, row=0)
button3 = Button(root, text="SEARCH RECORD", command=search, state=DISABLED)
button3.grid(column=3, row=2)
display()


root.update()
root.mainloop()
