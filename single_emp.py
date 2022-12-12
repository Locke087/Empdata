from Employee import Employee
import tkinter as tk
from tkinter import messagebox
import csv

class SingleEmployeePrivate():
    def __init__(self,master, viewer, employee) -> None:
        self.master = master
        self.master.title("View Employee Screen")
        self.master.geometry('1200x900')
        self.master['bg'] = '#007385'

        #TODO Binding is a tiny bit buggy when clicking. Maybe removing the feature to begin with?
        #TODO actually document this document
        self.frame =tk.Frame(width=1000, height=720, background='#007385')
        self.frame.grid(row=0, column=0)
        # In center of screen, create welcome message, username and password input boxes with username and password headings
        self.user = employee
        self.viewer = viewer
        self.back_button = tk.Button(self.frame, text='Back', command=self.go_back, background='silver')
        self.back_button.grid(row=0, column=0, padx=0)
        self.title_view = tk.Label(self.frame, text=f"{self.user.fname} {self.user.lname}'s Profile", font=('Arial', 50), background='silver')
        self.title_view.grid(row=0, column=1, padx=0, sticky=tk.W)
        self.views: dict[tk.Label] = {}
        self.views['id'] = tk.Label(self.frame, text="ID: " + self.user.emp_id, background='silver')
        self.views['fname'] = tk.Label(self.frame, text="First Name: " + self.user.fname, background='silver')
        self.views['lname'] = tk.Label(self.frame, text="Last Name: " + self.user.lname, background='silver')
        self.views['address'] = tk.Label(self.frame, text="Address: " + str(self.user.address), background='silver')
        self.views['office_phone'] = tk.Label(self.frame, text="Office Phone: " + self.user.office_phone, background='silver')
        self.views['pay_type'] = tk.Label(self.frame, text="Paytype: " + self.user.pay_type, foreground="white", background='silver')
        self.views['wage'] = tk.Label(self.frame, text="Wage: " + self.user.wage, background='silver')
        self.views['birthday'] = tk.Label(self.frame, text="Birthday" + self.user.birthday, background='silver')
        self.views['permission'] = tk.Label(self.frame, text="Permission Level: " + self.user.permission, background='silver')
        self.views['title'] = tk.Label(self.frame, text="Title: " + self.user.title, background='silver')
        self.views['department'] = tk.Label(self.frame, text="Department: " + self.user.department, background='silver')
        self.views['office_email'] = tk.Label(self.frame, text="Office Email: " + self.user.office_email, background='silver')
        self.views['emergency_contact'] = tk.Label(self.frame, text="Emergency Contact: " + self.user.emergency_contact, background='silver')
        self.views['start_date'] = tk.Label(self.frame, text="Start Date: " + self.user.start_date, background='silver')
        self.views['end_date'] = tk.Label(self.frame, text="End Date: " + self.user.end_date, background='silver')
        self.views['bank_info'] = tk.Label(self.frame, text="Bank Info: " + self.user.bank_info, background='silver')
        self.views['is_deactivated'] = tk.Label(self.frame, text="Is Deactivated: " + self.user.is_deactivated, background='silver')
        self.views['social_secuitry'] = tk.Label(self.frame, text= "Social Secuitry: " + self.user.social_secuitry, background='silver')

        rlim = 9
        clim = 4
        r, c = 1, 0
        for key, view in self.views.items():
            # print('dict values', view, key)
            view.grid(row=r, column=c, padx=10, pady=20)
            r += 1
            if r >= rlim:
                r = 1
                c += 1



        
    
    def go_back(self):
        from view_employees import ViewEmployeeEmp, ViewEmployeeAdmin
        self.frame.destroy()
        #TODO Insert total data  in place of the user below
        if self.viewer.permission == 'admin':
            self.app = ViewEmployeeAdmin(self.master, employee_data=self.viewer)
        else:
            self.app = ViewEmployeeEmp(self.master, employee_data=self.viewer)
   
        

class SingleEmployeePub():
    def __init__(self,master,viewer,  employee: Employee) -> None:
        self.master = master
        self.master.title("View Employee Screen")
        self.master.geometry('1000x720')

        
        self.frame =tk.Frame(width=1000, height=720)
        self.frame.grid(row=0, column=0)
        # In center of screen, create welcome message, username and password input boxes with username and password headings
        self.user = employee
        self.viewer = viewer
        self.back_button = tk.Button(self.frame, text='Back', command=self.go_back)
        self.back_button.grid(row=0, column=0, padx=0)
        self.back_button1 = tk.Button(self.frame, text='Print Pay', command=self.printpayInfo)
        self.back_button1.grid(row=0, column=2, padx=0)
        self.title_view = tk.Label(self.frame, text=f"{self.user.fname} {self.user.lname}'s Profile", font=('Arial', 50))
        self.title_view.grid(row=0, column=1, padx=0, sticky=tk.W)
        self.views: dict[tk.Label] = {}
        self.views['id'] = tk.Label(self.frame, text="ID: " + self.user.emp_id)
        self.views['fname'] = tk.Label(self.frame, text="First Name: " + self.user.fname)
        self.views['lname'] = tk.Label(self.frame, text="Last Name: " + self.user.lname)
        self.views['office_phone'] = tk.Label(self.frame, text="Office Phone: " + self.user.office_phone)
        self.views['birthday'] = tk.Label(self.frame, text="Birthday: " + self.user.birthday)
        self.views['title'] = tk.Label(self.frame, text="Title: " + self.user.title)
        self.views['department'] = tk.Label(self.frame, text="Department: " + self.user.department)
        self.views['office_email'] = tk.Label(self.frame, text="Office Email: " + self.user.office_email)
        self.views['emergency_contact'] = tk.Label(self.frame, text="Emergency Contact: " + self.user.emergency_contact)

        rlim = 5
        clim = 4
        r, c = 1, 0
        for key, view in self.views.items():
            # print('dict values', view, key)
            view.grid(row=r, column=c, padx=10, pady=20)
            r += 1
            if r >= rlim:
                r = 1
                c += 1
    
    def go_back(self):
        from view_employees import ViewEmployeeEmp
        self.frame.destroy()
        #TODO Insert total data  in place of the user below
        self.app = ViewEmployeeEmp(self.master, employee_data=self.viewer)