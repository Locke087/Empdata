from Employee import Employee
import tkinter as tk
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog as fd
import csv
from single_emp import *
from edit_employee import EditEmployee
from add_employee import AddEmployee
import tkinter.messagebox as messagebox
import os
import csvalchemy
#TODO clean up all the code for matinence.
class ViewEmployeeAdmin():
    def __init__(self,master, employee_data) -> None:
        self.master = master
        self.master.title("View Employee Screen")
        self.master.geometry('1200x900')
        # self.master['bg'] ='cyan'
        style = Style()
        style.configure('W.TLabel', font =
               ('Arial', 50, 'bold', 'underline'),
                foreground = 'red', background = 'blue')
        style.configure('W.TButton', font =
               ('Arial', 25, 'bold', 'underline'),
                foreground = 'orange', background = 'black')


        #TODO actually document this document
        #TODO Make the thing read once only or use asyncrounous programming
        #TODO (cont) to make the page load more seemless
        self.frame =tk.Frame(width=1200, height=900)
        self.frame.grid(row=0, column=0)
        # In center of screen, create welcome message, username and password input boxes with username and password headings
        self.user: Employee = employee_data
   
        self.employees: list[Employee] = []
        filename = './employee.csv'
        if os.path.exists('./employeetemp.csv'):
            filename = './employeetemp.csv'
        csvalchemy.singleton.path = filename
        self.employees = csvalchemy.singleton.get_rows()
        
        
        self.usertitle = tk.Label(self.frame, text=f'Hello, {self.user.fname} {self.user.lname}', font=('Arial', 35), anchor=tk.W)
        self.usertitle.grid(row=0, column=0, padx=40)
        self.perm = tk.Label(self.frame, text=f'Permission:{self.user.permission.upper()}', font=('Arial', 25), anchor=tk.E)
        self.perm.grid(row=1,column=0,pady=10, padx=40)

        self.edit_emp_btn = tk.Button(self.frame, text="Edit Employee", command=self.goEdit, font=('Arial', 15))
        self.edit_emp_btn.grid(row=3, column=0,pady=10)
        self.edit_emp_btn = tk.Button(self.frame, text="Add Employee", command=self.goAdd, font=('Arial', 15))
        self.edit_emp_btn.grid(row=4, column=0, pady=10)
        self.edit_emp_btn = tk.Button(self.frame, text="Deactivate/Activate Employee", command=self.goArchive, font=('Arial', 15))
        self.edit_emp_btn.grid(row=5, column=0, pady=10)
  
        self.emp_title = tk.Label(self.frame, text="Employee list", font=('Arial', 50))
        self.emp_title.grid(row=0, column=1, columnspan=3)


        self.emp_title = tk.Label(self.frame, text="🔍", font=('Arial', 25))
        self.emp_title.grid(row=1, column=1, padx=0)
        self.search_var = tk.StringVar()#search value to be stored in here
        self.search_entry = tk.Entry(self.frame, textvariable=self.search_var, width=30, font=('Arial', 25))
        self.search_entry.grid(row=1, column=2, padx=0, sticky=tk.NSEW)
    
        
        self.scroll = tk.Scrollbar(self.frame)
        self.scroll.grid(row=2, column=3, sticky=tk.NS)

        
        self.list_box = tk.Listbox(self.frame, height=15,yscrollcommand=self.scroll.set, font=('Arial', 25))
        self.deacts = []
        for row in self.employees:
            employee = Employee(row)
            if employee.is_deactivated == 'n':
                self.list_box.insert(tk.END, f"{employee.fname} {employee.lname}")
            else:
                self.deacts.append(employee)
        if len(self.deacts) > 0:
            self.list_box.insert(tk.END, '---DEACTIVATED EMPLOYEES---')
            for employee in self.deacts:
                self.list_box.insert(tk.END, f"{employee.fname} {employee.lname}")
        self.list_box.grid(row=2, column=1, columnspan=2, sticky=(tk.W + tk.E))
    
        

        self.go_to_emp = tk.Button(self.frame, text="View employee", command=self.goEmp, font=('Arial', 15))
        self.go_to_emp.grid(row=3, column=1, columnspan=2, pady=10)
        self.payslip = tk.Button(self.frame, text="Generate Payslip", command=self.generatePayslip, font=('Arial', 15))
        self.payslip.grid(row=4, column=1, columnspan=2, pady=10)
        
        self.scroll.config(command=self.list_box.yview)

        #Binding for events such as when the listbox element is selected and when we type in the search box
        self.list_box.bind('<<ListboxSelect>>', self.fillout)
        self.search_entry.bind("<KeyRelease>", self.update_search)

    def fillout(self,event):
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, self.list_box.get(tk.ANCHOR))
    def update_search(self, event):
        data = None
        #removing whitespace, which is annoying to deal with
        typed = self.search_var.get().replace(' ', '')
        if typed == '' or typed == '---DEACTIVATEDEMPLOYEES---':
            #Don't even bother if it's the header infomation
            #If there nothing but spaces or empty box, then just put everything back
            data = self.employees
        else:
            #TODO Chagne this into a search funciton in the CSV writer class
            #Otherwise do a simple search
            data = []
            for item in self.employees:
                comb = f"{item.emp_id}{item.fname}{item.lname}"
                is_ok = typed.lower() in item.fname.lower() or typed.lower() in item.lname.lower() \
                        or typed.lower() in comb.lower() or typed.lower() in comb.lower()
                if is_ok:
                    data.append(item)
        #clear the listbox first
        self.list_box.delete(0, tk.END)
        #Enter in the filtered results
        for emp in data:
            self.list_box.insert(tk.END, f"{emp.fname} {emp.lname}")
    def refresh_listbox(self):
        self.employees = csvalchemy.singleton.get_rows()
        self.list_box.delete(0, tk.END)
        self.deacts.clear()
        for row in self.employees:
            employee = Employee(row)
            if employee.is_deactivated == 'n':
                self.list_box.insert(tk.END, f"{employee.fname} {employee.lname}")
            else:
                self.deacts.append(employee)
        if len(self.deacts) > 0:
            self.list_box.insert(tk.END, '---DEACTIVATED EMPLOYEES---')
            for employee in self.deacts:
                self.list_box.insert(tk.END, f"{employee.fname} {employee.lname}")
    def goEdit(self):
        employee = None
        typed = self.list_box.get(tk.ANCHOR).replace(' ', '')
        if typed == '---DEACTIVATEDEMPLOYEES---':
            #Don't even bother if it's the header infomation
            return
        for item in self.employees:
            comb = f"{item.emp_id}{item.fname}{item.lname}"
            is_ok = typed.lower() in item.fname.lower() or typed.lower() in item.lname.lower() \
                    or typed.lower() in comb.lower() or typed.lower() in comb.lower()
            if is_ok:
                employee = item
                break
        self.frame.destroy()
        self.app = EditEmployee(self.master, self.user, employee)
    def goArchive(self):
        selected = self.list_box.get(tk.ANCHOR)
        if selected.replace(' ', '') != '' and selected.replace(' ', '') != '---DEACTIVATEDEMPLOYEES---':
            is_yes = messagebox.askyesno(f'Deactivate the employee?', 'Are you sure you want to deactivate the employee. If the employee is already deactivated it is reactivate the employee instead.')
            if is_yes:
                employee = None
                typed = self.list_box.get(tk.ANCHOR).replace(' ', '')
                if typed == '---DEACTIVATEDEMPLOYEES---':
                    #Don't even bother if it's the header infomation
                    return
                for row in self.employees:
                    item = Employee(row)
                    comb = f"{item.emp_id}{item.fname}{item.lname}"
                    is_ok = typed.lower() in item.fname.lower() or typed.lower() in item.lname.lower() \
                            or typed.lower() in comb.lower() or typed.lower() in comb.lower()
                    if is_ok:
                        employee = item
                        break
                rows =[]
                csvalchemy.singleton.archive_employee(employee)
                self.refresh_listbox()

                
    def generatePayslip(self):
        with open('payroll.txt', 'a') as file:
            messagebox.showinfo('Timecards', 'Please select a csv file for the timecards to be processed')
            f = self.open_datafiles()
            if f: 
                emps, totals = csvalchemy.singleton.process_timecards(f)
                for emp, total in zip(emps, totals):
                    if emp.bank_info == 'mm':
                        address = str(emp.address).replace('\n','')
                        file.write(f'Mailing {total} to {emp.fname} {emp.lname} at {address}\n')
                    else:
                        file.write(f'Transferred {total} for {emp.fname} {emp.lname} to {emp.acct_no} at {emp.route}\n')

            messagebox.showinfo('Receipts', 'Please select a csv file for the receipts to be processed')
            f = self.open_datafiles()
            if f:
                emps, totals = csvalchemy.singleton.proccess_receipts(f)
                for emp, total in zip(emps, totals):
                    if emp.bank_info == 'mm':
                        address = str(emp.address).replace('\n','')
                        file.write(f'Mailing {total} to {emp.fname} {emp.lname} at {address}\n')
                    else:
                        file.write(f'Transferred {total} for {emp.fname} {emp.lname} to {emp.acct_no} at {emp.route}\n')
            #generate payroll.txt
    def goAdd(self):
        self.frame.destroy()
        self.app = AddEmployee(self.master, self.user)
    def goEmp(self):
        #move on to the next window
        #1. Destory the current window
        
        #Must be initialized to variable or it will get dumped by the garbage collector
        #TODO Replace the employee with the searching for the user below
        #TODO which will have to perform a quick search
        employee = None
        typed = self.list_box.get(tk.ANCHOR).replace(' ', '')
        if typed == '---DEACTIVATEDEMPLOYEES---':
            #Don't even bother if it's the header infomation
            return
        for row in self.employees:
            item = Employee(row)
            comb = f"{item.emp_id}{item.fname}{item.lname}"
            is_ok = typed.lower() in item.fname.lower() or typed.lower() in item.lname.lower() \
                    or typed.lower() in comb.lower() or typed.lower() in comb.lower()
            if is_ok:
                employee = item
                break
        self.frame.destroy()
        self.app = SingleEmployeePrivate(self.master,self.user, employee)
    def open_datafiles(self):
        '''Open a csv file or text file for the admin'''
        # file type
        filetypes = (
            ('csv files', '*.csv'),
            ('text files', '*.txt')
        )
        # show the open file dialog
        f = fd.askopenfile(filetypes=filetypes)
        # read the text file and show its content on the Text
        return f
        

####NON_ADMIN####
class ViewEmployeeEmp():
    def __init__(self,master, employee_data) -> None:
        self.master = master
        self.master.title("View Employee Screen")
        self.master.geometry('1000x720')

        #TODO actually document this document
        #TODO Make the thing read once only 
        #TODO (cont) to make the page load more seemless
        self.frame =tk.Frame(width=1000, height=720)
        self.frame.grid(row=0, column=0)
        # In center of screen, create welcome message, username and password input boxes with username and password headings
        self.user: Employee = employee_data
   
        self.employees: list[Employee] = []
        filename = './employee.csv'
        if os.path.exists('./employeetemp.csv'):
            filename = './employeetemp.csv'
        with open(filename) as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                emp = Employee()
                emp.row_init(row)
                if emp.permission.lower() != 'admin':
                    self.employees.append(emp)
        
        self.usertitle = tk.Label(self.frame, text=f'Hello, {self.user.fname} {self.user.lname}', font=('Arial', 35), anchor=tk.W)
        self.usertitle.grid(row=0, column=0, padx=40)
        self.perm = tk.Label(self.frame, text=f'Permission:{self.user.permission.upper()}', font=('Arial', 25), anchor=tk.E)
        self.perm.grid(row=1,column=0,pady=10, padx=40)

        self.edit_emp_btn = tk.Button(self.frame, text="Edit Your Details", command=self.goEdit, font=('Arial', 15))
        self.edit_emp_btn.grid(row=3, column=0,pady=10)


        self.emp_title = tk.Label(self.frame, text="Employee list", font=('Arial', 50))
        self.emp_title.grid(row=0, column=1, columnspan=3)


        self.emp_title = tk.Label(self.frame, text="🔍", font=('Arial', 25))
        self.emp_title.grid(row=1, column=1, padx=0)
        self.search_var = tk.StringVar()#search value to be stored in here
        self.search_entry = tk.Entry(self.frame, textvariable=self.search_var, width=30, font=('Arial', 25))
        self.search_entry.grid(row=1, column=2, padx=0, sticky=tk.NSEW)
    
        
        self.scroll = tk.Scrollbar(self.frame)
        self.scroll.grid(row=2, column=3, sticky=tk.NS)

        self.list_box = tk.Listbox(self.frame, height=15,yscrollcommand=self.scroll.set, font=('Arial', 25))
        for employee in self.employees:
            self.list_box.insert(tk.END, f"{employee.fname} {employee.lname}")
        self.list_box.grid(row=2, column=1, columnspan=2, sticky=(tk.W + tk.E))
        self.list_box.activate(0)

        

        self.go_to_emp = tk.Button(self.frame, text="View Your Details", command=self.goEmpSelf, font=('Arial', 15))
        self.go_to_emp.grid(row=3, column=1, columnspan=2, pady=10)
        self.go_to_emp = tk.Button(self.frame, text="View Employee", command=self.goEmpPub, font=('Arial', 15))
        self.go_to_emp.grid(row=4, column=1, columnspan=2, pady=10)
        self.scroll.config(command=self.list_box.yview)

        #Binding for events such as when the listbox element is selected and when we type in the search box
        self.list_box.bind('<<ListboxSelect>>', self.fillout)
        self.search_entry.bind("<KeyRelease>", self.update_search)

    def fillout(self,event):
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, self.list_box.get(tk.ANCHOR))
    def update_search(self, event):
        data = None
        #removing whitespace, which is annoying to deal with
        typed = self.search_var.get().replace(' ', '')
        if typed == '':
            #If there nothing but spaces or empty box, then just put everything back
            data = self.employees
        else:
            #TODO Chagne this into a search funciton in the CSV writer class
            #Otherwise do a simple search
            data = []
            for item in self.employees:
                comb = f"{item.emp_id}{item.fname}{item.lname}"
                is_ok = typed.lower() in item.fname.lower() or typed.lower() in item.lname.lower() \
                        or typed.lower() in comb.lower() or typed.lower() in comb.lower()
                if is_ok:
                    data.append(item)
        #clear the listbox first
        self.list_box.delete(0, tk.END)
        #Enter in the filtered results
        for emp in data:
            self.list_box.insert(tk.END, f"{emp.fname} {emp.lname}")
        
    def goEdit(self):
        employee = self.user
        self.frame.destroy()
        self.app = EditEmployee(self.master, self.user, self.user)
    def goEmpSelf(self):
        #move on to the next window
        #1. Destory the current window
        
        #Must be initialized to variable or it will get dumped by the garbage collector
        #TODO Replace the employee with the searching for the user below
        #TODO which will have to perform a quick search
        employee = self.user
        self.frame.destroy()
        self.app = SingleEmployeePrivate(self.master,self.user, employee)
    def goEmpPub(self):
        #move on to the next window
        #1. Destory the current window
        
        #Must be initialized to variable or it will get dumped by the garbage collector
        #TODO Replace the employee with the searching for the user below
        #TODO which will have to perform a quick search
        employee = None
        typed = self.list_box.get(tk.ANCHOR).replace(' ', '')
        for item in self.employees:
            comb = f"{item.emp_id}{item.fname}{item.lname}"
            is_ok = typed.lower() in item.fname.lower() or typed.lower() in item.lname.lower() \
                    or typed.lower() in comb.lower() or typed.lower() in comb.lower()
            if is_ok:
                employee = item
                break
        self.frame.destroy()
        self.app = SingleEmployeePub(self.master,self.user, employee)

if __name__ == '__main__':
    window = tk.Tk()
    emp_data = None
    with open('./employee.csv') as file:
            reader = csv.reader(file)
            for i,row in enumerate(reader):
                if i == 0:
                    continue
                else:
                    emp_data = row
                    break
    employee = Employee()
    employee.row_init(emp_data)
    frame = ViewEmployeeAdmin(window, employee)
    window.mainloop()

            