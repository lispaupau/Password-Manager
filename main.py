import tkinter
from tkinter import messagebox
import random
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)] + \
                    [random.choice(symbols) for _ in range(nr_symbols)] + \
                    [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)
    gen_password = ''.join(password_list)
    pass_entry.delete(0, tkinter.END)
    pass_entry.insert(0, gen_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = pass_entry.get()
    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title='Oops', message='Please don`t leave any fields empty!')
    else:
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        data.update(new_data)

        with open('data.json', 'w') as data_file:
            json.dump(data, data_file, indent=4)

            website_entry.delete(0, tkinter.END)
            pass_entry.delete(0, tkinter.END)
            website_entry.focus()


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
        messagebox.showinfo(title=website, message=f'Email: {data[website]["email"]}\n'
                                                   f'Password: {data[website]["password"]}')
    except KeyError:
        messagebox.showwarning(title='Error.', message='This website was not found in the database.')
    except FileNotFoundError:
        messagebox.showwarning(title='Error', message='Database is empty or missing.')

    finally:
        website_entry.delete(0, tkinter.END)
        pass_entry.delete(0, tkinter.END)
        website_entry.focus()


# ---------------------------- SHOW SAVED WEBSITES ------------------------------- #
def show_saved_websites():
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
            list_websites = list(data.keys())
            messagebox.showinfo(title='Saved Websites', message='\n'.join(list_websites))
    except FileNotFoundError:
        messagebox.showwarning(title='Error', message='Database is empty or missing.')


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.config(padx=50, pady=50)
window.title('Password Manager')

canvas = tkinter.Canvas(width=200, height=200)
logo_img = tkinter.PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = tkinter.Label(text='Website:')
website_label.grid(column=0, row=1)
email_label = tkinter.Label(text='Email/Username:')
email_label.grid(column=0, row=2)
pass_label = tkinter.Label(text='Password:')
pass_label.grid(column=0, row=3)

# Entries
website_entry = tkinter.Entry(width=21)
website_entry.grid(column=1, row=1, columnspan=1)
website_entry.focus()
email_entry = tkinter.Entry(width=21)
email_entry.grid(column=1, row=2, columnspan=1)
email_entry.insert(0, 'pndao@inbox.ru')
pass_entry = tkinter.Entry(width=21)
pass_entry.grid(column=1, row=3)

# Buttons
gen_pass_button = tkinter.Button(text='Generate Password', width=13, command=generate_password)
gen_pass_button.grid(column=2, row=3)
add_button = tkinter.Button(text='Add', width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = tkinter.Button(text='Search', width=13, command=find_password)
search_button.grid(column=2, row=1)
show_websites = tkinter.Button(text='Saved Websites', command=show_saved_websites)
show_websites.grid(column=2, row=2)

window.mainloop()
