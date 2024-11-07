import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect('study_scheduler.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        major TEXT)''')
    conn.commit()
    conn.close()

# Main Application Class
class StudySchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Scheduler App")
        self.root.geometry("400x300")
        self.root.configure(bg="#0A1C28")  # Background color to match the dark theme
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.major = tk.StringVar()
        
        # Predefined major options
        self.major_options = ["IT", "Business", "IR", "Engineering", "Science"]
        self.show_login_screen()
        
    def show_login_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create a frame for centering
        frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Login UI
        tk.Label(frame, text="Log in", font=("Arial", 18, "bold"), bg="white").pack(pady=(0, 10))
        tk.Label(frame, text="Username", bg="white").pack(anchor="w")
        tk.Entry(frame, textvariable=self.username, font=("Arial", 12)).pack(fill="x", pady=(0, 10))

        tk.Label(frame, text="Password", bg="white").pack(anchor="w")
        tk.Entry(frame, textvariable=self.password, show="*", font=("Arial", 12)).pack(fill="x", pady=(0, 10))

        tk.Button(frame, text="Log in", command=self.login, bg="#00BCD4", fg="white", font=("Arial", 12), padx=10, pady=5).pack(fill="x", pady=(10, 5))
        tk.Label(frame, text="or,", bg="white").pack()
        tk.Button(frame, text="Sign up", command=self.show_signup_screen, bg="white", fg="#00BCD4", font=("Arial", 12, "underline"), bd=0).pack(pady=5)
        
    def show_signup_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Signup UI
        frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Sign Up", font=("Arial", 18, "bold"), bg="white").pack(pady=(0, 10))
        tk.Label(frame, text="Username", bg="white").pack(anchor="w")
        tk.Entry(frame, textvariable=self.username, font=("Arial", 12)).pack(fill="x", pady=(0, 10))

        tk.Label(frame, text="Password", bg="white").pack(anchor="w")
        tk.Entry(frame, textvariable=self.password, show="*", font=("Arial", 12)).pack(fill="x", pady=(0, 10))

        tk.Label(frame, text="Major", bg="white").pack(anchor="w")
        major_dropdown = tk.OptionMenu(frame, self.major, *self.major_options)
        major_dropdown.config(width=15, font=("Arial", 12))
        major_dropdown.pack(fill="x", pady=(0, 10))

        tk.Button(frame, text="Register", command=self.register, bg="#00BCD4", fg="white", font=("Arial", 12), padx=10, pady=5).pack(fill="x", pady=(10, 5))
        tk.Button(frame, text="Back to Login", command=self.show_login_screen, bg="white", fg="#00BCD4", font=("Arial", 12, "underline"), bd=0).pack(pady=5)
        
    def login(self):
        username = self.username.get()
        password = self.password.get()
        
        conn = sqlite3.connect('study_scheduler.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            messagebox.showinfo("Login Successful", f"Welcome {username}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
    
    def register(self):
        username = self.username.get()
        password = self.password.get()
        major = self.major.get()
        
        if not major:
            messagebox.showerror("Error", "Please select a major.")
            return
        
        conn = sqlite3.connect('study_scheduler.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Users (username, password, major) VALUES (?, ?, ?)", (username, password, major))
            conn.commit()
            messagebox.showinfo("Registration Successful", "You can now log in.")
            self.show_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            conn.close()
    
    def show_dashboard(self):
        # Clear the window and show main dashboard (for future features)
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Dashboard", font=("Arial", 16)).pack()
        tk.Label(self.root, text="Welcome to your study scheduler!").pack()
    
# Run the App
if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = StudySchedulerApp(root)
    root.mainloop()
