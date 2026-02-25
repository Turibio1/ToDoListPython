import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os


DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")



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
        self.root.configure(bg="#f0f0f0")
        
        self.tasks = []
        self.details = []
        self.completed = []
        
        # Title
        self.title_label = tk.Label(root, text="To-Do List", font=("Arial", 16, "bold"), fg="blue", 
                                    background="#f0f0f0")
        self.title_label.pack(pady=10, padx=50, fill="x", anchor="n")
         
        # Frame for buttons
        button_frame = tk.Frame(root,background="#f0f0f0")
        button_frame.pack( padx=50, expand=True, fill="x", anchor="n")
      
        # Add button
        self.add_btn = tk.Button(
                                button_frame, 
                                text="Add Task", 
                                command=self.add_task, 
                                width=8,
                                bd=5,                 
                                bg="#81D084",         
                                fg="white",          
                                font=("Arial", 10, "bold"),  
                                relief="raised",       
                                cursor="hand2",        
                                padx=5,                
                                pady=5                 
        )
        self.add_btn.grid(row=0, column=0, padx=5)
        
        # Delete button
        self.delete_btn = tk.Button(button_frame, 
                                    text="Delete Task", 
                                    command=self.delete_task, 
                                    width=8,
                                    bd=5,                  
                                    bg="#FF5722",           
                                    fg="white",             
                                    font=("Arial", 10, "bold"),  
                                    relief="raised",        
                                    padx=5,                
                                    pady=5                  
        )
        self.delete_btn.grid(row=0, column=1, padx=5)
        
        # Clear button
        self.clear_btn = tk.Button(button_frame,
                                   text="Clear All", command=self.clear_all, 
                                   width=8,
                                   bd=5,                  
                                   bg="#FF9800",           
                                   fg="white",             
                                   font=("Arial", 10, "bold"),  
                                   relief="raised",        
                                   cursor="hand2",         
                                   padx=5,                
                                   pady=5                  
        )
        self.clear_btn.grid(row=0, column=2, padx=5)

        # Listbox frame
        listbox_frame = tk.Frame(root, background="#f0f0f0")
        listbox_frame.pack(pady=10)

        #label title frame
        lable_title_frame = tk.Frame(listbox_frame, background="#f0f0f0")
        lable_title_frame.pack(padx=15, fill="x")

        #label title
        self.listbox_title = tk.Label(lable_title_frame, text="Tasks", font=("Arial", 12, "bold"), 
                                      fg="blue", background="#f0f0f0", anchor="s")    
        self.listbox_title.pack(pady=5, padx=38, side="left")
        self.details_title = tk.Label(lable_title_frame, text="Details", font=("Arial", 12, "bold"), 
                                      fg="blue", background="#f0f0f0", anchor="s")
        self.details_title.pack(pady=5, padx=80,side="right")

        # Listbox
        self.listbox = tk.Listbox(listbox_frame, height=30, width=20, font=("Arial", 10))
        self.listbox.pack(padx=10, side="left", fill="both")
        self.listbox.bind("<<ListboxSelect>>", self.select_task)
        self.listbox.bind("<Double-Button-1>", self.toggle_complete)

        # Details Label
        self.details_label = tk.Label(listbox_frame, height=30, width=30, font=("Arial", 10), 
                                      wraplength=200, justify="left", anchor="nw", background="#ffffff", relief="sunken", bd=1)
        self.details_label.pack(padx=10, side="right", fill="both", expand=True)       
        # load persisted tasks (if any)
        self.load_tasks()

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

        # clear any current items
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
            self.details_label.config(text=detail)
        except IndexError:
            self.details_label.config(text="")  
    
    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
            self.details_label.config(text="")
            self.details.pop(index)
            # keep internal lists synced
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
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()