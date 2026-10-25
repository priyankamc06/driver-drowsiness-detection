import tkinter as tk
from tkinter import messagebox
import sqlite3

# ---------- FUNCTIONS ----------

def add_user():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user_entry.get(), pass_entry.get())
        )
        conn.commit()
        messagebox.showinfo("Success", "User added!")
    except:
        messagebox.showerror("Error", "Username already exists")
    conn.close()

def view_users():
    from tkinter import ttk
    import sqlite3

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # ✅ get all required columns
    cursor.execute("SELECT id, username, password, login_time, login_date FROM users")
    data = cursor.fetchall()
    conn.close()

    # Window
    view_window = tk.Toplevel()
    view_window.title("All Users")
    view_window.geometry("700x400")
    view_window.configure(bg="#0f172a")

    # Frame
    frame = tk.Frame(view_window, bg="#1e293b")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=650, height=300)

    # Style
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
                    background="#1e293b",
                    foreground="white",
                    rowheight=28,
                    fieldbackground="#1e293b",
                    font=("Arial", 10))

    style.configure("Treeview.Heading",
                    background="#3b82f6",
                    foreground="white",
                    font=("Arial", 11, "bold"))

    style.map("Treeview",
              background=[("selected", "#2563eb")])

    # ✅ Updated table (5 columns)
    tree = ttk.Treeview(frame,
        columns=("ID", "Username", "Password", "Time", "Date"),
        show="headings")

    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")
    tree.heading("Time", text="Time")
    tree.heading("Date", text="Date")

    tree.column("ID", width=50, anchor="center")
    tree.column("Username", width=150, anchor="center")
    tree.column("Password", width=120, anchor="center")
    tree.column("Time", width=120, anchor="center")
    tree.column("Date", width=120, anchor="center")

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # ✅ Insert data (hide password)
    for row in data:
        id_, user, pwd, time, date = row
        tree.insert("", tk.END,
                    values=(id_, user, "*"*len(pwd), time, date))


def update_user():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET password=? WHERE username=?",
        (pass_entry.get(), user_entry.get())
    )
    conn.commit()

    if cursor.rowcount == 0:
        messagebox.showerror("Error", "User not found!")
    else:
        messagebox.showinfo("Success", "Password updated!")

    conn.close()


def delete_user():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE username=?",
        (user_entry.get(),)
    )
    conn.commit()

    if cursor.rowcount == 0:
        messagebox.showerror("Error", "User not found!")
    else:
        messagebox.showinfo("Success", "User deleted!")

    conn.close()


root = tk.Tk()
root.title("Admin Dashboard")
root.state("zoomed")
root.configure(bg="#0f172a")

# ---------- MAIN CARD ----------
card = tk.Frame(root, bg="#1e293b")
card.place(relx=0.5, rely=0.5, anchor="center", width=700, height=520)

# ---------- TITLE ----------
tk.Label(card,
         text="Admin Dashboard",
         font=("Arial", 24, "bold"),
         bg="#1e293b",
         fg="white").pack(pady=20)

tk.Label(card,
         text="Manage Users & Monitor System",
         font=("Arial", 11),
         bg="#1e293b",
         fg="#94a3b8").pack()

# ---------- INPUTS ----------
tk.Label(card, text="Username",
         bg="#1e293b", fg="white",
         font=("Arial", 11)).pack(pady=(20, 5))

user_entry = tk.Entry(card, font=("Arial", 12), width=30)
user_entry.pack(ipady=6)

tk.Label(card, text="Password",
         bg="#1e293b", fg="white",
         font=("Arial", 11)).pack(pady=(15, 5))

pass_entry = tk.Entry(card, font=("Arial", 12), width=30)
pass_entry.pack(ipady=6)

# ---------- BUTTON GRID ----------
btn_frame = tk.Frame(card, bg="#1e293b")
btn_frame.pack(pady=30)

tk.Button(btn_frame,
          text="➕ Add User",
          width=20, height=2,
          bg="#22c55e",
          fg="white",
          font=("Arial", 11, "bold"),
          command=add_user).grid(row=0, column=0, padx=10, pady=10)

tk.Button(btn_frame,
          text="👥 View Users",
          width=20, height=2,
          bg="#3b82f6",
          fg="white",
          font=("Arial", 11, "bold"),
          command=view_users).grid(row=0, column=1, padx=10, pady=10)

tk.Button(btn_frame,
          text="🔑 Update Password",
          width=20, height=2,
          bg="#f59e0b",
          fg="white",
          font=("Arial", 11, "bold"),
          command=update_user).grid(row=1, column=0, padx=10, pady=10)

tk.Button(btn_frame,
          text="🗑 Delete User",
          width=20, height=2,
          bg="#ef4444",
          fg="white",
          font=("Arial", 11, "bold"),
          command=delete_user).grid(row=1, column=1, padx=10, pady=10)

# ---------- LOGOUT ----------
def go_back():
    root.destroy()
    import mini_project
    mini_project.select_role()

tk.Button(card,
          text="⎋ Logout",
          width=25,
          height=2,
          bg="#64748b",
          fg="white",
          font=("Arial", 11, "bold"),
          command=go_back).pack(pady=10)

root.mainloop()