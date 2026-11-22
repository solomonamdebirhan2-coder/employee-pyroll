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
| 4 | Brhanu Kasahun | TTBR/0030/18 | Initial administrator and approval workflow design |

## 1. Introduction

The Employee Payroll Management System is a Python application developed to manage employee information and calculate monthly payroll. It helps an organization register employees, maintain employee records, control access by role, and process information changes through an approval workflow.

## 2. Objectives

- Register and maintain employee information.
- Store employee records in a file using JSON.
- Search and display employee records, and process updates or deactivation through an approval workflow.
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
- **hashlib and hmac:** Store and verify salted password hashes.
- **secrets:** Generates temporary passwords.
- **getpass:** Collects passwords without displaying typed characters.

## 4. Main System Features

1. Register a new employee after demonstration OTP verification and create a temporary-password account.
2. Authenticate users with employee ID and password; require a password change at first login.
3. Provide separate administrator and employee menus.
4. Allow administrators to view all employee records, search employees, register employees, and view organization payroll.
5. Allow employees to view only their own profile and payroll.
6. Require employee-submitted information changes and deactivation requests to be approved by an administrator.
7. Require administrator-submitted changes and deactivation requests to be approved by the specific affected employee.
8. Preserve employee records when an account is deactivated.
9. Maintain request status and decision history.
10. Allow administrators to grant or revoke limited special permissions for individual employee accounts.

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

Employee records are stored in employees.txt as JSON data. The project requires a minimum of 10 employee records. The application loads records at startup and saves approved changes. Authentication hashes are stored in accounts.txt, while request and approval history is stored in requests.txt. The account and request files are generated locally and excluded from Git.

## 7. Testing

The payroll display was previously checked with 10 employee records. The security modules passed nine automated tests covering first-time administrator setup, temporary employee accounts, password hashing and password changes, permission granting and revocation, both approval directions, prevention of self-approval, rejection without data changes, duplicate request prevention, and account deactivation without hard deletion. Python syntax compilation passed for main.py, auth.py, and request_manager.py.

The example payroll calculation produced gross salary of 20,000, pension of 1,050, income tax of 4,950, and net salary of 14,000.

## 8. Conclusion

The Employee Payroll Management System demonstrates how Python can be used to manage employee records, authenticate users, enforce role-based access, and automate payroll calculations. It includes input validation, JSON file storage, separate administrator and employee menus, password hashing, and a two-way request-and-approval workflow. The current version is an educational local-file application and can be extended with a database and graphical interface.
