"""Authentication and role-based access for the payroll application."""
import hashlib
import hmac
import json
import secrets
from pathlib import Path
from getpass import getpass

ACCOUNT_FILE = Path("accounts.txt")
ADMIN_ID = "TTBR/0030/18"
ITERATIONS = 240_000


def _hash_password(password, salt=None):
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return salt.hex(), digest.hex()


def _load_accounts():
    if not ACCOUNT_FILE.exists():
        return {}
    try:
        data = json.loads(ACCOUNT_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        raise RuntimeError("accounts.txt is unreadable or contains invalid JSON. Do not overwrite it.")


def _save_accounts(accounts):
    temporary = ACCOUNT_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(accounts, indent=4), encoding="utf-8")
    temporary.replace(ACCOUNT_FILE)


def _valid_password(password):
    return (
        len(password) >= 8
        and any(c.islower() for c in password)
        and any(c.isupper() for c in password)
        and any(c.isdigit() for c in password)
    )


def _new_account(role, password, must_change=False):
    salt, digest = _hash_password(password)
    return {
        "role": role,
        "salt": salt,
        "password_hash": digest,
        "must_change_password": must_change,
        "active": True,
        "permissions": [],
    }


def initialize_accounts(employee_ids):
    """Create first admin and one-time temporary passwords for existing employees."""
    accounts = _load_accounts()
    if accounts:
        return accounts

    if ADMIN_ID not in employee_ids:
        raise RuntimeError(
            f"First administrator {ADMIN_ID} is not present in employees.txt. "
            "Correct the employee record before initializing accounts."
        )

    print("\n=== FIRST-TIME SECURITY SETUP ===")
    print(f"Create the administrator password for {ADMIN_ID} (Brhanu Kasahun).")
    while True:
        password = getpass("New administrator password: ")
        if not _valid_password(password):
            print("Use at least 8 characters with uppercase, lowercase, and a number.")
            continue
        confirmation = getpass("Confirm administrator password: ")
        if password != confirmation:
            print("Passwords do not match.")
            continue
        break

    accounts[ADMIN_ID] = _new_account("ADMIN", password)

    print("\nOne-time temporary passwords for existing employees:")
    print("Give each password privately to its matching employee.")
    for employee_id in employee_ids:
        if employee_id == ADMIN_ID:
            continue
        temporary_password = secrets.token_urlsafe(9)
        accounts[employee_id] = _new_account("USER", temporary_password, True)
        print(f"{employee_id}: {temporary_password}")

    _save_accounts(accounts)
    print("\nAccounts initialized. Temporary passwords are not saved in plain text.")
    return accounts


def create_employee_account(employee_id):
    accounts = _load_accounts()
    if employee_id in accounts:
        raise ValueError("An account already exists for this employee.")
    temporary_password = secrets.token_urlsafe(9)
    accounts[employee_id] = _new_account("USER", temporary_password, True)
    _save_accounts(accounts)
    return temporary_password


def authenticate(employee_id, password):
    accounts = _load_accounts()
    account = accounts.get(employee_id)
    if not account or not account.get("active", False):
        return None
    try:
        salt = bytes.fromhex(account["salt"])
        expected = account["password_hash"]
    except (KeyError, ValueError):
        return None
    _, actual = _hash_password(password, salt)
    if hmac.compare_digest(actual, expected):
        return {"employee_id": employee_id, "role": account["role"],
                "must_change_password": account.get("must_change_password", False)}
    return None


def change_password(employee_id, new_password):
    if not _valid_password(new_password):
        raise ValueError("Use at least 8 characters with uppercase, lowercase, and a number.")
    accounts = _load_accounts()
    if employee_id not in accounts:
        raise ValueError("Account not found.")
    accounts[employee_id]["salt"], accounts[employee_id]["password_hash"] = _hash_password(new_password)
    accounts[employee_id]["must_change_password"] = False
    _save_accounts(accounts)


def set_account_active(employee_id, active):
    accounts = _load_accounts()
    if employee_id in accounts:
        accounts[employee_id]["active"] = bool(active)
        _save_accounts(accounts)


AVAILABLE_PERMISSIONS = {
    "VIEW_ALL_EMPLOYEES": "View all employee records",
    "SEARCH_EMPLOYEES": "Search employee records",
    "VIEW_ALL_PAYROLL": "View organization-wide payroll",
    "CALCULATE_GROSS_SALARY": "Calculate gross salary for an employee",
    "REGISTER_EMPLOYEE": "Register new employees",
}


def get_account_permissions(employee_id):
    account = _load_accounts().get(employee_id)
    if not account:
        return []
    return list(account.get("permissions", []))


def update_account_permissions(actor_id, employee_id, permission, grant=True):
    if permission not in AVAILABLE_PERMISSIONS:
        raise ValueError("Unknown special permission.")
    accounts = _load_accounts()
    if actor_id not in accounts or accounts[actor_id].get("role") != "ADMIN":
        raise PermissionError("Only an administrator can grant or revoke special permissions.")
    if employee_id not in accounts or accounts[employee_id].get("role") != "USER":
        raise ValueError("Special permissions can only be assigned to an existing employee account.")
    current = set(accounts[employee_id].get("permissions", []))
    if grant:
        current.add(permission)
    else:
        current.discard(permission)
    accounts[employee_id]["permissions"] = sorted(current)
    _save_accounts(accounts)
    return sorted(current)
