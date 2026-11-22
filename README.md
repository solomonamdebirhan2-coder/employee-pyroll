# Employee Payroll Management System

A Python console application for employee records, payroll calculations, secure login, role-based menus, and two-way change approvals.

## Project files
- `main.py`: Existing payroll application and role-specific menus.
- `auth.py`: Password hashing, authentication, temporary passwords, and account status.
- `request_manager.py`: Employee change/deactivation requests and approval workflow.
- `employees.txt`: Employee records stored as JSON (assignment sample data).
- `tests/test_security.py`: Automated tests for authentication and approval rules.
- `Project_Report.md`: Project report.

## First run
1. Run `python main.py` from this folder.
2. The first-time setup asks you to create the administrator password for Brhanu Kasahun (`TTBR/0030/18`).
3. The setup generates one-time temporary passwords for the other existing employees and displays them once in the terminal. Give each password privately to its matching employee.
4. Each employee signs in with their employee ID and temporary password, then must set a new password.
5. Future logins use the employee ID and the new password.

New employees registered by the administrator also receive a generated temporary password, which must be given to them privately.

## Roles
- **Administrator:** Can register employees, view all employee records, search employees, calculate gross salary, and view all payroll. Changes to another employee's information or account status must be submitted as requests and approved by that specific employee.
- **Employee:** Can view only their own profile and payroll, submit requests to change their own information or deactivate their account, view their request history, and review administrator requests concerning their own record. An administrator may grant or revoke specific additional permissions: viewing all employee records, searching employees, viewing organization-wide payroll, calculating another employee's gross salary, or registering new employees.

## Two-way approval
- Employee-submitted changes/deactivation requests require administrator approval.
- Administrator-submitted changes/deactivation requests require approval from the specific affected employee.
- The requester cannot approve their own request.
- Changes are applied only after approval. Deactivation preserves the employee record and marks the account inactive.

## Security and local data
Passwords are stored as salted PBKDF2-HMAC-SHA256 hashes, not plain text. `accounts.txt` and `requests.txt` are generated locally and excluded from Git by `.gitignore`. Do not share account files or temporary passwords. This is an educational local-file application; production deployment would require stronger operational controls, backups, access logging, and a database.

## Run tests
```powershell
python -m unittest discover -s tests -v
```
