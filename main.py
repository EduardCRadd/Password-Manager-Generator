import tkinter as tk
from tkinter import messagebox
import random
import pyperclip
import sqlite3


# DATABASE.
db = sqlite3.connect('user-data.db')
cursor = db.cursor()
id = None

# cursor.execute('CREATE TABLE UserData (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
#                'website varchar(250) NOT NULL UNIQUE, '
#                'email varchar(250) NOT NULL, '
#                'password varchar(250) NOT NULL)')

# cursor.execute('INSERT INTO UserData VALUES(1, "amazon.co.uk", "my_email@gmail.com", "wieuiwrhfg4")')
# db.commit()


# PASSWORD GENERATOR.
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, string=password)
    pyperclip.copy(password)


# SAVE PASSWORD.
def save():
    website = website_entry.get()  # .get() fetches the current entry text.
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            cursor.execute("INSERT INTO UserData VALUES(?, ?, ?, ?)",
                           (None, website_entry.get(), email_entry.get(), password_entry.get()))
            db.commit()

        finally:
            website_entry.delete(0, tk.END)  # .delete() from index 0, first char till the END.
            password_entry.delete(0, tk.END)


#  FIND PASSWORD.
def find_password():
    website = website_entry.get()

    try:
        cursor.execute("SELECT * FROM UserData WHERE website=?", (website,))
        result = cursor.fetchall()
        print(result)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")

    else:
        if website in result[0]:
            email = result[0][1]
            password = result[0][3]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# UI INTERFACE.
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = tk.Canvas(width=200, height=200, highlightthickness=0)
logo_img = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = tk.Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = tk.Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = tk.Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = tk.Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = tk.Entry(width=39)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "your_email@gmail.com")  # .insert(index, string), index 0=first char.
password_entry = tk.Entry(width=21)
password_entry.grid(column=1, row=3)

# Buttons
generate_password_button = tk.Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)
add_button = tk.Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = tk.Button(text="Search...", width=13, command=find_password)
search_button.grid(column=2, row=1)


window.mainloop()
