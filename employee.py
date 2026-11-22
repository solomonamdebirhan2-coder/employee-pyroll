"""Employee model for the payroll assignment."""


class Employee:
    """Store the required information for one employee."""

    def __init__(
        self, employee_id, full_name, department, position,
        basic_salary, house_allowance=0, transport_allowance=0,
        other_allowance=0, date_of_birth="", age=0, phone="", email=""
    ):
        self.employee_id = employee_id.strip().upper()
        self.full_name = full_name.strip()
        self.department = department.strip()
        self.position = position.strip()
        self.basic_salary = float(basic_salary)
        self.house_allowance = float(house_allowance)
        self.transport_allowance = float(transport_allowance)
        self.other_allowance = float(other_allowance)
        self.date_of_birth = date_of_birth
        self.age = age
        self.phone = phone
        self.email = email

    def to_dict(self):
        """Return employee information as a dictionary for JSON storage."""
        return {
            "employee_id": self.employee_id,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth,
            "age": self.age,
            "phone": self.phone,
            "email": self.email,
            "department": self.department,
            "position": self.position,
            "basic_salary": self.basic_salary,
            "house_allowance": self.house_allowance,
            "transport_allowance": self.transport_allowance,
            "other_allowance": self.other_allowance,
        }
