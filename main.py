"""Menu-driven Employee Payroll Management System for ABC Government Organization."""

from employee_manager import (
    load_employees,
    add_employee,
    display_employees,
    search_employee,
    update_employee,
    delete_employee,
    save_employees,
)
from payroll import display_employee_payroll, display_all_payroll


def main():
    # Load saved employee records when the program starts.
    employees = load_employees()
    print(f"Loaded {len(employees)} employee record(s).")

    # Display the menu once at the beginning.
    print("\n==============================================")
    print("       ABC GOVERNMENT ORGANIZATION")
    print("       EMPLOYEE PAYROLL MANAGEMENT SYSTEM")
    print("==============================================")
    print("1. Register New Employee")
    print("2. Save Employee Information")
    print("3. Display All Employees")
    print("4. Search Employee by ID")
    print("5. Update Employee Information")
    print("6. Delete Employee Record")
    print("7. Calculate Employee Gross Salary")
    print("8. Display All Employees' Payroll")
    print("9. Exit")
    print("----------------------------------------------")

    invalid_attempts = 0
    max_invalid_attempts = 4

    while True:
        choice = input("Enter your choice (1-9): ").strip()

        if choice not in {"1", "2", "3", "4", "5", "6", "7", "8", "9"}:
            invalid_attempts += 1
            remaining = max_invalid_attempts - invalid_attempts

            if invalid_attempts >= max_invalid_attempts:
                print("Too many invalid attempts. Goodbye!")
                break

            print(
                f"Invalid choice. Please enter a number from 1 to 9. "
                f"Attempts remaining: {remaining}."
            )
            continue

        # A valid choice resets the consecutive invalid-attempt counter.
        invalid_attempts = 0

        if choice == "1":
            add_employee(employees)
        elif choice == "2":
            save_employees(employees)
        elif choice == "3":
            display_employees(employees)
        elif choice == "4":
            search_employee(employees)
        elif choice == "5":
            update_employee(employees)
        elif choice == "6":
            delete_employee(employees)
        elif choice == "7":
            employee_id = input("Enter employee ID: ").strip().upper()
            employee = employees.get(employee_id)
            if employee is None:
                print("Employee not found.")
            else:
                # The payroll slip includes gross salary and deductions.
                display_employee_payroll(employee_id, employee)
        elif choice == "8":
            display_all_payroll(employees)
        elif choice == "9":
            save_employees(employees)
            print("Thank you for using the Employee Payroll Management System.")
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
