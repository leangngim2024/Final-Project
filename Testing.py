import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import customtkinter
from ttkbootstrap import Style
import hashlib

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("notes_app.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
                    user TEXT,
                    title TEXT,
                    content TEXT,
                    FOREIGN KEY (user) REFERENCES users(username))''')
conn.commit()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Save user to the database
def save_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

# Verify user login
def verify_user(username, password):
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row and row[0] == password:
        return True
    return False

# Save notes to the database
def save_note_to_db(user, title, content):
    cursor.execute("INSERT OR REPLACE INTO notes (user, title, content) VALUES (?, ?, ?)", (user, title, content))
    conn.commit()

# Load notes from the database for a specific user
def load_notes_from_db(user):
    cursor.execute("SELECT title, content FROM notes WHERE user = ?", (user,))
    return {title: content for title, content in cursor.fetchall()}

# Delete note from the database
def delete_note_from_db(user, title):
    cursor.execute("DELETE FROM notes WHERE user = ? AND title = ?", (user, title))
    conn.commit()

# Create the main application window
root = tk.Tk()
root.title("OneNote")
root.geometry("600x600")
customtkinter.set_appearance_mode("Dark")
style = Style(theme='darkly') # 'darkly or journal'

# Global variables
logged_in_user = None
notes = {}

def startup_screen():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Create startup screen UI

    startup_frame = tk.Frame(root)
    startup_frame.pack(expand=True)

    welcome_label = tk.Label(startup_frame, text="Welcome to OneNote", font=("Times New Roman", 30))
    welcome_label.pack(pady=30)

    login_button = tk.Button(startup_frame, text=" Login  ", command=login_screen, font=("Times New Roman", 20))
    login_button.pack(pady=20)

    signup_button = tk.Button(startup_frame, text="Sign Up", command=signup_screen, font=("Times New Roman", 20))
    signup_button.pack(pady=10)

    intro_label = tk.Label(startup_frame, anchor = "center", font=("Times New Roman", 14), text="You must create a private account before reaching your bookmarks.")
    intro_label.pack(pady=30)

def login_screen():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Login UI
    login_frame = tk.Frame(root)
    login_frame.pack(pady=50)

    tk.Label(login_frame, font=("Times New Roman", 20), text="Username").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(login_frame, font=("Times New Roman", 20))
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(login_frame, font=("Times New Roman", 20), text="Password").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(login_frame, font=("Times New Roman", 20), show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)


    tk.Label(login_frame, anchor = "center", font=("Times New Roman", 14), text="Enter your username and password.").grid(row=5, column=0, pady=10, columnspan=2)
    tk.Label(login_frame, anchor = "center", font=("Times New Roman", 14), text="Password must be at least 6 characters.").grid(row=6, column=0, pady=5, columnspan=2)

    def login():
        username = username_entry.get()
        password = hash_password(password_entry.get())
        if verify_user(username, password):
            global logged_in_user
            logged_in_user = username
            main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    tk.Button(login_frame, text="Login", command=login,font=("Times New Roman", 12)).grid(row=2, column=1, pady=20)
    tk.Button(login_frame, text="Back to Your Start", command=startup_screen, font=("Times New Roman", 12)).grid(row=3, column=1, pady=5)

def signup_screen():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Signup UI
    signup_frame = tk.Frame(root)
    signup_frame.pack(pady=50)

    tk.Label(signup_frame, text="Username", font=("Times New Roman", 20)).grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(signup_frame, font=("Times New Roman", 20))
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(signup_frame, text="Password", font=("Times New Roman", 20)).grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(signup_frame, show="*", font=("Times New Roman", 20))
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(signup_frame, anchor = "center", font=("Times New Roman", 14), text="Create a new username and password before allowing to login.").grid(row=5, column=0, pady=10, columnspan=2)
    tk.Label(signup_frame, anchor = "center", font=("Times New Roman", 14), text="Password must be at least 6 characters.").grid(row=6, column=0, pady=5, columnspan=2)


    def signup():
        username = username_entry.get()
        password = password_entry.get()
        save_user(username, hash_password(password))
        messagebox.showinfo("Success", "Account created successfully!")
        login_screen()

    tk.Button(signup_frame, text="Sign Up", command=signup, font=("Times New Roman", 12)).grid(row=2, column=1, pady=10)
    tk.Button(signup_frame, text="Back to Your Start", command=startup_screen, font=("Times New Roman", 12)).grid(row=3, column=1, pady=10)

def main_screen():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Create the notebook to hold the notes
    notebook = ttk.Notebook(root, style="TNotebook")
    notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Function to add a new note
    def add_note():
        note_frame = ttk.Frame(notebook, padding=10)
        notebook.add(note_frame, text="New Note")

        title_label = ttk.Label(note_frame, text="Title of your Note:", font=("Times New Roman", 12))
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
        title_entry = ttk.Entry(note_frame, width=50, background="White")
        title_entry.grid(row=0, column=1, padx=10, pady=10)

        content_label = ttk.Label(note_frame, text="Text Your Note:", font=("Times New Roman", 12))
        content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")
        content_entry = tk.Text(note_frame, wrap="word", height=10, width=40)
        content_entry.grid(row=1, column=1, padx=10, pady=10)

        infor_label = ttk.Label(note_frame,text="\tThe Purpose\n\n\nThis note app is a versatile tool that can\nsimplify information management,\n boost productivity, support learning,\nand help users stay organized in all areas of their lives.", font=("Times New Roman", 16))
        infor_label.grid(row=1, column=5, padx=10, pady=10, sticky="E")

        # Function to save the note
        def save_note():
            title = title_entry.get()
            content = content_entry.get("1.0", tk.END).strip()
            if title:
                notes[title] = content
                save_note_to_db(logged_in_user, title, content)
                notebook.tab(note_frame, text=title)
            else:
                messagebox.showwarning("Warning", "The Title cannot be empty.")

        ttk.Button(note_frame, text="Save My Note", command=save_note).grid(row=5, column=1, padx=10, pady=10)

        # Function to apply font and size directly when a selection is made
        def update_font(event=None):
            selected_font = font_combobox.get()
            selected_size = size_combobox.get()
            content_entry.config(font=(selected_font, selected_size))

        # Function to apply color directly when a selection is made
        def update_color(event=None):
            color = color_combobox.get()
            content_entry.tag_configure("color", foreground=color)
            try:
                content_entry.tag_add("color", "sel.first", "sel.last")
            except tk.TclError:
                pass  # If no text is selected, skip applying color

        # Dropdown for font kind with direct change on selection
        font_choices = ["Arial", "Times New Roman", "Courier New", "Helvetica", "Comic Sans MS"]
        font_combobox = ttk.Combobox(note_frame, values=font_choices, state="readonly", width=20)
        font_combobox.set("Times New Roman")  # Default font
        font_combobox.grid(row=2, column=0, padx=10, pady=10)
        font_combobox.bind("<<ComboboxSelected>>", update_font)

        # Dropdown for font size with direct change on selection
        size_choices = [str(i) for i in range(8, 30)]
        size_combobox = ttk.Combobox(note_frame, values=size_choices, state="readonly", width=5)
        size_combobox.set("12")  # Default size
        size_combobox.grid(row=2, column=1, padx=10, pady=10)
        size_combobox.bind("<<ComboboxSelected>>", update_font)

        # Dropdown for text color with direct change on selection
        color_choices = ["black", "red", "green", "blue", "purple", "orange"]
        color_combobox = ttk.Combobox(note_frame, values=color_choices, state="readonly", width=10)
        color_combobox.set("black")  # Default color
        color_combobox.grid(row=2, column=2, padx=10, pady=10)
        color_combobox.bind("<<ComboboxSelected>>", update_color)

    # Function to delete a note
    def delete_note():
        current_tab = notebook.index(notebook.select())
        note_title = notebook.tab(current_tab, "text")
        confirm = messagebox.askyesno("Delete Note", f"Are you sure you want to delete '{note_title}'?")
        if confirm:
            notebook.forget(current_tab)
            notes.pop(note_title, None)
            delete_note_from_db(logged_in_user, note_title)

    # Load saved notes
    global notes
    notes = load_notes_from_db(logged_in_user)
    for title, content in notes.items():
        note_frame = ttk.Frame(notebook, padding=10)
        notebook.add(note_frame, text=title)

        title_label = ttk.Label(note_frame, text="Title of your Note:", font=("Times New Roman", 14))
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
        title_entry = ttk.Entry(note_frame, width=40)
        title_entry.grid(row=0, column=1, padx=10, pady=10)
        title_entry.insert(0, title)

        content_label = ttk.Label(note_frame, text="Text Your Note:")
        content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")
        content_entry = tk.Text(note_frame, width=40, height=10)
        content_entry.grid(row=1, column=1, padx=10, pady=10)
        content_entry.insert(tk.END, content)

    # Add buttons to the main window
    ttk.Button(root, text="Add New Note", command=add_note).pack(side=tk.LEFT, padx=10, pady=10)
    ttk.Button(root, text="Delete", command=delete_note).pack(side=tk.LEFT, padx=10, pady=10)

# Show the startup screen initially
startup_screen()
root.mainloop()

# Close the database connection when the application ends
conn.close()
