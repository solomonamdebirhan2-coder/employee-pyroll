# ABC Government Organization
# Employee Payroll Management System
# i will build this application step by step.
# 1. Import required libraries
import json
import random
import time
import math
import re
from datetime import date, datetime
# 2. Create employee database
employees = {}
# OTP verification function
def verify_employee_otp():

    # Generate a random 6-digit OTP
    otp = random.randint(100000, 999999)

    # Record the generation time
    generated_time = time.time()

    # Display OTP for demo purposes
    print("\nYour demo OTP is:", otp)
    print("This OTP expires after 60 seconds.")

    # Ask employee to enter OTP
    entered_otp = input("Enter your OTP: ")

    # Check expiration time
    current_time = time.time()

    if current_time - generated_time > 60:
        print("OTP expired. Please request a new OTP.")
        return False

    # Check whether OTP is correct
    if entered_otp == str(otp):
        print("OTP verified successfully!")
        return True

    else:
        print("Incorrect OTP.")
        return False
# 3. Register employee function
# Validate first name and last name
def get_valid_name(prompt, field_name):

    while True:
        name = input(prompt).strip()

        if name == "":
            print(f"{field_name} cannot be empty.")

        elif not name.isalpha():
            print(f"{field_name} must contain letters only. Do not enter spaces or numbers.")

        else:
            return name
# Collect and validate date of birth
def get_valid_dob():

    while True:
        dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()

        try:
            birth_date = datetime.strptime(dob, "%Y-%m-%d").date()

            if birth_date >= date.today():
                print("Date of birth must be earlier than today.")
                continue

            age = calculate_age(birth_date)

            if age < 18 or age > 100:
                print("Employee age must be between 18 and 100.")
            else:
                return birth_date

        except ValueError:
            print("Invalid date! Use YYYY-MM-DD, for example 2002-05-15.")


# Calculate age automatically from date of birth
def calculate_age(birth_date):

    today = date.today()
    age = today.year - birth_date.year

    # Subtract one if the birthday has not happened this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age
# Validate department and position (allow multiple words)
def get_valid_text(prompt, field_name):
    while True:
        value = input(prompt).strip()

        if value == "":
            print(f"{field_name} cannot be empty.")
        elif not re.fullmatch(r"[A-Za-z]+(?:[ '&-][A-Za-z]+)*", value):
            print(f"{field_name} must contain words only. Numbers and invalid symbols are not allowed.")
        else:
            return value


# Validate employee ID and prevent duplicates
def get_valid_employee_id():

    while True:
        employee_id = input("Enter Employee ID: ").strip().upper()

        if employee_id == "":
            print("Employee ID cannot be empty.")

        elif any(existing_id.upper() == employee_id for existing_id in employees):
            print("This Employee ID already exists. Enter a different ID.")

        else:
            return employee_id


# Validate and normalize Ethiopian mobile phone numbers
def get_valid_phone():
    while True:
        phone = input("Enter Phone Number: ").strip()

        # Allow users to type spaces or hyphens for readability
        phone = phone.replace(" ", "").replace("-", "")

        # Convert local format to international format
        if phone.startswith("09") or phone.startswith("07"):
            phone = "+251" + phone[1:]
        elif phone.startswith("2519") or phone.startswith("2517"):
            phone = "+" + phone

        # Check the final international format
        if len(phone) == 13 and phone.startswith(("+2519", "+2517")) and phone[1:].isdigit():
            return phone
        else:
            print("Invalid phone number. Use 09XXXXXXXX, 07XXXXXXXX, or +2519XXXXXXXX / +2517XXXXXXXX.")


# Validate employee email address
def get_valid_email():
    while True:
        email = input("Enter Email Address: ").strip()

        # Check the basic structure: name@domain.extension
        pattern = r"[A-Za-z0-9][A-Za-z0-9._%+-]*@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"

        if email == "":
            print("Email address cannot be empty.")
        elif not re.fullmatch(pattern, email):
            print("Invalid email. Example: employee@gmail.com")
        else:
            return email


# Validate salary and allowance amounts
def get_valid_salary(prompt):

    while True:
        value = input(prompt).strip()

        if value == "":
            print("This field cannot be empty.")
            continue

        try:
            amount = float(value)

            if not math.isfinite(amount):
                print("Please enter a valid finite number.")
            elif amount < 0:
                print("Amount cannot be negative.")
            else:
                return amount

        except ValueError:
            print("Invalid input! Please enter numbers only.")


def register_employee():
    print("\n--- Employee Identity Verification ---")

    if not verify_employee_otp():
        print("Registration cancelled. Identity verification failed.")
        return
    employee_id = get_valid_employee_id()

    # Collect first name and last name separately
    first_name = get_valid_name("Enter First Name: ", "First name")
    last_name = get_valid_name("Enter Last Name: ", "Last name")

    # Automatically create full name
    full_name = first_name + " " + last_name

    # Collect date of birth and calculate age
    date_of_birth = get_valid_dob()
    age = calculate_age(date_of_birth)

    # Collect and validate phone number
    phone = get_valid_phone()

    # Collect and validate email address
    email = get_valid_email()

    department = get_valid_text("Enter Department: ", "Department")
    position = get_valid_text("Enter Position: ", "Position")

    # Collect salary and allowances with validation
    basic_salary = get_valid_salary("Enter Basic Salary: ")
    house_allowance = get_valid_salary("Enter House Allowance: ")
    transport_allowance = get_valid_salary("Enter Transport Allowance: ")
    other_allowance = get_valid_salary("Enter Other Allowance: ")

    employees[employee_id] = {
        "full_name": full_name,
        "date_of_birth": date_of_birth.isoformat(),
        "age": age,
        "phone": phone,
        "email": email,
        "department": department,
        "position": position,
        "basic_salary": basic_salary,
        "house_allowance": house_allowance,
        "transport_allowance": transport_allowance,
        "other_allowance": other_allowance
    }

    print("Employee registered successfully!")

# 4. Save employee information function
def save_employees():
    try:
        with open("employees.txt", "w") as file:
            json.dump(employees, file, indent=4)

        print("Employee information saved successfully!")

    except OSError as error:
        print("Could not save employee information:", error)

# 5. Load employee information from the file
def load_employees():
    global employees

    try:
        with open("employees.txt", "r") as file:
            loaded_data = json.load(file)

        if isinstance(loaded_data, dict):
            employees = loaded_data
            print("Employee information loaded successfully!")
        else:
            employees = {}
            print("Invalid employee data format. Starting with an empty database.")

    except FileNotFoundError:
        employees = {}
        print("No saved employee file found. Starting with an empty database.")

    except json.JSONDecodeError:
        employees = {}
        print("The employee file contains invalid JSON. Starting with an empty database.")

    except OSError as error:
        employees = {}
        print("Could not load employee information:", error)


# 6. Display all employees function
def display_employees():

    # Check whether the employee database is empty
    if not employees:
        print("\nNo employee records found.")
        return

    print("\n========== ALL EMPLOYEE RECORDS ==========")

    # Visit each employee record in the dictionary
    for employee_id, details in employees.items():
        print("\n------------------------------------------")
        print("Employee ID:", employee_id)
        print("Full Name:", details.get("full_name", "Not available"))
        print("Date of Birth:", details.get("date_of_birth", "Not available"))
        print("Age:", details.get("age", "Not available"))
        print("Phone:", details.get("phone", "Not available"))
        print("Email:", details.get("email", "Not available"))
        print("Department:", details.get("department", "Not available"))
        print("Position:", details.get("position", "Not available"))
        print("Basic Salary:", details.get("basic_salary", 0))
        print("House Allowance:", details.get("house_allowance", 0))
        print("Transport Allowance:", details.get("transport_allowance", 0))
        print("Other Allowance:", details.get("other_allowance", 0))

    print("\n==========================================")
    print("Total Employees:", len(employees))

# 6. Search employee function
def search_employee():
    while True:
        employee_id = input("Enter Employee ID: ").strip().upper()

        if employee_id == "":
            print("Employee ID cannot be empty. Please try again.")
        else:
            break

    employee = employees.get(employee_id)

    if employee:
        print("\n========== EMPLOYEE RECORD ==========")
        print("Employee ID:", employee_id)
        print("Full Name:", employee.get("full_name", "Not available"))
        print("Date of Birth:", employee.get("date_of_birth", "Not available"))
        print("Age:", employee.get("age", "Not available"))
        print("Phone:", employee.get("phone", "Not available"))
        print("Email:", employee.get("email", "Not available"))
        print("Department:", employee.get("department", "Not available"))
        print("Position:", employee.get("position", "Not available"))
        print("Basic Salary:", employee.get("basic_salary", 0))
        print("House Allowance:", employee.get("house_allowance", 0))
        print("Transport Allowance:", employee.get("transport_allowance", 0))
        print("Other Allowance:", employee.get("other_allowance", 0))
    else:
        print("\nEmployee not found.")

# 7. Update employee function
def update_employee():
    # Keep asking until an existing employee ID is entered
    while True:
        employee_id = input("Enter Employee ID to update: ").strip().upper()

        if employee_id == "":
            print("Employee ID cannot be empty. Please try again.")
            continue

        selected_employee = employees.get(employee_id)

        if selected_employee is None:
            print("Employee not found. Please enter a valid ID.")
            continue

        print("Employee found!")
        break

    print("\n--- Update Employee Information ---")
    print("Leave a field empty to keep the current value.")

    # Get the employee's current first and last names
    existing_names = selected_employee["full_name"].split()
    existing_first_name = existing_names[0]
    existing_last_name = existing_names[-1]

    # Ask for an updated first name and validate it
    while True:
        first_name = input(f"Enter First Name [{existing_first_name}]: ").strip()

        if first_name == "":
            new_first_name = existing_first_name
            break
        elif not first_name.isalpha():
            print("First name must contain letters only. Please try again.")
        else:
            new_first_name = first_name
            break

    # Ask for an updated last name and validate it
    while True:
        last_name = input(f"Enter Last Name [{existing_last_name}]: ").strip()

        if last_name == "":
            new_last_name = existing_last_name
            break
        elif not last_name.isalpha():
            print("Last name must contain letters only. Please try again.")
        else:
            new_last_name = last_name
            break

    # Update the full name
    selected_employee["full_name"] = new_first_name + " " + new_last_name

    # Get the employee's current date of birth
    existing_dob = selected_employee.get("date_of_birth", "")
    print("\nDate of birth must use YYYY-MM-DD format.")

    # Ask for an updated date of birth and validate it
    while True:
        dob = input(f"Enter Date of Birth [{existing_dob}]: ").strip()

        if dob == "":
            new_dob = existing_dob
            break

        try:
            new_birth_date = datetime.strptime(dob, "%Y-%m-%d").date()

            if new_birth_date >= date.today():
                print("Date of birth must be earlier than today. Please try again.")
                continue

            new_age = calculate_age(new_birth_date)

            if new_age < 18 or new_age > 100:
                print("Employee age must be between 18 and 100. Please try again.")
                continue

            new_dob = new_birth_date.isoformat()
            selected_employee["age"] = new_age
            break

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, for example 2002-05-15.")

    # Save the updated date of birth
    selected_employee["date_of_birth"] = new_dob

    # Ask for an updated phone number; empty input keeps the old number
    existing_phone = selected_employee.get("phone", "")
    while True:
        phone = input(f"Enter Phone Number [{existing_phone}]: ").strip()

        if phone == "":
            new_phone = existing_phone
            break

        phone = phone.replace(" ", "").replace("-", "")

        # Normalize Ethiopian phone number formats
        if phone.startswith("09") or phone.startswith("07"):
            phone = "+251" + phone[1:]
        elif phone.startswith("2519") or phone.startswith("2517"):
            phone = "+" + phone

        if len(phone) == 13 and phone.startswith(("+2519", "+2517")) and phone[1:].isdigit():
            new_phone = phone
            break
        else:
            print("Invalid phone number. Use 09XXXXXXXX, 07XXXXXXXX, or +2519XXXXXXXX / +2517XXXXXXXX.")

    selected_employee["phone"] = new_phone

    # Ask for an updated email address; empty input keeps the old email
    existing_email = selected_employee.get("email", "")
    email_pattern = r"[A-Za-z0-9][A-Za-z0-9._%+-]*@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"

    while True:
        email = input(f"Enter Email Address [{existing_email}]: ").strip()

        if email == "":
            new_email = existing_email
            break
        elif not re.fullmatch(email_pattern, email):
            print("Invalid email. Example: employee@gmail.com")
        else:
            new_email = email
            break

    selected_employee["email"] = new_email

    # Ask for an updated department; empty input keeps the old value
    existing_department = selected_employee.get("department", "")
    while True:
        department = input(f"Enter Department [{existing_department}]: ").strip()

        if department == "":
            new_department = existing_department
            break
        elif not re.fullmatch(r"[A-Za-z]+(?:[ '&-][A-Za-z]+)*", department):
            print("Department must contain words only. Numbers and invalid symbols are not allowed.")
        else:
            new_department = department
            break

    selected_employee["department"] = new_department

    # Ask for an updated position; empty input keeps the old value
    existing_position = selected_employee.get("position", "")
    while True:
        position = input(f"Enter Position [{existing_position}]: ").strip()

        if position == "":
            new_position = existing_position
            break
        elif not re.fullmatch(r"[A-Za-z]+(?:[ '&-][A-Za-z]+)*", position):
            print("Position must contain words only. Numbers and invalid symbols are not allowed.")
        else:
            new_position = position
            break

    selected_employee["position"] = new_position

    # Update basic salary and allowances
    salary_fields = [
        ("basic_salary", "Basic Salary"),
        ("house_allowance", "House Allowance"),
        ("transport_allowance", "Transport Allowance"),
        ("other_allowance", "Other Allowance")
    ]

    for field, label in salary_fields:
        existing_amount = selected_employee.get(field, 0)

        while True:
            value = input(f"Enter {label} [{existing_amount}]: ").strip()

            if value == "":
                new_amount = existing_amount
                break

            try:
                new_amount = float(value)

                if not math.isfinite(new_amount):
                    print("Please enter a valid finite number.")
                elif new_amount < 0:
                    print("Amount cannot be negative.")
                else:
                    break

            except ValueError:
                print("Invalid input. Please enter numbers only.")

        selected_employee[field] = new_amount

    print("Employee information updated successfully!")
    save_employees()  # Automatically save the updated employee record

# 8. Delete employee function
def delete_employee():
    if not employees:
        print("There are no employee records to delete.")
        return

    # Keep asking until an existing employee ID is entered
    while True:
        employee_id = input("Enter Employee ID to delete: ").strip().upper()

        if employee_id == "":
            print("Employee ID cannot be empty. Please try again.")
            continue

        selected_employee = employees.get(employee_id)

        if selected_employee is None:
            print("Employee not found. Please enter a valid employee ID.")
            continue

        break

    print("\n========== EMPLOYEE TO DELETE ==========")
    print("Employee ID:", employee_id)
    print("Full Name:", selected_employee.get("full_name", "Not available"))
    print("Department:", selected_employee.get("department", "Not available"))
    print("Position:", selected_employee.get("position", "Not available"))

    # Ask for confirmation before deleting the record
    while True:
        confirmation = input("Are you sure you want to delete this employee? (yes/no): ").strip().lower()

        if confirmation in ("yes", "y"):
            del employees[employee_id]
            save_employees()
            print("Employee record deleted successfully!")
            break
        elif confirmation in ("no", "n"):
            print("Deletion cancelled. Employee record was not changed.")
            break
        else:
            print("Please enter yes or no.")

# 9. Calculate gross salary function
def calculate_gross_salary():
    if not employees:
        print("There are no employee records available.")
        return

    # Ask until an existing employee ID is entered
    while True:
        employee_id = input("Enter Employee ID: ").strip().upper()

        if employee_id == "":
            print("Employee ID cannot be empty. Please try again.")
            continue

        selected_employee = employees.get(employee_id)

        if selected_employee is None:
            print("Employee not found. Please enter a valid employee ID.")
            continue

        break

    # Get the employee's salary components
    basic_salary = float(selected_employee.get("basic_salary", 0))
    house_allowance = float(selected_employee.get("house_allowance", 0))
    transport_allowance = float(selected_employee.get("transport_allowance", 0))
    other_allowance = float(selected_employee.get("other_allowance", 0))

    # Calculate gross salary
    gross_salary = (
        basic_salary
        + house_allowance
        + transport_allowance
        + other_allowance
    )

    print("\n========== GROSS SALARY DETAILS ==========")
    print("Employee ID:", employee_id)
    print("Full Name:", selected_employee.get("full_name", "Not available"))
    print("------------------------------------------")
    print(f"Basic Salary:       {basic_salary:,.2f}")
    print(f"House Allowance:    {house_allowance:,.2f}")
    print(f"Transport Allowance:{transport_allowance:,.2f}")
    print(f"Other Allowance:    {other_allowance:,.2f}")
    print("------------------------------------------")
    print(f"Gross Salary:       {gross_salary:,.2f}")
    print("==========================================")

# 10. Display payroll function
def display_payroll():
    if not employees:
        print("There are no employee records available.")
        return

    print("\n" + "=" * 125)
    print("ABC GOVERNMENT ORGANIZATION - EMPLOYEE PAYROLL")
    print("=" * 125)
    print(
        f"{'ID':<12} {'EMPLOYEE NAME':<22} {'BASIC':>12} "
        f"{'ALLOWANCES':>12} {'GROSS':>12} {'PENSION':>12} "
        f"{'TAX':>12} {'NET SALARY':>14}"
    )
    print("-" * 125)

    total_basic = 0
    total_allowances = 0
    total_gross = 0
    total_pension = 0
    total_tax = 0
    total_net = 0

    for employee_id, details in employees.items():
        basic_salary = float(details.get("basic_salary", 0))
        house_allowance = float(details.get("house_allowance", 0))
        transport_allowance = float(details.get("transport_allowance", 0))
        other_allowance = float(details.get("other_allowance", 0))

        allowances = house_allowance + transport_allowance + other_allowance
        gross_salary = basic_salary + allowances

        # Employee pension contribution is 7% of basic salary
        pension = basic_salary * 0.07

        # Calculate monthly income tax based on gross salary
        if gross_salary <= 2000:
            tax_rate = 0
            tax_deduction = 0
        elif gross_salary <= 4000:
            tax_rate = 0.15
            tax_deduction = 300
        elif gross_salary <= 7000:
            tax_rate = 0.20
            tax_deduction = 500
        elif gross_salary <= 10000:
            tax_rate = 0.25
            tax_deduction = 850
        elif gross_salary <= 14000:
            tax_rate = 0.30
            tax_deduction = 1350
        else:
            tax_rate = 0.35
            tax_deduction = 2050

        income_tax = (gross_salary * tax_rate) - tax_deduction
        net_salary = gross_salary - pension - income_tax

        print(
            f"{employee_id:<12} "
            f"{details.get('full_name', 'Not available')[:22]:<22} "
            f"{basic_salary:>12,.2f} {allowances:>12,.2f} "
            f"{gross_salary:>12,.2f} {pension:>12,.2f} "
            f"{income_tax:>12,.2f} {net_salary:>14,.2f}"
        )

        total_basic += basic_salary
        total_allowances += allowances
        total_gross += gross_salary
        total_pension += pension
        total_tax += income_tax
        total_net += net_salary

    print("-" * 125)
    print(
        f"{'TOTAL':<35} {total_basic:>12,.2f} {total_allowances:>12,.2f} "
        f"{total_gross:>12,.2f} {total_pension:>12,.2f} "
        f"{total_tax:>12,.2f} {total_net:>14,.2f}"
    )
    print("=" * 125)
    print("Total Employees:", len(employees))

# 12. Main application menu
def main():
    load_employees()

    while True:
        print("\n========================================")
        print("ABC GOVERNMENT ORGANIZATION")
        print("EMPLOYEE PAYROLL MANAGEMENT SYSTEM")
        print("========================================")
        print("1. Register New Employee")
        print("2. Save Employee Information")
        print("3. Display All Employees")
        print("4. Search Employee by ID")
        print("5. Update Employee Information")
        print("6. Delete Employee Record")
        print("7. Calculate Employee Gross Salary")
        print("8. Display All Employees' Payroll")
        print("9. Exit")
        print("========================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_employee()
        elif choice == "2":
            save_employees()
        elif choice == "3":
            display_employees()
        elif choice == "4":
            search_employee()
        elif choice == "5":
            update_employee()
        elif choice == "6":
            delete_employee()
        elif choice == "7":
            calculate_gross_salary()
        elif choice == "8":
            display_payroll()
        elif choice == "9":
            print("Thank you for using our system!")
            break
        else:
            print("Invalid choice. Please select 1 to 9.")

# 12. Start application
# ============================================================
# SECURITY LAYER: LOGIN, ROLES, AND TWO-WAY APPROVAL
# The original payroll functions above are preserved.
# ============================================================
import secrets
from auth import (
    initialize_accounts, create_employee_account, authenticate, read_password,
    change_password, set_account_active, get_account_permissions,
    update_account_permissions, AVAILABLE_PERMISSIONS
)
import request_manager as requests


def persist_employee_data():
    """Atomically save employee data; raise errors so approvals cannot be falsely completed."""
    temporary = "employees.tmp"
    with open(temporary, "w", encoding="utf-8") as file:
        json.dump(employees, file, indent=4)
    import os
    os.replace(temporary, "employees.txt")


original_register_employee = register_employee


def register_employee():
    """Keep the original registration flow, then create a temporary-password account."""
    before = set(employees)
    original_register_employee()
    added = set(employees) - before
    if not added:
        return
    employee_id = next(iter(added))
    try:
        temporary_password = create_employee_account(employee_id)
        persist_employee_data()
        print("\nEmployee account created.")
        print("Give this temporary password privately to the employee:")
        print(temporary_password)
        print("The employee must change it at first login.")
    except Exception as error:
        employees.pop(employee_id, None)
        print("Account creation failed. Registration was cancelled:", error)



def prompt_new_password(employee_id):
    while True:
        password = read_password("New password (at least 8 characters, uppercase, lowercase, and number): ")
        confirmation = read_password("Confirm new password: ")
        if password != confirmation:
            print("Passwords do not match.")
            continue
        try:
            change_password(employee_id, password)
            print("Password changed successfully.")
            return True
        except ValueError as error:
            print(error)


def login():
    print("\n========== SECURE LOGIN ==========")
    employee_id = input("Employee ID: ").strip().upper()
    password = read_password("Password: ")
    session = authenticate(employee_id, password)
    if session is None:
        print("Invalid employee ID/password, or the account is inactive.")
        return None

    if session["must_change_password"]:
        print("\nYou must change your temporary password before continuing.")
        if not prompt_new_password(employee_id):
            return None
    return session


def show_personal_profile(employee_id):
    details = employees.get(employee_id)
    if not details:
        print("Your employee record could not be found. Contact the administrator.")
        return
    print("\n========== MY PROFILE ==========")
    print("Employee ID:", employee_id)
    for label, field in [
        ("Full Name", "full_name"), ("Date of Birth", "date_of_birth"),
        ("Age", "age"), ("Phone", "phone"), ("Email", "email"),
        ("Department", "department"), ("Position", "position"),
        ("Account Status", "account_status")
    ]:
        print(f"{label}: {details.get(field, 'ACTIVE' if field == 'account_status' else 'Not available')}")


def show_personal_payroll(employee_id):
    details = employees.get(employee_id)
    if not details:
        print("Your employee record could not be found.")
        return
    basic = float(details.get("basic_salary", 0))
    allowances = sum(float(details.get(field, 0)) for field in
                     ("house_allowance", "transport_allowance", "other_allowance"))
    gross = basic + allowances
    pension = basic * 0.07
    if gross <= 2000:
        rate, deduction = 0, 0
    elif gross <= 4000:
        rate, deduction = 0.15, 300
    elif gross <= 7000:
        rate, deduction = 0.20, 500
    elif gross <= 10000:
        rate, deduction = 0.25, 850
    elif gross <= 14000:
        rate, deduction = 0.30, 1350
    else:
        rate, deduction = 0.35, 2050
    tax = gross * rate - deduction
    net = gross - pension - tax
    print("\n========== MY PAYROLL ==========")
    print("Employee:", details.get("full_name", "Not available"))
    print(f"Basic salary:       {basic:,.2f}")
    print(f"Allowances:         {allowances:,.2f}")
    print(f"Gross salary:       {gross:,.2f}")
    print(f"Pension (7%):       {pension:,.2f}")
    print(f"Income tax:         {tax:,.2f}")
    print(f"Net salary:         {net:,.2f}")


def request_field_change(employee_id, requester_id, requester_role):
    allowed = sorted(requests.EDITABLE_FIELDS)
    print("\nInformation fields that can be changed:")
    for index, field in enumerate(allowed, 1):
        print(f"{index}. {field}")
    while True:
        choice = input("Choose field number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(allowed):
            field = allowed[int(choice) - 1]
            break
        print("Choose a valid field number.")

    new_value = input(f"Enter proposed new value for {field}: ").strip()
    if not new_value:
        print("The proposed value cannot be empty.")
        return
    if field in {"basic_salary", "house_allowance", "transport_allowance", "other_allowance"}:
        try:
            new_value = float(new_value)
            if not math.isfinite(new_value) or new_value < 0:
                raise ValueError
        except ValueError:
            print("Salary and allowance values must be valid non-negative numbers.")
            return
    elif field == "date_of_birth":
        try:
            parsed = datetime.strptime(new_value, "%Y-%m-%d").date()
            age = calculate_age(parsed)
            if parsed >= date.today() or not 18 <= age <= 100:
                raise ValueError
            new_value = parsed.isoformat()
        except ValueError:
            print("Enter a valid date (YYYY-MM-DD) for an employee aged 18–100.")
            return
    elif field == "full_name":
        if not re.fullmatch(r"[A-Za-z]+(?: [A-Za-z]+)+", new_value):
            print("Enter a valid full name using letters and spaces.")
            return
    elif field in {"department", "position"}:
        if not re.fullmatch(r"[A-Za-z]+(?:[ '&-][A-Za-z]+)*", new_value):
            print("Enter valid text without numbers.")
            return
    elif field == "email":
        pattern = r"[A-Za-z0-9][A-Za-z0-9._%+-]*@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"
        if not re.fullmatch(pattern, new_value):
            print("Enter a valid email address.")
            return
    elif field == "phone":
        normalized = new_value.replace(" ", "").replace("-", "")
        if normalized.startswith(("09", "07")):
            normalized = "+251" + normalized[1:]
        elif normalized.startswith(("2519", "2517")):
            normalized = "+" + normalized
        if not (len(normalized) == 13 and normalized.startswith(("+2519", "+2517")) and normalized[1:].isdigit()):
            print("Enter a valid Ethiopian mobile number.")
            return
        new_value = normalized

    reason = input("Reason for this change request: ").strip()
    try:
        item = requests.submit_change(
            employee_id, requester_id, requester_role, field, new_value, reason, employees
        )
        print(f"Request {item['request_id']} submitted. It is pending approval.")
    except (ValueError, RuntimeError) as error:
        print("Could not submit request:", error)


def request_deactivation(employee_id, requester_id, requester_role):
    reason = input("Reason for deactivation request: ").strip()
    try:
        item = requests.submit_deactivation(
            employee_id, requester_id, requester_role, reason, employees
        )
        print(f"Deactivation request {item['request_id']} submitted for approval.")
    except (ValueError, RuntimeError) as error:
        print("Could not submit request:", error)


def show_requests_for_employee(employee_id):
    try:
        items = [item for item in requests.load_requests() if item["employee_id"] == employee_id]
    except RuntimeError as error:
        print(error)
        return
    if not items:
        print("No requests found for your employee record.")
        return
    print("\n========== MY REQUEST HISTORY ==========")
    for item in items:
        print(f"\n{item['request_id']} | {item['request_type']} | {item['status']}")
        print("Requested by:", item["requested_by"])
        print("Reason:", item["reason"])
        if item["request_type"] == "UPDATE":
            print(f"Change: {item['field_name']} | {item['old_value']} -> {item['new_value']}")
        print("Created:", item["created_at"])
        if item["decided_at"]:
            print("Decision by:", item["approved_by"], "|", item["decided_at"])


def pending_requests_for_approver(session):
    try:
        items = requests.load_requests()
    except RuntimeError as error:
        print(error)
        return
    pending = []
    for item in items:
        if item["status"] != "PENDING":
            continue
        if session["role"] == "ADMIN" and item["requester_role"] == "USER":
            pending.append(item)
        elif session["role"] == "USER" and item["requester_role"] == "ADMIN" and item["employee_id"] == session["employee_id"]:
            pending.append(item)

    if not pending:
        print("No pending requests require your approval.")
        return
    print("\n========== REQUESTS AWAITING YOUR APPROVAL ==========")
    for item in pending:
        print(f"\n{item['request_id']} | {item['request_type']} | Employee: {item['employee_id']}")
        print("Requested by:", item["requested_by"])
        print("Reason:", item["reason"])
        if item["request_type"] == "UPDATE":
            print(f"Proposed: {item['field_name']} = {item['new_value']}")
    request_id = input("\nEnter request ID to review (or press Enter to return): ").strip().upper()
    if not request_id:
        return
    if not any(item["request_id"] == request_id for item in pending):
        print("That request is not assigned to your approval.")
        return
    decision = input("Approve or reject? (A/R): ").strip().upper()
    if decision not in ("A", "R"):
        print("Invalid decision. No changes made.")
        return
    try:
        decided = requests.decide_request(
            request_id, session["employee_id"], session["role"],
            "APPROVED" if decision == "A" else "REJECTED",
            employees, persist_employee_data, set_account_active
        )
        print(f"{decided['request_id']} was {decided['status'].lower()}.")
    except (ValueError, PermissionError, RuntimeError, OSError) as error:
        print("Could not decide request:", error)


def change_own_password(session):
    print("\n--- Change Password ---")
    current = read_password("Current password: ")
    verified = authenticate(session["employee_id"], current)
    if not verified:
        print("Current password is incorrect.")
        return
    prompt_new_password(session["employee_id"])


def manage_special_permissions(session):
    print("\n========== GRANT / REVOKE SPECIAL PERMISSIONS ==========")
    target = input("Enter employee ID: ").strip().upper()
    if target not in employees:
        print("Employee not found.")
        return
    if target == "TTBR/0030/18":
        print("The first administrator's full access is managed through the administrator role.")
        return

    current = get_account_permissions(target)
    print("\nCurrent special permissions:")
    if current:
        for permission in current:
            print("-", AVAILABLE_PERMISSIONS[permission])
    else:
        print("None")

    permission_keys = list(AVAILABLE_PERMISSIONS)
    print("\nAvailable permissions:")
    for index, key in enumerate(permission_keys, 1):
        print(f"{index}. {AVAILABLE_PERMISSIONS[key]} ({key})")
    choice = input("Choose permission number: ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(permission_keys):
        print("Invalid permission choice.")
        return
    permission = permission_keys[int(choice) - 1]
    action = input("Grant or revoke? (G/R): ").strip().upper()
    if action not in ("G", "R"):
        print("Invalid action.")
        return
    try:
        updated = update_account_permissions(session["employee_id"], target, permission, action == "G")
        print("Permission list updated.")
        print("Current permissions:", ", ".join(updated) if updated else "None")
    except (ValueError, PermissionError) as error:
        print("Could not update permissions:", error)


def employee_special_access(session):
    permissions = get_account_permissions(session["employee_id"])
    actions = {
        "VIEW_ALL_EMPLOYEES": ("View all employee records", display_employees),
        "SEARCH_EMPLOYEES": ("Search employee records", search_employee),
        "VIEW_ALL_PAYROLL": ("View organization-wide payroll", display_payroll),
        "CALCULATE_GROSS_SALARY": ("Calculate gross salary for an employee", calculate_gross_salary),
        "REGISTER_EMPLOYEE": ("Register a new employee", register_employee),
    }
    available = [(key, actions[key]) for key in permissions if key in actions]
    if not available:
        print("No special permissions have been granted to your account.")
        return
    print("\n========== YOUR SPECIAL ACCESS ==========")
    for index, (key, (label, _)) in enumerate(available, 1):
        print(f"{index}. {label}")
    choice = input("Choose an authorized action (or Enter to return): ").strip()
    if not choice:
        return
    if not choice.isdigit() or not 1 <= int(choice) <= len(available):
        print("Invalid choice.")
        return
    available[int(choice) - 1][1][1]()


def admin_menu(session):
    while True:
        print("\n========== ADMINISTRATOR MENU ==========")
        print("1. Register New Employee")
        print("2. Save Employee Information")
        print("3. Display All Employees")
        print("4. Search Employee by ID")
        print("5. Submit Employee Information Change Request")
        print("6. Submit Employee Deactivation Request")
        print("7. Review Employee Requests")
        print("8. Calculate Employee Gross Salary")
        print("9. Display All Employees' Payroll")
        print("10. View All Request History")
        print("11. Change My Password")
        print("12. Grant / Revoke Special Permissions")
        print("13. Logout")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            register_employee()
        elif choice == "2":
            try:
                persist_employee_data()
                print("Employee information saved.")
            except OSError as error:
                print("Could not save:", error)
        elif choice == "3":
            display_employees()
        elif choice == "4":
            search_employee()
        elif choice == "5":
            target = input("Enter the specific employee ID: ").strip().upper()
            if target == session["employee_id"]:
                print("You cannot approve your own change. A second administrator is required.")
            elif target not in employees:
                print("Employee not found.")
            else:
                request_field_change(target, session["employee_id"], "ADMIN")
        elif choice == "6":
            target = input("Enter employee ID to request deactivation: ").strip().upper()
            if target == session["employee_id"]:
                print("A second administrator is required to request changes to your own account.")
            elif target not in employees:
                print("Employee not found.")
            else:
                request_deactivation(target, session["employee_id"], "ADMIN")
        elif choice == "7":
            pending_requests_for_approver(session)
        elif choice == "8":
            calculate_gross_salary()
        elif choice == "9":
            display_payroll()
        elif choice == "10":
            try:
                for item in requests.load_requests():
                    print(f"{item['request_id']} | {item['employee_id']} | {item['request_type']} | {item['status']}")
            except RuntimeError as error:
                print(error)
        elif choice == "11":
            change_own_password(session)
        elif choice == "12":
            manage_special_permissions(session)
        elif choice == "13":
            print("Logged out.")
            return
        else:
            print("Choose a number from 1 to 13.")


def employee_menu(session):
    employee_id = session["employee_id"]
    while True:
        print("\n========== EMPLOYEE MENU ==========")
        print("1. View My Profile")
        print("2. View My Payroll")
        print("3. Submit My Information Change Request")
        print("4. Submit My Account Deactivation Request")
        print("5. View My Request History")
        print("6. Review Administrator Requests About Me")
        print("7. Change My Password")
        print("8. Special Permission Access")
        print("9. Logout")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            show_personal_profile(employee_id)
        elif choice == "2":
            show_personal_payroll(employee_id)
        elif choice == "3":
            request_field_change(employee_id, employee_id, "USER")
        elif choice == "4":
            request_deactivation(employee_id, employee_id, "USER")
        elif choice == "5":
            show_requests_for_employee(employee_id)
        elif choice == "6":
            pending_requests_for_approver(session)
        elif choice == "7":
            change_own_password(session)
        elif choice == "8":
            employee_special_access(session)
        elif choice == "9":
            print("Logged out.")
            return
        else:
            print("Choose a number from 1 to 9.")


def main():
    load_employees()
    if not employees:
        print("No employee records exist. Ask an administrator to restore or register employee data.")
        return
    try:
        initialize_accounts(list(employees.keys()))
    except (RuntimeError, OSError) as error:
        print("Security setup could not continue:", error)
        return

    while True:
        session = login()
        if session is None:
            retry = input("Try logging in again? (y/n): ").strip().lower()
            if retry not in ("y", "yes"):
                print("Goodbye.")
                return
            continue

        employee = employees.get(session["employee_id"])
        if employee is None or employee.get("account_status", "ACTIVE") != "ACTIVE":
            print("Your employee record is inactive or missing. Contact the administrator.")
            set_account_active(session["employee_id"], False)
            continue

        if session["role"] == "ADMIN":
            admin_menu(session)
        else:
            employee_menu(session)


if __name__ == "__main__":
    main()
