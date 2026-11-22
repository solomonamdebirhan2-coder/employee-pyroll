# Employee Payroll Management System

A simple Python terminal application for ABC Government Organization. It manages employee dictionaries and calculates monthly payroll.

## Requirements
- Python 3.10 or newer
- No third-party packages are required

## Run the application
Open PowerShell or a terminal in this project folder and run:

```powershell
python main.py
```

## Project files
- `main.py` - displays the required 1–9 menu and controls the program.
- `employee.py` - defines the Employee class and converts an employee to a dictionary.
- `employee_manager.py` - registers, searches, displays, updates, deletes, loads and saves employee records.
- `payroll.py` - calculates gross salary, pension, income tax and net salary.
- `employees.txt` - stores employee dictionaries in JSON format.
- `Project_Report.md` - project report.

## Assignment menu
1. Register New Employee
2. Save Employee Information
3. Display All Employees
4. Search Employee by ID
5. Update Employee Information
6. Delete Employee Record
7. Calculate Employee Gross Salary
8. Display All Employees' Payroll
9. Exit

## Payroll rules
- Gross salary = basic salary + house allowance + transport allowance + other allowance.
- Pension = 7% of basic salary.
- Income tax is calculated using the assignment's gross-salary brackets.
- Net salary = gross salary - pension - income tax.

The program loads saved records at startup and saves records after changes and when the user exits. No login or web interface is required by this assignment.

## Sample data and privacy
The included employees.txt contains fictional sample employee records only. Do not commit real employee names, phone numbers, email addresses, salary records, or other private information to a public repository.
