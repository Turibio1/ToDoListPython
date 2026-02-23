import tkinter as tk
from tkinter import simpledialog, messagebox

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x500")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        
        self.tasks = []
        self.details = []
        
        # Title
        self.title_label = tk.Label(root, text="To-Do List", font=("Arial", 16, "bold"), fg="blue", 
                                    background="#3771dd")
        self.title_label.pack(pady=10, padx=50, fill="x", anchor="n")
        
        # Resize event binding
        self.root.bind("<Configure>", self.update_title_font)
         
        # Frame for buttons
        button_frame = tk.Frame(root,background="#fc0000")
        button_frame.pack( padx=40, expand=True, fill="x", anchor="n")
      
        # Add button
        self.add_btn = tk.Button(
                                button_frame, 
                                text="Add Task", 
                                command=self.add_task, 
                                width=10,
                                bd=5,                 
                                bg="#81D084",         
                                fg="white",          
                                font=("Arial", 10, "bold"),  
                                relief="raised",       
                                cursor="hand2",        
                                padx=10,                
                                pady=5                 
        )
        self.add_btn.grid(row=0, column=0, padx=5)
        
        # Delete button
        self.delete_btn = tk.Button(button_frame, 
                                    text="Delete Task", 
                                    command=self.delete_task, 
                                    width=10,
                                    bd=5,                  
                                    bg="#FF5722",           
                                    fg="white",             
                                    font=("Arial", 10, "bold"),  
                                    relief="raised",        
                                    padx=10,                
                                    pady=5                  
        )
        self.delete_btn.grid(row=0, column=1, padx=5)
        
        # Clear button
        self.clear_btn = tk.Button(button_frame,
                                   text="Clear All", command=self.clear_all, width=10,
                                   bd=5,                  
                                   bg="#FF9800",           
                                   fg="white",             
                                   font=("Arial", 10, "bold"),  
                                   relief="raised",        
                                   cursor="hand2",         
                                   padx=10,                
                                   pady=5                  
        )
        self.clear_btn.grid(row=0, column=2, padx=5)

        # Listbox frame
        listbox_frame = tk.Frame(root, background="#00b90f")
        listbox_frame.pack(pady=10)
    
        # Listbox
        self.listbox = tk.Listbox(listbox_frame, height=30, width=30, font=("Arial", 10))
        self.listbox.pack(pady=10, padx=10, side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.select_task)
        self.root.bind("<Configure>", self.update_listbox_size)
        
        # Details Label
        self.details_label = tk.Label(listbox_frame, height=30, width=50, font=("Arial", 10), 
                                      wraplength=200, justify="left", anchor="nw")
        self.details_label.pack(pady=10, padx=10, side="right", fill="both", expand=True)
        self.root.bind("<Configure>", self.update_details_label_size)
        
       
    def update_title_font(self, event):
        new_font_size = max(12, self.root.winfo_width() // 60)
        self.title_label.configure(font=("Arial", new_font_size, "bold"))
        self.update_button_font()
    
    def update_button_font(self):
        new_font_size = max(8, self.root.winfo_width() // 80)
        button_font = ("Arial", new_font_size)
        self.add_btn.configure(font=button_font)
        self.delete_btn.configure(font=button_font)
        self.clear_btn.configure(font=button_font)

    
    def update_listbox_size(self, event):
        new_height = max(10, self.root.winfo_height() // 10)
        self.listbox.configure(height=new_height)
        new_width = max(20, self.root.winfo_width() // 10)
        self.listbox.configure(width=new_width)

    def update_details_label_size(self, event):
        new_width = max(20, self.root.winfo_width() // 10)
        self.details_label.configure(width=new_width)
        new_height = max(10, self.root.winfo_height() // 10)
        self.details_label.configure(height=new_height)
    
    
    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter a new task:")
        if task:
            detail=simpledialog.askstring("Task Detail", "Enter details for the task:")
            self.tasks.append(task)
            self.listbox.insert(tk.END, task)
            if detail:
                self.details.append(detail)
            else:
                self.details.append("No details provided.")
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
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")
    
    def clear_all(self):
        if messagebox.askyesno("Confirm", "Clear all tasks?"):
            self.listbox.delete(0, tk.END)
            self.tasks.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()