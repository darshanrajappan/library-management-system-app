import mysql.connector
from tkinter import *
from tkinter import messagebox, Toplevel
from tkinter import ttk
from datetime import date

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vision1215@Mysql",
    database="library_db"
)

cursor = db.cursor()

# Function to toggle between dark and light mode
def toggle_theme():
    if root['bg'] == 'white':
        # Switch to dark mode
        root.config(bg='#2e2e2e')
        for widget in root.winfo_children():
            widget.config(bg='#2e2e2e', fg='white')
    else:
        # Switch to light mode
        root.config(bg='white')
        for widget in root.winfo_children():
            widget.config(bg='white', fg='black')

# Create common styled button function
def create_button(parent, text, command):
    return Button(parent, text=text, command=command, width=20, font=("Arial", 12), bg="#4CAF50", fg="white", activebackground="#45a049", relief=RAISED, padx=10, pady=10)

# Functions for dialog box actions
def open_add_book_dialog():
    dialog = Toplevel()
    dialog.title("Add Book")
    dialog.state("zoomed")
    dialog.configure(bg='white')

    Label(dialog, text="Title", font=("Arial", 12), bg='white').pack(pady=10)
    book_title_entry = Entry(dialog, font=("Arial", 12), width=30)
    book_title_entry.pack()

    Label(dialog, text="Author", font=("Arial", 12), bg='white').pack(pady=10)
    book_author_entry = Entry(dialog, font=("Arial", 12), width=30)
    book_author_entry.pack()

    Label(dialog, text="Quantity", font=("Arial", 12), bg='white').pack(pady=10)
    book_quantity_entry = Entry(dialog, font=("Arial", 12), width=30)
    book_quantity_entry.pack()

    def add_book():
        title = book_title_entry.get()
        author = book_author_entry.get()
        quantity = book_quantity_entry.get()

        if title and author and quantity:
            try:
                cursor.execute("INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)", (title, author, quantity))
                db.commit()
                messagebox.showinfo("Success", "Book added successfully!")
                dialog.destroy()  # Close the dialog after adding the book
            except Exception as e:
                messagebox.showerror("Error", f"Error adding book: {str(e)}")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")
    
    Button(dialog, text="Add Book", command=add_book, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)

def open_add_member_dialog():
    dialog = Toplevel()
    dialog.title("Add Member")
    dialog.state("zoomed")
    dialog.configure(bg='white')

    Label(dialog, text="Name", font=("Arial", 12), bg='white').pack(pady=10)
    member_name_entry = Entry(dialog, font=("Arial", 12), width=30)
    member_name_entry.pack()

    Label(dialog, text="Contact", font=("Arial", 12), bg='white').pack(pady=10)
    member_contact_entry = Entry(dialog, font=("Arial", 12), width=30)
    member_contact_entry.pack()

    def add_member():
        name = member_name_entry.get()
        contact = member_contact_entry.get()

        if name and contact:
            try:
                cursor.execute("INSERT INTO members (name, contact) VALUES (%s, %s)", (name, contact))
                db.commit()
                messagebox.showinfo("Success", "Member added successfully!")
                dialog.destroy()  # Close the dialog after adding the member
            except Exception as e:
                messagebox.showerror("Error", f"Error adding member: {str(e)}")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")
    
    Button(dialog, text="Add Member", command=add_member, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)

def open_issue_book_dialog():
    dialog = Toplevel()
    dialog.title("Issue Book")
    dialog.state("zoomed")
    dialog.configure(bg='white')

    Label(dialog, text="Book ID", font=("Arial", 12), bg='white').pack(pady=10)
    issue_book_id_entry = Entry(dialog, font=("Arial", 12), width=30)
    issue_book_id_entry.pack()

    Label(dialog, text="Member ID", font=("Arial", 12), bg='white').pack(pady=10)
    issue_member_id_entry = Entry(dialog, font=("Arial", 12), width=30)
    issue_member_id_entry.pack()

    def issue_book():
        book_id = issue_book_id_entry.get()
        member_id = issue_member_id_entry.get()
        issue_date = date.today()

        if book_id and member_id:
            try:
                # Check if the book is available
                cursor.execute("SELECT quantity FROM books WHERE book_id = %s", (book_id,))
                book = cursor.fetchone()
                if book and book[0] > 0:
                    # Update book quantity and add transaction
                    cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = %s", (book_id,))
                    cursor.execute("INSERT INTO transactions (book_id, member_id, issue_date) VALUES (%s, %s, %s)", (book_id, member_id, issue_date))
                    db.commit()
                    messagebox.showinfo("Success", "Book issued successfully!")
                    dialog.destroy()  # Close the dialog after issuing the book
                else:
                    messagebox.showwarning("Unavailable", "Book not available or invalid book ID.")
            except Exception as e:
                messagebox.showerror("Error", f"Error issuing book: {str(e)}")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")
    
    Button(dialog, text="Issue Book", command=issue_book, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)

def open_return_book_dialog():
    dialog = Toplevel()
    dialog.title("Return Book")
    dialog.state("zoomed")
    dialog.configure(bg='white')

    Label(dialog, text="Transaction ID", font=("Arial", 12), bg='white').pack(pady=10)
    return_transaction_id_entry = Entry(dialog, font=("Arial", 12), width=30)
    return_transaction_id_entry.pack()

    def return_book():
        transaction_id = return_transaction_id_entry.get()
        return_date = date.today()

        if transaction_id:
            try:
                # Check if the transaction exists
                cursor.execute("SELECT book_id FROM transactions WHERE transaction_id = %s", (transaction_id,))
                transaction = cursor.fetchone()
                if transaction:
                    book_id = transaction[0]
                    # Update book quantity and transaction return date
                    cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id = %s", (book_id,))
                    cursor.execute("UPDATE transactions SET return_date = %s WHERE transaction_id = %s", (return_date, transaction_id))
                    db.commit()
                    messagebox.showinfo("Success", "Book returned successfully!")
                    dialog.destroy()  # Close the dialog after returning the book
                else:
                    messagebox.showwarning("Invalid", "Transaction not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Error returning book: {str(e)}")
        else:
            messagebox.showwarning("Input Error", "Please fill the transaction ID.")
    
    Button(dialog, text="Return Book", command=return_book, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)

def open_search_books_dialog():
    dialog = Toplevel()
    dialog.title("Search Books")
    dialog.state("zoomed")
    dialog.configure(bg='white')

    Label(dialog, text="Search by Title or Author", font=("Arial", 12), bg='white').pack(pady=10)
    search_entry = Entry(dialog, font=("Arial", 12), width=30)
    search_entry.pack()

    listbox = Listbox(dialog, width=50, height=10, font=("Arial", 12))
    listbox.pack(padx=10, pady=10, fill=BOTH, expand=True)

    def search_books():
        search_term = search_entry.get()
        if search_term:
            try:
                cursor.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s", 
                               ('%' + search_term + '%', '%' + search_term + '%'))
                books = cursor.fetchall()
                listbox.delete(0, END)  # Clear previous search results
                if books:
                    for book in books:
                        listbox.insert(END, f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Qty: {book[3]}")
                else:
                    listbox.insert(END, "No books found.")
            except Exception as e:
                messagebox.showerror("Error", f"Error searching books: {str(e)}")
        else:
            messagebox.showwarning("Input Error", "Please enter a search term.")

    Button(dialog, text="Search", command=search_books, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)

def open_search_members_dialog():
    dialog = Toplevel()
    dialog.title("Search Members")
    dialog.state("zoomed")
    dialog.configure(bg='white')

    Label(dialog, text="Search by Name", font=("Arial", 12), bg='white').pack(pady=10)
    search_entry = Entry(dialog, font=("Arial", 12), width=30)
    search_entry.pack()

    listbox = Listbox(dialog, width=50, height=10, font=("Arial", 12))
    listbox.pack(padx=10, pady=10, fill=BOTH, expand=True)

    def search_members():
        search_term = search_entry.get()
        if search_term:
            try:
                cursor.execute("SELECT * FROM members WHERE name LIKE %s", ('%' + search_term + '%',))
                members = cursor.fetchall()
                listbox.delete(0, END)  # Clear previous search results
                if members:
                    for member in members:
                        listbox.insert(END, f"ID: {member[0]}, Name: {member[1]}, Contact: {member[2]}")
                else:
                    listbox.insert(END, "No members found.")
            except Exception as e:
                messagebox.showerror("Error", f"Error searching members: {str(e)}")
        else:
            messagebox.showwarning("Input Error", "Please enter a search term.")

    Button(dialog, text="Search", command=search_members, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)

def open_view_all_books_dialog():
    dialog = Toplevel()
    dialog.title("All Books")
    dialog.state("zoomed")
    dialog.configure(bg='white')

    listbox = Listbox(dialog, width=50, height=15, font=("Arial", 12))
    listbox.pack(padx=10, pady=10, fill=BOTH, expand=True)

    try:
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        for book in books:
            listbox.insert(END, f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Qty: {book[3]}")
    except Exception as e:
        messagebox.showerror("Error", f"Error retrieving books: {str(e)}")

def open_view_all_members_dialog():
    dialog = Toplevel()
    dialog.title("All Members")
    dialog.state("zoomed")
    dialog.configure(bg='white')

    listbox = Listbox(dialog, width=50, height=15, font=("Arial", 12))
    listbox.pack(padx=10, pady=10, fill=BOTH, expand=True)

    try:
        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()
        for member in members:
            listbox.insert(END, f"ID: {member[0]}, Name: {member[1]}, Contact: {member[2]}")
    except Exception as e:
        messagebox.showerror("Error", f"Error retrieving members: {str(e)}")

def check_late_returns():
    dialog = Toplevel()
    dialog.title("Late Returns")
    dialog.state("zoomed")
    dialog.configure(bg='white')

    listbox = Listbox(dialog, width=50, height=15, font=("Arial", 12))
    listbox.pack(padx=10, pady=10, fill=BOTH, expand=True)

    try:
        # Check for books issued more than 14 days ago and not returned
        cursor.execute("SELECT * FROM transactions WHERE return_date IS NULL AND issue_date < CURDATE() - INTERVAL 14 DAY")
        late_returns = cursor.fetchall()
        if late_returns:
            for transaction in late_returns:
                cursor.execute("SELECT title FROM books WHERE book_id = %s", (transaction[1],))
                book_title = cursor.fetchone()[0]
                cursor.execute("SELECT name FROM members WHERE member_id = %s", (transaction[2],))
                member_name = cursor.fetchone()[0]
                listbox.insert(END, f"Book: {book_title}, Member: {member_name}, Issue Date: {transaction[3]}")
        else:
            listbox.insert(END, "No late returns.")
    except Exception as e:
        messagebox.showerror("Error", f"Error checking late returns: {str(e)}")

def open_transaction_history_dialog():
    dialog = Toplevel()
    dialog.title("Transaction History")
    dialog.state("zoomed")
    dialog.configure(bg='white')

    listbox = Listbox(dialog, width=70, height=15, font=("Arial", 12))
    listbox.pack(padx=10, pady=10, fill=BOTH, expand=True)

    try:
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
        for transaction in transactions:
            cursor.execute("SELECT title FROM books WHERE book_id = %s", (transaction[1],))
            book_title = cursor.fetchone()[0]
            cursor.execute("SELECT name FROM members WHERE member_id = %s", (transaction[2],))
            member_name = cursor.fetchone()[0]
            return_date = transaction[4] if transaction[4] else "Not Returned"
            listbox.insert(END, f"Book: {book_title}, Member: {member_name}, Issue: {transaction[3]}, Return: {return_date}")
    except Exception as e:
        messagebox.showerror("Error", f"Error retrieving transactions: {str(e)}")



# Main UI Setup with Tkinter
root = Tk()
root.title("Library Management System")
# Set window to according screen size
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.config(bg='white')

Label(root, text="Library Management System", font=("Arial", 20, "bold"), bg="white", fg="black").pack(pady=20)

# Add buttons
frame = Frame(root, bg="white")
frame.pack(pady=20)

# Add the main action buttons
create_button(frame, "Add Book", open_add_book_dialog).grid(row=0, column=0, padx=10, pady=10)
create_button(frame, "Add Member", open_add_member_dialog).grid(row=0, column=1, padx=10, pady=10)
create_button(frame, "Issue Book", open_issue_book_dialog).grid(row=1, column=0, padx=10, pady=10)
create_button(frame, "Return Book", open_return_book_dialog).grid(row=1, column=1, padx=10, pady=10)
create_button(frame, "Search Books", open_search_books_dialog).grid(row=2, column=0, padx=10, pady=10)
create_button(frame, "Search Members", open_search_members_dialog).grid(row=2, column=1, padx=10, pady=10)
create_button(frame, "View All Books", open_view_all_books_dialog).grid(row=3, column=0, padx=10, pady=10)
create_button(frame, "View All Members", open_view_all_members_dialog).grid(row=3, column=1, padx=10, pady=10)
create_button(frame, "Check Late Returns", check_late_returns).grid(row=4, column=0, padx=10, pady=10)
create_button(frame, "Transaction History", open_transaction_history_dialog).grid(row=4, column=1, padx=10, pady=10)
Button(root, text="Toggle Theme", command=toggle_theme, font=("Arial", 20, "bold"), bg="white", fg="black").pack(pady=10)

root.mainloop()
