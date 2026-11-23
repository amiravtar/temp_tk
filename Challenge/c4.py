
import tkinter as tk
from tkinter import messagebox


def add_task():
    title = task_entry.get().strip()

    if not title:
        messagebox.showwarning("Warning", "Enter a task title")
        return

    task_list.insert(tk.END, title)
    task_entry.delete(0, tk.END)


def delete_task():
    selection = task_list.curselection()

    if not selection:
        messagebox.showwarning("Warning", "Select a task")
        return

    task_list.delete(selection[0])


# Main window
root = tk.Tk()
root.title("To-Do List")
root.geometry("600x400")
root.minsize(400, 300)

# Header
header = tk.Frame(root)
header.pack(fill="x", padx=10, pady=10)

tk.Label(
    header,
    text="My To-Do List",
    font=("Arial", 18, "bold")
).pack()

# Input section
input_frame = tk.Frame(root)
input_frame.pack(fill="x", padx=10, pady=5)

task_entry = tk.Entry(input_frame)
task_entry.pack(side="left", fill="x", expand=True)

tk.Button(
    input_frame,
    text="Add",
    command=add_task
).pack(side="left", padx=5)

# Task list
task_list = tk.Listbox(root)
task_list.pack(fill="both", expand=True, padx=10, pady=5)

# Actions
actions = tk.Frame(root)
actions.pack(fill="x", padx=10, pady=10)

tk.Button(
    actions,
    text="Delete Selected",
    command=delete_task
).pack(side="left")

# Start application
root.mainloop()
