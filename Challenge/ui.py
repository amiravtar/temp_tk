
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import tkinter.font as tkFont


class CrudWindow(tk.Toplevel):
    """Window for creating and editing tasks."""

    def __init__(self, parent, on_save, task=None):
        super().__init__(parent)

        self.on_save = on_save
        self.task = task

        self.title("Edit Task" if task else "New Task")
        self.geometry("380x330")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.create_widgets()

        if task:
            self.load_task()

    def create_widgets(self):
        form = ttk.Frame(self, padding=20)
        form.pack(fill="both", expand=True)

        # Title
        ttk.Label(form, text="Task Title").pack(anchor="w")
        self.title_entry = ttk.Entry(form)
        self.title_entry.pack(fill="x", pady=(5, 12))

        # Priority
        ttk.Label(form, text="Priority").pack(anchor="w")
        self.priority_var = tk.StringVar(value="Medium")

        ttk.Combobox(
            form,
            textvariable=self.priority_var,
            values=["High", "Medium", "Low"],
            state="readonly"
        ).pack(fill="x", pady=(5, 12))

        # Due date
        ttk.Label(form, text="Due Date (YYYY-MM-DD)").pack(anchor="w")
        self.date_entry = ttk.Entry(form)
        self.date_entry.pack(fill="x", pady=(5, 12))

        # Status
        ttk.Label(form, text="Status").pack(anchor="w")
        self.status_var = tk.StringVar(value="Pending")

        ttk.Combobox(
            form,
            textvariable=self.status_var,
            values=["Pending", "Completed"],
            state="readonly"
        ).pack(fill="x", pady=(5, 15))

        # Actions
        actions = ttk.Frame(form)
        actions.pack(fill="x")

        ttk.Button(
            actions,
            text="Cancel",
            command=self.destroy
        ).pack(side="right", padx=(5, 0))

        ttk.Button(
            actions,
            text="Save",
            command=self.save_task
        ).pack(side="right")

        self.title_entry.focus()

    def load_task(self):
        self.title_entry.insert(0, self.task["title"])
        self.priority_var.set(self.task["priority"])
        self.date_entry.insert(0, self.task["due_date"])
        self.status_var.set(self.task["status"])

    def save_task(self):
        title = self.title_entry.get().strip()
        due_date = self.date_entry.get().strip()

        if not title:
            messagebox.showwarning(
                "Validation",
                "Task title is required.",
                parent=self
            )
            return

        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning(
                    "Validation",
                    "Date must use YYYY-MM-DD format.",
                    parent=self
                )
                return

        task_data = {
            "title": title,
            "priority": self.priority_var.get(),
            "due_date": due_date,
            "status": self.status_var.get()
        }

        self.on_save(task_data)
        self.destroy()


class ToDoApp:
    """Main application window."""

    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("750x500")
        self.root.minsize(600, 400)

        # Temporary in-memory storage
        self.tasks = []
        self.next_id = 1

        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        # Header
        header = ttk.Frame(self.root, padding=15)
        header.pack(fill="x")

        ttk.Label(
            header,
            text="My To-Do List",
            font=("Arial", 20, "bold")
        ).pack(side="left")

        self.clock_label = ttk.Label(header)
        self.clock_label.pack(side="right")

        # Toolbar
        toolbar = ttk.Frame(self.root, padding=(15, 5))
        toolbar.pack(fill="x")

        ttk.Button(
            toolbar,
            text="Add Task",
            command=self.add_task
        ).pack(side="left", padx=(0, 5))

        ttk.Button(
            toolbar,
            text="Edit Task",
            command=self.edit_task
        ).pack(side="left", padx=5)

        ttk.Button(
            toolbar,
            text="Delete Task",
            command=self.delete_task
        ).pack(side="left", padx=5)

        # Task table
        table_frame = ttk.Frame(self.root, padding=15)
        table_frame.pack(fill="both", expand=True)

        columns = ("title", "priority", "due_date", "status")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading("title", text="Task")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("due_date", text="Due Date")
        self.tree.heading("status", text="Status")

        self.tree.column("title", width=280)
        self.tree.column("priority", width=100)
        self.tree.column("due_date", width=130)
        self.tree.column("status", width=100)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Footer
        self.count_label = ttk.Label(
            self.root,
            text="Total tasks: 0",
            padding=15
        )
        self.count_label.pack(anchor="w")

    def add_task(self):
        CrudWindow(
            self.root,
            on_save=self.create_task
        )

    def create_task(self, task_data):
        task_data["id"] = self.next_id
        self.next_id += 1

        self.tasks.append(task_data)
        self.refresh_tasks()

    def edit_task(self):
        task_id = self.get_selected_id()

        if task_id is None:
            return

        task = self.find_task(task_id)

        CrudWindow(
            self.root,
            on_save=lambda data: self.update_task(task_id, data),
            task=task
        )

    def update_task(self, task_id, task_data):
        task = self.find_task(task_id)

        if task:
            task.update(task_data)
            self.refresh_tasks()

    def delete_task(self):
        task_id = self.get_selected_id()

        if task_id is None:
            return

        confirmed = messagebox.askyesno(
            "Delete Task",
            "Are you sure you want to delete this task?"
        )

        if confirmed:
            self.tasks = [
                task for task in self.tasks
                if task["id"] != task_id
            ]

            self.refresh_tasks()

    def get_selected_id(self):
        selection = self.tree.selection()

        if not selection:
            messagebox.showwarning(
                "Selection",
                "Please select a task."
            )
            return None

        return int(selection[0])

    def find_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task

        return None

    def refresh_tasks(self):
        self.tree.delete(*self.tree.get_children())

        for task in self.tasks:
            self.tree.insert(
                "",
                tk.END,
                iid=str(task["id"]),
                values=(
                    task["title"],
                    task["priority"],
                    task["due_date"] or "-",
                    task["status"]
                )
            )

        self.count_label.config(
            text=f"Total tasks: {len(self.tasks)}"
        )

    def update_clock(self):
        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.clock_label.config(text=current_time)

        self.root.after(1000, self.update_clock)


if __name__ == "__main__":
    root = tk.Tk()
    print(tkFont.families())
    default_font=tkFont.Font(family="Aria")
    default_font.configure(size=50)
    root.option_add("*Font", default_font)
    app = ToDoApp(root)
    root.mainloop()
