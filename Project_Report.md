# ABC Government Organization
# Employee Payroll Management System
## Project Report

**Project Type:** Python menu-driven Employee Payroll Management System

## Group Information

**Group Name:** To be completed by the group  
**Course/Section:** To be completed by the group  
**Instructor:** To be completed by the group  
**Submission Date:** To be completed by the group

## Group Members and Contributions

| No. | Full Name | Student ID | Contribution |
|---:|---|---|---|
| 1 | Solomon Amdebirhan | Omitted from public copy | To be confirmed by the group |
| 2 | Solomon Mesfin | Omitted from public copy | To be confirmed by the group |
| 3 | Asres Muntaye | Omitted from public copy | To be confirmed by the group |
| 4 | Brhanu Kasahun | Omitted from public copy | To be confirmed by the group |

## 1. Introduction

The Employee Payroll Management System is a Python application for managing employee information and calculating monthly salaries for ABC Government Organization. It uses a menu-driven terminal interface and stores employee records as JSON-formatted data in employees.txt.

## 2. Objectives

- Register and maintain employee information.
- Save and load employee records using file handling.
- Display and search employee records by employee ID.
- Update and delete employee records.
- Calculate gross salary, pension, income tax and net salary.
- Display the payroll of all employees.

## 3. Technologies and Python Concepts

- **Python:** main programming language.
- **Dictionary:** stores each employee's information, using employee ID as the key.
- **JSON and file handling:** save and read records in employees.txt.
- **Functions:** organize registration, searching, updating, deleting and payroll tasks.
- **Conditionals and loops:** control menu choices and validate user input.
- **Arithmetic operations:** calculate gross salary, pension, tax and net salary.

No third-party Python packages are required.

## 4. Project Structure

| File | Responsibility |
|---|---|
| main.py | Main menu and application flow |
| employee.py | Employee class and employee dictionary conversion |
| employee_manager.py | Register, save, display, search, update and delete employees |
| payroll.py | Gross salary, pension, income tax and payroll reports |
| employees.txt | Employee records stored in JSON format |
| README.md | Setup and usage instructions |

The application is separated into modules to make the code easier to understand, test and maintain.

## 5. Main Menu and Features

1. Register New Employee
2. Save Employee Information
3. Display All Employees
4. Search Employee by ID
5. Update Employee Information
6. Delete Employee Record
7. Calculate Employee Gross Salary
8. Display All Employees' Payroll
9. Exit

Each employee dictionary contains employee_id, full_name, department, position, basic_salary, house_allowance, transport_allowance and other_allowance. Additional personal information fields may also be stored.

The program rejects duplicate employee IDs, invalid or negative salary values, and displays a clear message when a requested employee ID does not exist.

## 6. Payroll Calculation

**Gross Salary**

Gross Salary = Basic Salary + House Allowance + Transport Allowance + Other Allowance

**Pension**

Pension = Basic Salary × 7%

**Monthly Income Tax**

| Gross Salary | Tax Rate | Deduction |
|---|---:|---:|
| 0–2,000 | 0% | 0 |
| 2,001–4,000 | 15% | 300 |
| 4,001–7,000 | 20% | 500 |
| 7,001–10,000 | 25% | 850 |
| 10,001–14,000 | 30% | 1,350 |
| Above 14,000 | 35% | 2,050 |

Income Tax = (Gross Salary × Tax Rate) − Deduction

**Net Salary**

Net Salary = Gross Salary − Pension − Income Tax

**Official Assignment Example**

For basic salary 15,000 ETB, house allowance 3,000 ETB, transport allowance 1,500 ETB and other allowance 500 ETB:

- Gross salary = 15,000 + 3,000 + 1,500 + 500 = **20,000 ETB**
- Pension = 15,000 × 7% = **1,050 ETB**
- Income tax = (20,000 × 35%) − 2,050 = **4,950 ETB**
- Net salary = 20,000 − 1,050 − 4,950 = **14,000 ETB**

**Calculation note:** The assignment brief states 13,950 ETB as the net result, but its own gross salary, pension and income-tax figures produce 14,000 ETB. This report follows the stated formula and arithmetic.

## 7. Data Storage

Employee records are stored in employees.txt as JSON. The application loads the employee dictionary when it starts and saves changes after registration, updating, deletion, when the user selects Save Employee Information, and before exiting.

The public sample data file contains 10 fictional employee records. Replace them with approved assignment data for local demonstration.

## 8. Testing

The project should be tested for:
- Loading and saving employee records.
- Registering a new employee and rejecting a duplicate ID.
- Displaying all employees.
- Searching for an existing and a nonexistent employee ID.
- Updating an employee's salary.
- Deleting an employee and handling a nonexistent ID.
- Correct gross salary, pension, income tax and net salary calculations.
- Invalid menu choices and invalid or negative salary inputs.

Screenshots of the menu options and invalid-input handling should be added before submission.

## 9. Conclusion

The Employee Payroll Management System demonstrates Python dictionaries, functions, file handling, loops, conditionals and arithmetic operations. It provides the employee management and payroll features required by the assignment through a simple menu-driven application.
