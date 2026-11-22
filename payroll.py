"""Payroll calculations for the assignment."""


def calculate_payroll(employee):
    basic = float(employee.get("basic_salary", 0))
    allowances = (
        float(employee.get("house_allowance", 0))
        + float(employee.get("transport_allowance", 0))
        + float(employee.get("other_allowance", 0))
    )
    gross = basic + allowances
    pension = basic * 0.07

    if gross <= 2000:
        rate, deduction = 0.00, 0
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

    income_tax = max(0, gross * rate - deduction)
    net = gross - pension - income_tax

    return {
        "basic": basic,
        "allowances": allowances,
        "gross": gross,
        "pension": pension,
        "income_tax": income_tax,
        "net": net,
    }


def display_employee_payroll(employee_id, employee):
    result = calculate_payroll(employee)
    print("\n========== PAYROLL SLIP ==========")
    print(f"Employee ID:       {employee_id}")
    print(f"Employee Name:     {employee.get('full_name', '')}")
    print("----------------------------------")
    print(f"Basic Salary:      {result['basic']:,.2f}")
    print(f"Allowances:        {result['allowances']:,.2f}")
    print(f"Gross Salary:      {result['gross']:,.2f}")
    print(f"Pension (7%):      {result['pension']:,.2f}")
    print(f"Income Tax:        {result['income_tax']:,.2f}")
    print("----------------------------------")
    print(f"NET SALARY:        {result['net']:,.2f}")
    print("==================================")


def display_all_payroll(employees):
    if not employees:
        print("No employee records available.")
        return

    print("\n" + "=" * 100)
    print("ABC GOVERNMENT ORGANIZATION - PAYROLL REPORT")
    print("=" * 100)
    print(f"{'ID':<14}{'EMPLOYEE':<24}{'GROSS':>14}{'PENSION':>14}{'TAX':>14}{'NET':>14}")
    print("-" * 100)

    totals = {"gross": 0, "pension": 0, "income_tax": 0, "net": 0}
    for employee_id, employee in employees.items():
        result = calculate_payroll(employee)
        print(
            f"{employee_id:<14}"
            f"{employee.get('full_name', '')[:22]:<24}"
            f"{result['gross']:>14,.2f}"
            f"{result['pension']:>14,.2f}"
            f"{result['income_tax']:>14,.2f}"
            f"{result['net']:>14,.2f}"
        )
        for key in totals:
            totals[key] += result[key]

    print("-" * 100)
    print(
        f"{'TOTAL':<38}{totals['gross']:>14,.2f}"
        f"{totals['pension']:>14,.2f}"
        f"{totals['income_tax']:>14,.2f}"
        f"{totals['net']:>14,.2f}"
    )
    print("=" * 100)
    print(f"Number of employees: {len(employees)}")
