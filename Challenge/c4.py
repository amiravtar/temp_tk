import tkinter as tk

root=tk.Tk()

root.geometry("600x600")

lsb=tk.Listbox(root)

lsb.pack()

lsb.insert(tk.END,"test1")
lsb.insert(tk.END,"test2")

root.mainloop()