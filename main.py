from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def create_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    pass_entry.delete(0, END)

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_list)

    password = "".join(password_list)

    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def content_entry():
    website = website_entry.get()
    username = name_entry.get()
    password = pass_entry.get()
    password_data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(username) == 0:
        messagebox.showwarning(title="Invalid Entry", message="Please make sure you have entered your details!")

    else:
        try:
            with open("passwords.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("passwords.json", "w") as file:
                json.dump(password_data, file, indent=4)
        except json.JSONDecodeError:
            with open("passwords.json", "w") as file:
                json.dump(password_data, file, indent=4)
        else:
            data.update(password_data)
            with open("passwords.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, "end")
            pass_entry.delete(0, "end")
            website_entry.focus()


# ---------------------------- SAVE PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("passwords.json", "r") as file:
            pwd = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Invalid search", message="No data file found.")
    except json.JSONDecodeError:
        messagebox.showerror(title="Invalid search", message="Data file is empty.")
    else:
        if website in pwd:
            username = pwd[website].get("email")
            password = pwd[website].get("password")
            messagebox.showinfo(title="Saved password", message=f"Your saved details are: \nEmail: {username} "
                                                                f"\nPassword: {password}")
        elif len(website) > 0:
            messagebox.showwarning(title="Invalid search", message="Please enter a website name to search.")
        else:
            messagebox.showerror(title="Invalid search", message="The website's details you are trying to access do not exist")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=2, row=1)

website_lbl = Label(text="Website:")
website_lbl.grid(column=1, row=2)
name_lbl = Label(text="Email/Username:")
name_lbl.grid(column=1, row=3)
pass_lbl = Label(text="Password:")
pass_lbl.grid(column=1, row=4)

website_entry = Entry(width=21)
website_entry.grid(column=2, row=2)
website_entry.focus()
name_entry = Entry(width=35)
name_entry.grid(column=2, row=3, columnspan=2)
name_entry.insert(0, "ariwalamustafa853@gmail.com")
pass_entry = Entry(width=21)
pass_entry.grid(column=2, row=4)

gen_button = Button(text="Generate P", command=create_password)
gen_button.grid(column=3, row=4)
add_button = Button(text="Add", width=36, command=content_entry)
add_button.grid(column=2, row=5, columnspan=2)
search_button = Button(text="Search", command=find_password)
search_button.grid(column=3, row=2)

window.mainloop()
