import datetime
import webbrowser
import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import re
from datetime import date
import threading
import time
from plyer import notification

# connect to the database
conn = sqlite3.connect('s.db')
c = conn.cursor()

global userid

# create the users table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (email TEXT, username TEXT, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, description TEXT,
             amount REAL, expense_type TEXT,income REAL DEFAULT 0,savings REAL DEFAULT 0,  user INTEGER, email TEXT,
             deleted INTEGER DEFAULT 0, 
             FOREIGN KEY(user) REFERENCES users(rowid))''')



def send_notification():
    while True:
        now = datetime.datetime.now()
        notification_title = "Daily Expense Tracker"
        notification_text = f"Enter Your today's expense."
        notification.notify(title=notification_title, message=notification_text, timeout=10)
        time.sleep(3600 * 24)  # wait for 24 hours

thread = threading.Thread(target=send_notification)
thread.daemon = True
thread.start()

class LoginPage(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.on_login_success = on_login_success
        
        self.configure(background="#F4E3CA") # set background color to red
        
        # Add logo image
        logo_image = tk.PhotoImage(file="login.png")
        logo_label = tk.Label(self, image=logo_image, bg="#F4E3CA")
        logo_label.image = logo_image
        logo_label.grid(row=0, columnspan=2, padx=10, pady=10)
        
        # Set label colors
        label_bg = "#ED8E7C" # light red
        label_fg = "#FFFFFF" # white
        
        tk.Label(self, text="Email", bg=label_bg, fg=label_fg).grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Username", bg=label_bg, fg=label_fg).grid(row=2, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Password", bg=label_bg, fg=label_fg).grid(row=3, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=1, padx=5, pady=5)

        # Set button colors
        button_bg = "#ED8E7C" # light red
        button_fg = "#FFFFFF" # white
        
        tk.Button(self, text="Login", bg=button_bg, fg=button_fg, command=self.login).grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(self, text="Sign UP", bg=button_bg, fg=button_fg, command=self.create_user).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
       
       
        
        self.grid_rowconfigure(6, minsize=30)
        self.grid_rowconfigure(7, minsize=30)
        self.grid_columnconfigure(0, minsize=100)
        self.grid_columnconfigure(1, minsize=200)
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror("Error", "Invalid email address")
            return
        # cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        c.execute("SELECT * FROM users WHERE username = ? AND password = ? AND email = ?", (username, password, email))
        user = c.fetchone()

        # Check the username and password
        # if username == "admin" and password == "admin":
        if user is not None:
            print("login successfull")
            # userid = username
            # self.on_login_success
            expense_page = WelcomePage(root, username)
            expense_page.grid(row=0, column=0)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def create_user(self):
        # get the username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror("Error", "Invalid email address")
            return
        c.execute("SELECT rowid FROM users WHERE username=?", (username,))
        user = c.fetchone()

        if user:
         messagebox.showerror("Registration Failed", "Username already exists")
        else:
        # insert the user into the database
         c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
         conn.commit()
         messagebox.showinfo("Login Success", "You have successfully logged in!")
    
         
class WelcomePage(tk.Frame):
    
    def __init__(self, master, user_info):
        super().__init__(master)
        self.user_info = user_info

        self.user = self.user_info
        # self.user = "admin1"
        print(f"entering user, {self.user}")
        self.expenses = []
        self.expense_id = 0  
        if len(self.user_info) >= 101:
           self.income = self.user_info[100]
        else:
           self.income = None
        print(self.user_info)
        print(len(self.user_info))
        
        
        

        self.configure(bg="#F5F5F5")  # set background color

        # set background image
        bg_image = tk.PhotoImage(file="ccc.png")
        self.bg_label = tk.Label(self, image=bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.image = bg_image

        self.welcome_label = tk.Label(self, text="Welcome, " + self.user + "!", bg="#F5F5F5",font=('Arial', 13))
        self.welcome_label.pack() 
        self.expense_label = tk.Label(self, text="Expense:", bg="#F5F5F5",font=('Arial', 13))
        self.expense_label.pack()
        self.income_label = tk.Label(self, text="Income: ₹0.00", bg="#F5F5F5",font=('Arial', 13))
        self.income_label.pack()

        self.savings_label = tk.Label(self, text="Savings: ₹0.00", bg="#F5F5F5",font=('Arial', 13))
        self.savings_label.pack()
       
        today = date.today().strftime("%d/%m/%Y")
        tk.Label(self, text="Date", bg="#F5F5F5",font=('Arial', 13)).pack(padx=5, pady=5, side=tk.LEFT)
        self.date_label = tk.Label(self, text=today, bg="#FFFFFF",font=('Arial', 13))
        self.date_label.pack(padx=5, pady=5, side=tk.LEFT)
        # Schedule date update to run every day
        self.schedule_date_update()

        

        self.expense_description_label = tk.Label(self, text="Description:", bg="#F5F5F5", font=("Arial", 13))
        self.expense_description_label.pack(anchor='w')

        self.expense_description_entry = tk.Entry(self)
        self.expense_description_entry.pack(anchor='w')

        self.expense_amount_label = tk.Label(self, text="Amount:", bg="#F5F5F5", font=("Arial", 13))
        self.expense_amount_label.pack(anchor='w')

        self.expense_amount_entry = tk.Entry(self)
        self.expense_amount_entry.pack(anchor='w')

        self.expense_type_label = tk.Label(self, text="Type:", bg="#F5F5F5", font=("Arial", 13))
        self.expense_type_label.pack(anchor='w')

        self.check_mo = tk.IntVar()
        self.expense_type_mobile = tk.Checkbutton(self, text="Online", variable=self.check_mo, bg="#F5F5F5", font=('Arial', 13))
        self.expense_type_mobile.pack(anchor='w')

        self.check_te = tk.IntVar()
        self.expense_type_telephone = tk.Checkbutton(self, text="Cash", variable=self.check_te, bg="#F5F5F5", font=('Arial', 13))
        self.expense_type_telephone.pack(anchor='w')
        spacer_label = tk.Label(self, text="", height=1, bg="#F5F5F5")
        spacer_label.pack(anchor='w')

        self.add_expense_button = tk.Button(self, text="Add Expense", command=self.add_expense, font=('Arial', 13), padx=20, pady=10)
        self.add_expense_button.pack(anchor='w')        
        # Create the "Add Income" button
        self.add_income_button = tk.Button(self, text="Add Income", command=self.add_income, font=('Arial', 13),padx=20, pady=10)
        self.add_income_button.pack(side='top', anchor='e')

# Create the "Delete Expense" button
        self.delete_button = tk.Button(self, text="Delete Expense", command=self.delete_expense,font=('Arial', 13),padx=20, pady=10)
        self.delete_button.pack(side='top', anchor='e')

        self.investment_button = tk.Button(self, text="Investment Suggestions", command=self.open_investment_window,font=('Arial', 13),padx=20, pady=10)
        self.investment_button.pack()

        
        
        
        

        self.expense_history_treeview = ttk.Treeview(self, columns=("date", "description", "amount", "type"))

        self.expense_history_treeview.heading("date", text="Date")

        self.expense_history_treeview.heading("description", text="Description")
        self.expense_history_treeview.heading("amount", text="Amount")
        self.expense_history_treeview.heading("type", text="Type")
       
        self.expense_history_treeview.pack()
        
        self.refresh_expense_history()
    


    def open_investment_window(self):
        investment_window = tk.Toplevel(self)
        investment_window.title("Investment Suggestions")

        # add labels and links for gold prices and investment websites
        gold_label = tk.Label(investment_window, text="Gold Prices")
        gold_label.pack()
        gold_link = tk.Label(investment_window, text="https://www.goodreturns.in/gold-rates/mumbai.html", fg="blue", cursor="hand2")
        gold_link.pack()
        gold_link.bind("<Button-1>", lambda e: webbrowser.open_new(gold_link.cget("text")))

        investment_label = tk.Label(investment_window, text="Investment Websites")
        investment_label.pack()
        investment_link_1 = tk.Label(investment_window, text="https://www.etoro.com/", fg="blue", cursor="hand2")
        investment_link_1.pack()
        investment_link_1.bind("<Button-1>", lambda e: webbrowser.open_new(investment_link_1.cget("text")))

        investment_link_2 = tk.Label(investment_window, text="https://www.moneycontrol.com/stocksmarketsindia/", fg="blue", cursor="hand2")
        investment_link_2.pack()
        investment_link_2.bind("<Button-1>", lambda e: webbrowser.open_new(investment_link_2.cget("text")))

    def add_expense(self):
      date = self.date_label['text'] 
      description = self.expense_description_entry.get()
      amount = float(self.expense_amount_entry.get())
      
      if self.check_mo.get() == 1:
        expense_type = "Online"
      elif self.check_te.get() == 1:
        expense_type = "Cash"
      else:
        expense_type = ""

    # Add the expense to the list
      c.execute("INSERT INTO expenses (date, description, amount, expense_type, user) VALUES (?, ?, ?, ?, ?)",
          (date, description, amount, expense_type, self.user))

      conn.commit()

    # Clear the expense entry fields
      
      self.expense_description_entry.delete(0, tk.END)
      self.expense_amount_entry.delete(0, tk.END)
      self.check_mo.set(0)
      self.check_te.set(0)
      

    # Refresh the expense history
      self.refresh_expense_history()

    # Update the savings label
      self.update_income_savings(float(self.income_label.cget("text")[8:].lstrip("₹")))
    
    def add_income(self):
        # Create a dialog box to get the income from the user
        income_dialog = tk.Toplevel(self)
        tk.Label(income_dialog, text="Enter Income:").grid(row=0, column=0, padx=5, pady=5)
        income_entry = tk.Entry(income_dialog)
        income_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(income_dialog, text="OK", command=lambda: self.update_income_savings((float(income_entry.get()), 0))).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def update_income_savings(self, values):
    # Get the user's expenses from the entries
      income, savings = values
     

     
     # Get the user's expenses from the database
      c.execute("SELECT SUM(amount) FROM expenses WHERE user=? AND deleted=0", (self.user,))
      expenses = c.fetchone()[0] or 0

    # Calculate the savings
      savings = income - expenses

    # Update the user's income and savings values in the database
      c.execute('UPDATE expenses SET income = ?, savings = ? WHERE user = ?', (income, savings, self.user_info[2]))
      conn.commit()
      messagebox.showinfo("Success", "Income and savings updated successfully")
    # Update the income and savings labels
      self.income_label.config(text=f"Income: ₹{income:.2f}")
      self.savings_label.config(text=f"Savings: ₹{savings:.2f}")

    # Refresh the expense history
      self.refresh_expense_history()

    
      
    def refresh_expense_history(self):
       self.expense_history_treeview.delete(*self.expense_history_treeview.get_children())
       conn = sqlite3.connect("s.db")
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM expenses WHERE user=? AND deleted=0", (self.user,))
       rows = cursor.fetchall()
       for row in rows:
        
        self.expense_history_treeview.insert("", tk.END, text=row[0], values=(row[1], row[2], row[3], row[4]))
        
       conn.close()
    def schedule_date_update(self):
        # Get current time and calculate seconds until midnight
         now = datetime.datetime.now()
         tomorrow = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time.min)
         seconds_until_midnight = (tomorrow - now).seconds

        # Schedule date update to run every day at midnight
         threading.Timer(seconds_until_midnight, self.update_date).start()

    def update_date(self):
        today = date.today().strftime("%d/%m/%Y")
        self.date_label.config(text=today)

        # Schedule next date update
        self.schedule_date_update()

    def delete_expense(self):
     item = self.expense_history_treeview.selection()
     if item:
        result = messagebox.askyesno("Delete Expense", "Are you sure you want to delete this expense?")
        if result == tk.YES:
            expense_id = int(self.expense_history_treeview.item(item)['text'])
            conn = sqlite3.connect("s.db")
            cursor = conn.cursor()
            cursor.execute("SELECT amount FROM expenses WHERE id=?", (expense_id,))
            expense_amount = cursor.fetchone()[0]
            cursor.execute("UPDATE expenses SET deleted=1 WHERE id=?", (expense_id,))
            conn.commit()
            conn.close()
            self.refresh_expense_history()
            conn = sqlite3.connect("s.db")
            cursor = conn.cursor()
            cursor.execute("SELECT MIN(id) FROM expenses WHERE id > 0 AND deleted=0")
            min_id = cursor.fetchone()[0]
            self.id = min_id if min_id is not None else 1
            conn.close()

            # Update savings label
            income = float(self.income_label.cget("text")[8:].lstrip("$"))
            savings = float(self.savings_label.cget("text")[10:].lstrip("$")) + expense_amount
            self.update_income_savings((income, savings))


def login_success():
    pass
    # user_info = {"name": "John Doe", "email": "johndoe@example.com"}
    # expense_page = ExpensePage(root, user_info)
    expense_page = WelcomePage(root, "admin")
    expense_page.grid(row=0, column=0)

root = tk.Tk()
root.title("Expense Tracker")

login_page =LoginPage(root, login_success)
login_page.grid(row=0, column=0)

root.mainloop()
#no this does not work user income and saving label is empty when we logged in