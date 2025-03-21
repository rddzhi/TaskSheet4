import mysql

from database import Database
from tkinter import messagebox


class Controller:
    def __init__(self):
        self.cursor = None
        self.conn = None
        self.db = Database()
    
    def add_employee(self, name, employee_id, department, position):
        return self.db.add_employee(name, employee_id, department, position)
    
    def delete_employee(self, employee_id):
        try:
            query = "DELETE FROM employees WHERE employee_id = %s"
            self.db.cursor.execute(query, (employee_id,))
            self.db.conn.commit()
            
            print(f"Employee {employee_id} deleted successfully.")
            return True
        except mysql.connector.Error as e:
            print(f"Database Error: {e}")
            return False
    
    def get_all_employees(self):
        return self.db.get_all_employees()
    
    def employee_exists(self, emp_id):
        query = "SELECT COUNT(*) FROM employees WHERE employee_id = %s"
        result = self.db.fetch_query(query, (emp_id,))
        return result[0][0] > 0 if result else False
    
    def is_clocked_in(self, emp_id):
        self.cursor.execute("SELECT COUNT(*) FROM attendance WHERE emp_id = %s AND clock_out_time IS NULL", (emp_id,))
        return self.cursor.fetchone()[0] > 0
    
    def clock_in(self, employee_id):
        self.db.clock_in(employee_id)
        return True
    
    def clock_out(self, employee_id):
        self.db.clock_out(employee_id)
    
    def request_leave(self, employee_id, start_date, end_date, reason):
        self.db.request_leave(employee_id, start_date, end_date, reason)
    
    def get_leave_status(self, employee_id):
        status = self.db.get_leave_status(employee_id)
        if status:
            return status
        else:
            return "No leave request found."
    
    def get_all_leave_requests(self):
        return self.db.get_all_leave_requests()
    
    def update_employee(self, emp_id, new_emp_id, new_name, new_department, new_position):
        try:
            query = """UPDATE employees
                       SET employee_id = %s, name = %s, department = %s, position = %s
                       WHERE employee_id = %s"""
            values = (new_emp_id, new_name, new_department, new_position, emp_id)
            self.db.execute_query(query, values)
            
            query_attendance = "UPDATE attendance SET employee_id = %s WHERE employee_id = %s"
            self.db.execute_query(query_attendance, (new_emp_id, emp_id))
            
            query_leave = "UPDATE leave_requests SET employee_id = %s WHERE employee_id = %s"
            self.db.execute_query(query_leave, (new_emp_id, emp_id))
            
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Failed to update employee: {e}")
            self.db.conn.rollback()
            return False
    
    def view_leave_requests(self):
        try:
            query = "SELECT * FROM leave_requests"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Database Error: {e}")
            return []
    
    def update_leave_status(self, leave_id, status):
        query = "UPDATE leave_requests SET status = %s WHERE id = %s"
        values = (status, leave_id)
        self.db.execute_query(query, values)
        
    def approve_leave(self, leave_id):
        self.db.approve_leave(leave_id)
        messagebox.showinfo("Success", "Leave request approved!")
    
    def reject_leave(self, leave_id):
        self.db.reject_leave(leave_id)
        messagebox.showinfo("Success", "Leave request rejected!")
    
    def update_leave_status(self, leave_id, status):
        query = "UPDATE leave_requests SET status = %s WHERE id = %s"
        connection = self.db.conn
        cursor = connection.cursor()
        
        try:
            cursor.execute(query, (status, leave_id))
            connection.commit()
            print(f"Leave request {leave_id} status updated to {status}.")
        except Exception as e:
            print("Error updating leave request status:", e)
            connection.rollback()
        finally:
            cursor.close()


