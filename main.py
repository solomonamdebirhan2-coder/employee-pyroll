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
if __name__ == "__main__":
    main()
