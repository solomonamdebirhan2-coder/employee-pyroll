"""Functions for registering, finding, updating and saving employees."""

import json
import math
from pathlib import Path
from employee import Employee

DATA_FILE = Path(__file__).with_name("employees.txt")


def load_employees():
    """Read employee dictionaries from the JSON-formatted text file."""
    if not DATA_FILE.exists():
        return {}
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            print("Employee data must be a JSON dictionary.")
            return {}
        # Keep the ID both as the dictionary key and inside each employee record.
        for employee_id, details in data.items():
            if isinstance(details, dict):
                details.setdefault("employee_id", employee_id)
        return data
    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not load employee records: {error}")
        return {}


def save_employees(employees):
    """Write all employee dictionaries to employees.txt as JSON."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(employees, file, indent=4)
        print("Employee records saved.")
    except OSError as error:
        print(f"Could not save employee records: {error}")


def read_text(prompt):
    """Read a required text value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def read_amount(prompt):
    """Read a numeric salary or allowance that is finite and nonnegative."""
    while True:
        try:
            amount = float(input(prompt))
            if math.isfinite(amount) and amount >= 0:
                return amount
            print("Enter a finite amount that is zero or greater.")
        except ValueError:
            print("Enter a valid number.")


def add_employee(employees):
    """Register a new employee after checking for a duplicate ID."""
    print("\n--- Register New Employee ---")
    employee_id = read_text("Employee ID: ").upper()
    if employee_id in employees:
        print("That employee ID already exists.")
        return

    full_name = read_text("Full name: ")
    department = read_text("Department: ")
    position = read_text("Position: ")
    basic = read_amount("Basic salary: ")
    house = read_amount("House allowance: ")
    transport = read_amount("Transport allowance: ")
    other = read_amount("Other allowance: ")

    employee = Employee(
        employee_id, full_name, department, position,
        basic, house, transport, other
    )
    employees[employee_id] = employee.to_dict()
    save_employees(employees)
    print("Employee registered successfully.")


def display_employees(employees):
    """Display the basic details of every employee."""
    if not employees:
        print("\nNo employee records found.")
        return

    print("\n--- Employee Records ---")
    for employee_id, details in employees.items():
        print("-" * 40)
        print(f"ID: {details.get('employee_id', employee_id)}")
        print(f"Name: {details.get('full_name', '')}")
        print(f"Department: {details.get('department', '')}")
        print(f"Position: {details.get('position', '')}")
        print(f"Basic salary: {float(details.get('basic_salary', 0)):,.2f}")
    print("-" * 40)
    print(f"Total employees: {len(employees)}")


def search_employee(employees):
    """Find an employee using their ID."""
    employee_id = input("Enter employee ID: ").strip().upper()
    details = employees.get(employee_id)
    if details is None:
        print("Employee not found.")
        return

    print("\n--- Employee Details ---")
    for field, value in details.items():
        print(f"{field.replace('_', ' ').title()}: {value}")


def update_employee(employees):
    """Update employee text and salary fields; Enter keeps the old value."""
    employee_id = input("Enter employee ID to update: ").strip().upper()
    details = employees.get(employee_id)
    if details is None:
        print("Employee not found.")
        return

    print("Press Enter to keep the current value.")
    for field, label in (
        ("full_name", "Full name"),
        ("department", "Department"),
        ("position", "Position"),
    ):
        value = input(f"{label} [{details.get(field, '')}]: ").strip()
        if value:
            details[field] = value

    for field, label in (
        ("basic_salary", "Basic salary"),
        ("house_allowance", "House allowance"),
        ("transport_allowance", "Transport allowance"),
        ("other_allowance", "Other allowance"),
    ):
        while True:
            value = input(f"{label} [{details.get(field, 0)}]: ").strip()
            if not value:
                break
            try:
                amount = float(value)
                if not math.isfinite(amount) or amount < 0:
                    print("Enter a finite amount that is zero or greater.")
                    continue
                details[field] = amount
                break
            except ValueError:
                print("Enter a valid number.")

    details["employee_id"] = employee_id
    save_employees(employees)
    print("Employee updated successfully.")


def delete_employee(employees):
    """Delete an employee only after confirmation."""
    employee_id = input("Enter employee ID to delete: ").strip().upper()
    if employee_id not in employees:
        print("Employee not found.")
        return
    confirm = input("Delete this employee? (y/n): ").strip().lower()
    if confirm == "y":
        del employees[employee_id]
        save_employees(employees)
        print("Employee deleted.")
    else:
        print("Deletion cancelled.")
