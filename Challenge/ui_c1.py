import datetime
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox, ttk

import arabic_reshaper
from bidi.algorithm import get_display


def prepare_persian(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)


DATE_STRING_FORMAT = "%Y-%m-%d %H:%M:%S"


class TodoList:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("اپلیکیشن TODO")
        self.root.geometry("800x500")
        self.root.minsize(800, 500)
        self.setup_ui()

    def setup_ui(self):
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(fill="x")

        self.date_variable = tk.StringVar(value="test5")
        self.lbl_date = tk.Label(
            self.header_frame,
            textvariable=self.date_variable,
        )
        self.lbl_date.pack(side="right")
        self.update_time()

        self.action_header = tk.Frame(self.root)
        self.action_header.pack(fill="x", padx=20)

        self.btn_add_task = tk.Button(
            self.action_header, text="Add Task", command=self.add_task
        )
        self.btn_edit_task = tk.Button(self.action_header, text="Edit Task")
        self.btn_delete_task = tk.Button(self.action_header, text="Delete Task")
        self.btn_add_task.pack(side="right", padx=10)
        self.btn_edit_task.pack(side="right", padx=10)
        self.btn_delete_task.pack(side="right", padx=10)

        self.task_header = tk.Frame(self.root)
        self.task_header.pack(fill="x", padx=20, pady=20)
        task_columns = ("Task", "priority", "due date", "status")

        self.task_list = ttk.Treeview(
            self.task_header, columns=task_columns, show="headings"
        )
        self.task_list.heading("Task", text="Task", anchor="center")
        self.task_list.heading("priority", text="priority", anchor="center")
        self.task_list.heading("due date", text="due date", anchor="center")
        self.task_list.heading("status", text="status", anchor="center")
        self.task_list.pack(expand=True)

    def update_time(self):
        self.date_variable.set(datetime.datetime.now().strftime(DATE_STRING_FORMAT))
        self.root.after(1000, self.update_time)

    def add_task(self):
        add_ui = TaskCrud(tk.Toplevel())


class TaskCrud:
    def __init__(self, root: tk.Toplevel, on_save=None, input=None) -> None:
        self.root = root
        self.on_save = on_save
        self.input = input

        self.root.geometry("500x300")
        self.root.minsize(500, 300)
        self.root.title("اضافه کردن")
        self.setup_ui()

        self.root.mainloop()

    def setup_ui(self):

        self.main_frame=tk.Frame(self.root)
        self.main_frame.pack(fill="both",padx=10,pady=10)

        self.lbl1=tk.Label(self.main_frame,text="Title").pack(anchor="w")

        self.ent_title=tk.Entry(self.main_frame)
        self.ent_title.pack(fill="x")


        self.selected_p=tk.StringVar(value="Medium")

        self.cmb_pri=ttk.Combobox(self.main_frame,textvariable=self.selected_p,values=("High","Medium","Low"),state="readonly")
        self.cmb_pri.pack(fill="x")


        self.lbl2=tk.Label(self.main_frame,text="Due Date yyy-mm-dd").pack(anchor="w")

        self.ent_due_date=tk.Entry(self.main_frame)
        self.ent_due_date.pack(fill="x")

        self.is_done=tk.BooleanVar(value=False)
        self.ckb_is_done=tk.Checkbutton(self.main_frame,text="Is Done",variable=self.is_done)
        self.ckb_is_done.pack(fill="x")
        
if __name__ == "__main__":
    root = tk.Tk()

    TodoList(root)
    root.mainloop()
