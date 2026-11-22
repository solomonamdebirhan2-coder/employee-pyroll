# ABC Government Organization
# Employee Payroll Management System
## Project Report

**Project Type:** Employee Payroll Management System

## Group Members and Contributions

| No. | Full Name | Student ID | Contribution |
|---:|---|---|---|
| 1 | Solomon Amdebirhan | TTBR/0226/18 | |
| 2 | Solomon Mesfin | TTBR/0227/18 | |
| 3 | Asres Muntaye | TTBR/0010/18 | |
| 4 | Brhanu | To be filled | |

## 1. Introduction

The Employee Payroll Management System is a Python application developed to manage employee information and calculate monthly payroll. It helps an organization register employees, maintain employee records, update or delete information, and calculate salary payments.

## 2. Objectives

- Register and maintain employee information.
- Store employee records in a file using JSON.
- Search, display, update, and delete employee records.
- Calculate gross salary, pension, income tax, and net salary.
- Reduce manual payroll calculation errors.

## 3. Technologies and Libraries

- **Python:** Main programming language.
- **json:** Saves and loads employee records in JSON format.
- **random:** Generates a demonstration one-time password (OTP).
- **time:** Checks OTP expiration time.
- **math:** Validates finite numeric salary values.
- **re:** Validates text, phone numbers, and email addresses.
- **datetime:** Validates dates of birth and calculates employee age.

## 4. Main System Features

1. Register a new employee after demonstration OTP verification.
2. Save employee records to employees.txt.
3. Display all employee records.
4. Search for an employee using an employee ID.
5. Update employee information and automatically save changes.
6. Delete an employee after confirmation and automatically save changes.
7. Calculate an individual employee's gross salary.
8. Display payroll details for all employees.
9. Exit the application.

The employee record includes employee ID, full name, date of birth, age, phone number, email, department, position, basic salary, and allowances.

## 5. Payroll Calculation

**Gross Salary**

Gross Salary = Basic Salary + House Allowance + Transport Allowance + Other Allowance

**Pension**

Pension = Basic Salary × 7%

**Income Tax**

The system applies the assignment's monthly tax brackets:

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

**Example**

For an employee with basic salary of 15,000, house allowance of 2,000, transport allowance of 2,000, and other allowance of 1,000:

- Gross salary = 20,000
- Pension = 15,000 × 7% = 1,050
- Income tax = (20,000 × 35%) − 2,050 = 4,950
- Net salary = 20,000 − 1,050 − 4,950 = **14,000**

## 6. Data Storage

Employee records are stored in employees.txt as JSON data. The project requires a minimum of 10 employee records to be registered and saved in this file. The application loads the records when it starts and saves changes when the user selects the save option, updates an employee, or confirms deletion.

## 7. Testing

The application was run and checked with 10 employee records. The payroll display test confirmed that the system calculated gross salary, 7% pension, income tax, net salary, and payroll totals. The Python syntax check also passed.

The example payroll calculation produced gross salary of 20,000, pension of 1,050, income tax of 4,950, and net salary of 14,000.

## 8. Conclusion

The Employee Payroll Management System demonstrates how Python can be used to manage employee records and automate payroll calculations. It includes input validation, JSON file storage, employee management operations, and payroll reporting. The project provides a foundation that could be extended with a database, user authentication, and a graphical interface in the future.
