# Employee Payroll Management System — Web Portal

## Current implementation

The project has a private Flask web portal and retains the original terminal application.

### Web features
- Private employee-ID/password login; no public self-registration.
- First-login temporary password change and normal password changes.
- Employee dashboard limited to the signed-in employee.
- Administrator dashboard and organization payroll overview.
- Employee registration with generated temporary password.
- Employee search and permission-separated record/payroll visibility.
- Employee change and deactivation requests.
- Two-way approvals: employee requests require administrator approval; administrator requests require approval from the specific affected employee.
- Special permissions for selected employees.
- Gross/net payroll calculations using the assignment tax and pension rules.
- Request history and administrator-only audit trail.
- CSRF tokens, HTTP-only/SameSite cookies, session expiry, login throttling, and salted PBKDF2 password hashes.

## Run locally on Windows

From PowerShell:

```powershell
cd C:\Users\HP\Desktop\Employee_Payroll_System
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 on the same computer.

The terminal version remains available with `python main.py`.

## Local JSON and hosted PostgreSQL

Local development uses:
- `employees.txt`
- `accounts.txt`
- `requests.txt`

Hosted mode uses PostgreSQL when the `DATABASE_URL` environment variable is configured. The employee, account, and request services automatically use PostgreSQL in that mode.

Before importing anything, create a private PostgreSQL database and set its connection string as `DATABASE_URL`. Then run:

```powershell
python migrate_to_postgres.py --confirm
```

This command copies employee personal information, password hashes, and request history to the configured database. It refuses to overwrite a non-empty database. Only run it after verifying the database destination and obtaining authorization to transfer the data. Keep secure backups of the local JSON files.

Never commit `employees.txt`, `accounts.txt`, `requests.txt`, `audit_log.txt`, `.flask_secret`, or database credentials.

## Deploying privately on Render

1. Create a private PostgreSQL database in your hosting account.
2. Create a web service from this repository using the included `render.yaml`.
3. Set `DATABASE_URL` to the database's **internal** connection string.
4. Keep the generated `SECRET_KEY`; keep `COOKIE_SECURE=1`.
5. Before real employee login, connect to the hosted service's environment and run the migration command once. Do not run the import twice.
6. Verify HTTPS, admin login, employee login, permissions, approval flows, and backups before inviting employees.

The deployment configuration uses one Gunicorn worker and one thread because the current JSON-era service functions perform read/modify/write operations. This is a conservative initial deployment, not a high-concurrency architecture. A larger organization should move each operation to database transactions and add database-level audit retention, automated backups, monitoring, and external rate limiting.

## Verification

Run:

```powershell
python -m py_compile app.py web_features.py storage.py audit_log.py auth.py request_manager.py main.py
python -m unittest discover -s tests -v
git diff --check
```

The current automated suite covers security workflows and web access control. Do not expose the site publicly until the hosted database is configured, data migration is explicitly authorized, and deployment checks are completed.
