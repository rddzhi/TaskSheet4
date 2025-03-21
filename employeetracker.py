import tkinter as tk
from tkinter import messagebox, Toplevel, simpledialog, ttk

from controller import Controller


class EmployeeTrackerApp:
    def __init__(self, root):
        self.leave_frame = None
        self.controller = Controller()
        self.root = root
        self.root.title("Employee Attendance Tracker")
        self.root.geometry("620x850")
        self.root.configure(bg="#2C3E50")
        
        tk.Label(root, text="Employee Attendance Tracker", font=("Arial", 18, "bold"), bg="#2C3E50", fg="white").pack(
            pady=15)
        
        frame = tk.Frame(root, bg="#34495E", padx=20, pady=20, relief="ridge", bd=2)
        frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(frame, text="Employee ID:", bg="#34495E", fg="white", font=("Arial", 12)).grid(row=0, column=0,
                                                                                                sticky="w", pady=5)
        self.emp_id_entry = tk.Entry(frame, font=("Arial", 12), width=30)
        self.emp_id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(frame, text="Employee Name:", bg="#34495E", fg="white", font=("Arial", 12)).grid(row=1, column=0,
                                                                                                  sticky="w", pady=5)
        self.name_entry = tk.Entry(frame, font=("Arial", 12), width=30)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(frame, text="Department:", bg="#34495E", fg="white", font=("Arial", 12)).grid(row=2, column=0,
                                                                                               sticky="w", pady=5)
        self.department_entry = tk.Entry(frame, font=("Arial", 12), width=30)
        self.department_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(frame, text="Position:", bg="#34495E", fg="white", font=("Arial", 12)).grid(row=3, column=0,
                                                                                             sticky="w", pady=5)
        self.position_entry = tk.Entry(frame, font=("Arial", 12), width=30)
        self.position_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Button(frame, text="Add Employee", command=self.add_employee, bg="#27AE60", fg="white",
                  font=("Arial", 12, "bold"), width=15).grid(row=4, column=0, pady=10)
        tk.Button(frame, text="View Employees", command=self.admin_login, bg="#2980B9", fg="white",
                  font=("Arial", 12, "bold"), width=15, ).grid(row=4, column=1, pady=10)
        
        # Attendance Section
        attendance_frame = tk.Frame(root, bg="#34495E", padx=20, pady=20, relief="ridge", bd=2)
        attendance_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(attendance_frame, text="Employee ID for Attendance:", bg="#34495E", fg="white",
                 font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.attendance_id_entry = tk.Entry(attendance_frame, font=("Arial", 12), width=30)
        self.attendance_id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Button(attendance_frame, text="Clock In", command=self.clock_in, bg="#F39C12", fg="white",
                  font=("Arial", 12), width=15).grid(row=1, column=0, pady=10)
        tk.Button(attendance_frame, text="Clock Out", command=self.clock_out, bg="#E74C3C", fg="white",
                  font=("Arial", 12), width=15).grid(row=1, column=1, pady=10)
        
        # Leave Management
        leave_frame = tk.Frame(root, bg="#34495E", padx=20, pady=20, relief="ridge", bd=2)
        leave_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(leave_frame, text="Employee ID for Leave:", bg="#34495E", fg="white", font=("Arial", 12)).grid(row=0,
                                                                                                                column=0,
                                                                                                                sticky="w",
                                                                                                                pady=5)
        self.leave_id_entry = tk.Entry(leave_frame, font=("Arial", 12), width=30)
        self.leave_id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(leave_frame, text="Start Date (yyyy/mm/dd):", bg="#34495E", fg="white", font=("Arial", 12)).grid(row=1,
                                                                                                                  column=0,
                                                                                                                  sticky="w",
                                                                                                                  pady=5)
        self.start_date_entry = tk.Entry(leave_frame, font=("Arial", 12), width=30)
        self.start_date_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(leave_frame, text="End Date (yyyy/mm/dd):", bg="#34495E", fg="white", font=("Arial", 12)).grid(row=2,
                                                                                                                column=0,
                                                                                                                sticky="w",
                                                                                                                pady=5)
        self.end_date_entry = tk.Entry(leave_frame, font=("Arial", 12), width=30)
        self.end_date_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(leave_frame, text="Reason:", bg="#34495E", fg="white", font=("Arial", 12)).grid(row=3, column=0,
                                                                                                 sticky="w", pady=5)
        self.reason_entry = tk.Entry(leave_frame, font=("Arial", 12), width=30)
        self.reason_entry.grid(row=3, column=1, padx=10, pady=5)
        
        leave_buttons_frame = tk.Frame(leave_frame, bg="#34495E")
        leave_buttons_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        tk.Button(leave_buttons_frame, text="Request Leave", command=self.request_leave, bg="#8E44AD", fg="white",
                  font=("Arial", 12, "bold"), width=13).grid(row=0, column=0, padx=5, pady=5)
        
        tk.Button(leave_buttons_frame, text="View Leave Requests", command=self.admin_login_leave, bg="#16A085",
                  fg="white", font=("Arial", 12, "bold"), width=17).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(leave_buttons_frame, text="Check My Leave Status", command=self.check_leave_status, bg="#D35400",
                  fg="white", font=("Arial", 12, "bold"), width=18).grid(row=0, column=2, padx=5, pady=5)
    
    def admin_login(self):
        password = simpledialog.askstring("Admin Login", "Enter admin password:", show='*')
        if password == "admin123":
            self.view_employees()
        else:
            messagebox.showerror("Error", "Incorrect password!")
    
    def view_employees(self):
        """ Displays employees in a table format without Actions column """
        employee_window = Toplevel(self.root)
        employee_window.title("Employee List")
        employee_window.geometry("600x500")
        employee_window.configure(bg="#ADD8E6")
        
        columns = ("ID", "Name", "Employee ID", "Department", "Position")
        tree = ttk.Treeview(employee_window, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        
        tree.pack(fill="both", expand=True)
        
        employees = self.controller.get_all_employees()
        
        if not employees:
            tk.Label(employee_window, text="No employees found.", bg="#e0f7fa", font=("Arial", 12)).pack()
            return
        
        if not employees:
            tk.Label(employee_window, text="No employees found.", bg="#e0f7fa", font=("Arial", 12)).pack()
        else:
            for emp in employees:
                if len(emp) >= 5:  # Ensure there are at least 5 values
                    emp_id, name, emp_code, department, position = emp  # Unpack all 5 values
                    tree.insert("", "end", values=(emp_id, name, emp_code, department, position))
        
        def edit_employee():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select an employee to edit.")
                return
            
            emp_values = tree.item(selected_item, "values")
            emp_id, emp_name, emp_code, emp_department, emp_position = emp_values
            
            edit_window = Toplevel(employee_window)
            edit_window.title("Edit Employee")
            edit_window.geometry("300x250")  # Increase height to fit the button
            
            tk.Label(edit_window, text="Name:").pack(pady=2)
            name_entry = tk.Entry(edit_window)
            name_entry.insert(0, emp_name)
            name_entry.pack(pady=2)
            
            tk.Label(edit_window, text="Department:").pack(pady=2)
            department_entry = tk.Entry(edit_window)
            department_entry.insert(0, emp_department)
            department_entry.pack(pady=2)
            
            tk.Label(edit_window, text="Position:").pack(pady=2)
            position_entry = tk.Entry(edit_window)
            position_entry.insert(0, emp_position)
            position_entry.pack(pady=2)
            
            def save_changes():
                new_name = name_entry.get().strip()
                new_department = department_entry.get().strip()
                new_position = position_entry.get().strip()
                
                if not new_name or not new_department or not new_position:
                    messagebox.showerror("Error", "All fields are required!")
                    return
                
                success = self.controller.update_employee(emp_id, emp_id, new_name, new_department, new_position)
                if success:
                    messagebox.showinfo("Success", "Employee updated successfully!")
                    
                    # ✅ Update the Treeview directly without closing and reopening the main window
                    tree.item(selected_item, values=(emp_id, new_name, emp_code, new_department, new_position))
                    
                    edit_window.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update employee.")
            
            tk.Button(edit_window, text="Save", command=save_changes, bg="#27AE60", fg="white", font=("Arial", 12),
                      width=20).pack(pady=10)
        
        def delete_employee():
            selected_item = tree.selection()
            
            if not selected_item:
                print("No employee selected for deletion.")
                return
            
            employee_data = tree.item(selected_item, "values")
            if len(employee_data) >= 3:
                employee_id = employee_data[2]  # Assuming Employee ID is the third column in the Treeview
                
                if self.controller.delete_employee(employee_id):
                    tree.delete(selected_item)  # Removes from Treeview UI
                    print("Employee successfully deleted from the database and UI.")
        
        tk.Button(employee_window, text="Edit Selected", command=edit_employee, bg="blue", fg="white").pack(
            side=tk.LEFT, padx=10)
        tk.Button(employee_window, text="Delete Selected", command=delete_employee, bg="red", fg="white").pack(
            side=tk.RIGHT, padx=10)
    
    def add_employee(self):
        name = self.name_entry.get().strip()
        emp_id = self.emp_id_entry.get().strip()
        department = self.department_entry.get().strip()
        position = self.position_entry.get().strip()
        
        if not name or not emp_id or not department or not position:
            messagebox.showerror("Error", "All fields are required!")
            return  # Stop execution if fields are empty
        
        self.controller.add_employee(name, emp_id, department, position)
        messagebox.showinfo("Success", "Employee record successfully added!")
        
        self.name_entry.delete(0, tk.END)
        self.emp_id_entry.delete(0, tk.END)
        self.department_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
    
    def admin_login_leave(self):
        password = simpledialog.askstring("Admin Login", "Enter admin password:", show='*')
        if password == "admin123":
            self.view_leave_requests()
        else:
            messagebox.showerror("Error", "Incorrect password!")
    
    def view_leave_requests(self):
        """Displays leave requests with approve/reject options."""
        
        leave_window = Toplevel(self.root)
        leave_window.title("Leave Requests")
        leave_window.geometry("600x500")
        
        columns = ("Leave ID", "Employee ID", "Start Date", "End Date", "Reason", "Status")
        tree = ttk.Treeview(leave_window, columns=columns, show="headings")
        tree.heading("Leave ID", text="Leave ID")
        tree.heading("Employee ID", text="Employee ID")
        tree.heading("Start Date", text="Start Date")
        tree.heading("End Date", text="End Date")
        tree.heading("Reason", text="Reason")
        tree.heading("Status", text="Status")
        
        tree.column("Leave ID", width=60)
        tree.column("Employee ID", width=80)
        tree.column("Start Date", width=80)
        tree.column("End Date", width=80)
        tree.column("Reason", width=140)
        tree.column("Status", width=80)
        
        tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        leave_requests = self.controller.get_all_leave_requests()
        
        for leave in leave_requests:
            tree.insert("", "end", values=leave)
        
        button_frame = tk.Frame(leave_window)
        button_frame.pack(pady=10)
        
        approve_btn = tk.Button(button_frame, text="Approve", bg="#4CAF50", fg="white", padx=10, pady=5,
                                command=lambda: self.process_leave_request(tree, "approved"))
        approve_btn.grid(row=0, column=0, padx=5)
        
        reject_btn = tk.Button(button_frame, text="Reject", bg="#F44336", fg="white", padx=10, pady=5,
                               command=lambda: self.process_leave_request(tree, "rejected"))
        reject_btn.grid(row=0, column=1, padx=5)
    
    def process_leave_request(self, tree, status):
        """Handles the approval or rejection of a leave request."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a leave request to proceed.")
            return
        
        leave_values = tree.item(selected_item, "values")
        leave_id = leave_values[0]
        
        if status == "approved":
            self.approve_leave(leave_id)
        elif status == "rejected":
            self.reject_leave(leave_id)
        
        tree.delete(selected_item)
    
    def check_leave_status(self):
        emp_id = self.leave_id_entry.get()
        if not emp_id:
            messagebox.showerror("Error", "Please enter your Employee ID!")
            return
        
        status = self.controller.get_leave_status(emp_id)
        messagebox.showinfo("Leave Status", f"Your leave status: {status}")
    
    def clock_in(self):
        emp_id = self.attendance_id_entry.get().strip()
        if not emp_id:
            messagebox.showerror("Error", "Please enter Employee ID!")
            return
        
        success = self.controller.clock_in(emp_id)
        if success:
            messagebox.showinfo("Success", "Clock-in successful!")
        else:
            messagebox.showerror("Error", f"Employee ID {emp_id} does not exist. Please add the employee first.")
    
    def clock_out(self):
        emp_id = self.attendance_id_entry.get()
        if not emp_id:
            messagebox.showerror("Error", "Please enter Employee ID!")
            return
        
        self.controller.clock_out(emp_id)
        messagebox.showinfo("Success", "Clock-out successful!")
        
    def request_leave(self):
        emp_id = self.leave_id_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        reason = self.reason_entry.get()
        
        if not all([emp_id, start_date, end_date, reason]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        self.controller.request_leave(emp_id, start_date, end_date, reason)
        messagebox.showinfo("Success", "Leave request submitted!")
    
    def approve_leave(self, leave_id):
        self.controller.update_leave_status(leave_id, "Approved")
        messagebox.showinfo("Success", "Leave request approved!")
        self.view_leave_requests()

    def reject_leave(self, leave_id):
        self.controller.update_leave_status(leave_id, "Denied")
        messagebox.showinfo("Success", "Leave request denied!")
        self.view_leave_requests()


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeTrackerApp(root)
    root.mainloop()