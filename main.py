import tkinter as tk
from tkinter import simpledialog, messagebox
import customtkinter as ctk
import json
import os
import sys

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(__file__)

DATA_FILE = os.path.join(BASE_DIR, "tasks.json")


class MultilineDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, initial_text=""):
        self.initial_text = initial_text
        super().__init__(parent, title=title)

    def body(self, master):
        self.text = tk.Text(master, height=8, width=40, wrap='word')
        self.text.pack(padx=6, pady=6)
        if self.initial_text:
            self.text.insert('1.0', self.initial_text)
        return self.text

    def apply(self):
        self.result = self.text.get('1.0', 'end-1c')


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x500")
        self.root.resizable(True, True)

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.tasks = []
        self.details = []
        self.completed = []

        # Title
        self.title_label = ctk.CTkLabel(
            root,
            text="To-Do List",
            font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        # Frame for buttons
        button_frame = ctk.CTkFrame(root)
        button_frame.grid(row=1, column=0, padx=10, sticky="ew")

        button_frame.columnconfigure((0, 1, 2), weight=1)

        # Add button
        self.add_btn = ctk.CTkButton(
            button_frame,
            text="Add Task",
            command=self.add_task
        )
        self.add_btn.grid(row=0, column=0, padx=5, sticky="ew")

        # Delete button
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete Task",
            command=self.delete_task
        )
        self.delete_btn.grid(row=0, column=1, padx=5, sticky="ew")

        # Clear button
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear All",
            command=self.clear_all
        )
        self.clear_btn.grid(row=0, column=2, padx=5, sticky="ew")

        # Listbox frame
        listbox_frame = ctk.CTkFrame(root)
        listbox_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.columnconfigure(1, weight=1)
        listbox_frame.rowconfigure(1, weight=1)

        # Label title frame
        label_title_frame = ctk.CTkFrame(listbox_frame)
        label_title_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        label_title_frame.columnconfigure(0, weight=1)
        label_title_frame.columnconfigure(1, weight=1)

        # Titles
        self.listbox_title = ctk.CTkLabel(
            label_title_frame,
            text="Tasks",
            font=("Arial", 12, "bold")
        )
        self.listbox_title.grid(row=0, column=0, pady=5)

        self.details_title = ctk.CTkLabel(
            label_title_frame,
            text="Details",
            font=("Arial", 12, "bold")
        )
        self.details_title.grid(row=0, column=1, pady=5)

        # Listbox 
        self.listbox = tk.Listbox(
            listbox_frame,
            font=("Arial", 10),
            bg="#2b2b2b",
            fg="white",
            selectbackground="#3a7ebf",
            selectforeground="white",
            relief="flat",
            highlightthickness=0
        )
        self.listbox.grid(row=1, column=0, sticky="nsew", padx=5)

        self.listbox.bind("<<ListboxSelect>>", self.select_task)
        self.listbox.bind("<Double-Button-1>", self.toggle_complete)

        # scrollbar
        self.scrollbar = ctk.CTkScrollbar(
                                        listbox_frame,
                                        command=self.listbox.yview
                                    )

        self.scrollbar.grid(row=1, column=0, sticky="nse")
        self.listbox.configure(yscrollcommand=self.scrollbar.set)

        # Details
        self.details_label = ctk.CTkLabel(
            listbox_frame,
            text="",
            font=("Arial", 10),
            anchor="nw",
            justify="left",
            wraplength=200
        )
        self.details_label.grid(row=1, column=1, sticky="nsew", padx=5)

        self.load_tasks()

        # Bind resize
        self.root.bind("<Configure>", self.resize_fonts)

    def resize_fonts(self, event):
        size = max(10, int(event.width / 35))
        self.title_label.configure(font=("Arial", size + 6, "bold"))
        self.listbox.configure(font=("Arial", size))
        self.details_label.configure(font=("Arial", size))
        self.add_btn.configure(font=("Arial", size, "bold"))
        self.delete_btn.configure(font=("Arial", size, "bold"))
        self.clear_btn.configure(font=("Arial", size, "bold"))

    def save_tasks(self):
        data = {
            "tasks": self.tasks,
            "details": self.details,
            "completed": self.completed,
        }
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                print("tasks saved successfully")
        except Exception as e:
            print("Error saving tasks:", e)

    def load_tasks(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                print("tasks loaded successfully")
        except Exception as e:
            print("Error loading tasks:", e)
            return

        tasks = data.get("tasks", [])
        details = data.get("details", [])
        completed = data.get("completed", [])

        self.listbox.delete(0, tk.END)
        self.tasks = []
        self.details = []
        self.completed = []

        for i, t in enumerate(tasks):
            d = details[i] if i < len(details) else "No details provided."
            c = completed[i] if i < len(completed) else False
            self.tasks.append(t)
            self.details.append(d)
            self.completed.append(bool(c))
            prefix = "☑" if c else "☐"
            self.listbox.insert(tk.END, f"{prefix} {t}")

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter a new task:")
        if task:
            dialog = MultilineDialog(self.root, title="Task Detail")
            detail = dialog.result
            self.tasks.append(task)
            self.completed.append(False)
            self.listbox.insert(tk.END, f"☐ {task}")
            if detail:
                self.details.append(detail)
            else:
                self.details.append("No details provided.")
            self.save_tasks()

    def select_task(self, event):
        try:
            index = self.listbox.curselection()[0]
            detail = self.details[index]
            self.details_label.configure(text=detail)
        except IndexError:
            self.details_label.configure(text="")

    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
            self.details_label.configure(text="")
            self.details.pop(index)
            try:
                self.tasks.pop(index)
            except Exception:
                pass
            try:
                self.completed.pop(index)
            except Exception:
                pass
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Clear all tasks?"):
            self.listbox.delete(0, tk.END)
            self.tasks.clear()
            self.details.clear()
            self.completed.clear()
            self.save_tasks()

    def toggle_complete(self, event):
        try:
            index = self.listbox.curselection()[0]
            self.completed[index] = not self.completed[index]
            text = self.tasks[index]
            prefix = "☑" if self.completed[index] else "☐"
            self.listbox.delete(index)
            self.listbox.insert(index, f"{prefix} {text}")
            self.listbox.selection_set(index)
            self.save_tasks()
        except IndexError:
            return


if __name__ == "__main__":
    root = ctk.CTk()
    app = ToDoApp(root)
    root.mainloop()

# Para gerar o .exe com ícone:
# pyinstaller --onefile --windowed --icon=icon.ico main.py