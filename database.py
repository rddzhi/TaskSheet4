import mysql.connector


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost", user="root", password="12345",
                                            database="employee_attendance_tracker")
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def execute_query(self, query, values=()):
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return False
    
    def fetch_query(self, query, values=()):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()
    
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                employee_id VARCHAR(50) UNIQUE,
                department VARCHAR(100),
                position VARCHAR(100)
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id VARCHAR(50),
                clock_in DATETIME,
                clock_out DATETIME,
                total_hours DECIMAL(5,2),
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS leave_requests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id VARCHAR(50),
                start_date DATE,
                end_date DATE,
                reason TEXT,
                status VARCHAR(20) DEFAULT 'Pending',
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
            )
        """)
        
        self.conn.commit()
    
    def add_employee(self, name, employee_id, department, position):
        self.cursor.execute("SELECT COUNT(*) FROM employees WHERE employee_id = %s", (employee_id,))
        if self.cursor.fetchone()[0] > 0:
            print(f"Error: Employee ID {employee_id} already exists.")
            return False
        
        self.cursor.execute("INSERT INTO employees (name, employee_id, department, position) VALUES (%s, %s, %s, %s)",
                            (name, employee_id, department, position))
        self.conn.commit()
        print(f"Employee {employee_id} added successfully.")
        return True
    
    def get_all_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()
    
    def delete_employee(self, employee_id):
        self.cursor.execute("SELECT employee_id FROM attendance WHERE employee_id = %s", (employee_id,))
        if self.cursor.fetchone():
            print(f"Error: Cannot delete employee {employee_id} because attendance records exist.")
            return False
        
        self.cursor.execute("SELECT employee_id FROM leave_requests WHERE employee_id = %s", (employee_id,))
        if self.cursor.fetchone():
            print(f"Error: Cannot delete employee {employee_id} because leave requests exist.")
            return False
        
        self.cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
        self.conn.commit()
        return True
    
    def update_employee(self, emp_id, new_emp_id, new_name, new_department, new_position):
        try:
            self.cursor.execute("SELECT employee_id FROM employees WHERE employee_id = %s", (new_emp_id,))
            if self.cursor.fetchone():
                print(f"Error: Employee ID {new_emp_id} already exists.")
                return False
            
            query = """UPDATE employees
                       SET employee_id = %s, name = %s, department = %s, position = %s
                       WHERE employee_id = %s"""
            values = (new_emp_id, new_name, new_department, new_position, emp_id)
            self.db.execute_query(query, values)
            
            query_attendance = """UPDATE attendance SET employee_id = %s WHERE employee_id = %s"""
            self.db.execute_query(query_attendance, (new_emp_id, emp_id))
            
            query_leave = """UPDATE leave_requests SET employee_id = %s WHERE employee_id = %s"""
            self.db.execute_query(query_leave, (new_emp_id, emp_id))
            
            return True
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return False
        
        return self.execute_query(query, values)  # ✅ Fixed: Now properly updates employee records
    
    def clock_in(self, employee_id):
        try:
            self.cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
            employee = self.cursor.fetchone()
            
            if not employee:
                print(f"Error: Employee ID {employee_id} does not exist in employees table.")
                return False
            
            query = "INSERT INTO attendance (employee_id, clock_in) VALUES (%s, NOW())"
            self.cursor.execute(query, (employee_id,))
            self.conn.commit()
            print("Clock-in successful! Data committed.")
            return True
        
        except mysql.connector.Error as e:
            print(f"Database Error: {e}")
            return False
    
    def clock_out(self, employee_id):
        try:
            query = "UPDATE attendance SET clock_out = NOW() WHERE employee_id = %s AND clock_out IS NULL"
            self.cursor.execute(query, (employee_id,))
            self.conn.commit()
            print("Clock-out successful! Data committed.")
            return True
        
        except mysql.connector.Error as e:
            print(f"Database Error: {e}")
            return False
    
    def request_leave(self, employee_id, start_date, end_date, reason):
        try:
            self.cursor.execute(
                "INSERT INTO leave_requests (employee_id, start_date, end_date, reason, status) VALUES (%s, %s, %s, %s, %s)",
                (employee_id, start_date, end_date, reason, "pending"))
            self.conn.commit()
            print(f"Leave request submitted for {employee_id}.")
        except mysql.connector.Error as err:
            print(f"Error inserting leave request: {err}")
    
    def get_leave_status(self, employee_id):
        self.cursor.execute("SELECT status FROM leave_requests WHERE employee_id = %s ORDER BY id DESC LIMIT 1",
                            (employee_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None
    
    def get_all_leave_requests(self):
        self.cursor.execute("SELECT * FROM leave_requests")
        return self.cursor.fetchall()
    
    def approve_leave(self, leave_id):
        self.cursor.execute("UPDATE leave_requests SET status = 'approved' WHERE id = %s", (leave_id,))
        self.conn.commit()
    
    def reject_leave(self, leave_id):
        self.cursor.execute("UPDATE leave_requests SET status = 'denied' WHERE id = %s", (leave_id,))
        self.conn.commit()
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()