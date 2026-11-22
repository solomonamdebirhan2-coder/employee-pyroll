"""Two-way employee change/deactivation request workflow."""
import json
from pathlib import Path
from datetime import datetime, timezone

REQUEST_FILE = Path("requests.txt")
EDITABLE_FIELDS = {
    "full_name", "date_of_birth", "phone", "email",
    "department", "position", "basic_salary", "house_allowance",
    "transport_allowance", "other_allowance",
}


def load_requests():
    if not REQUEST_FILE.exists():
        return []
    try:
        data = json.loads(REQUEST_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("Request file must contain a JSON list.")
        return data
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Cannot safely read requests.txt: {error}") from error


def save_requests(requests):
    temporary = REQUEST_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(requests, indent=4), encoding="utf-8")
    temporary.replace(REQUEST_FILE)


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def submit_change(employee_id, requester_id, requester_role, field_name, new_value, reason, employees):
    if employee_id not in employees:
        raise ValueError("Employee not found.")
    if field_name not in EDITABLE_FIELDS:
        raise ValueError("This field cannot be changed through a request.")
    if not str(reason).strip():
        raise ValueError("A reason is required.")
    old_value = employees[employee_id].get(field_name)
    if str(old_value) == str(new_value):
        raise ValueError("The new value is the same as the current value.")
    requests = load_requests()
    if any(item["status"] == "PENDING" and item["employee_id"] == employee_id
           and item["request_type"] == "UPDATE" and item["field_name"] == field_name
           for item in requests):
        raise ValueError("A pending request already exists for this employee and field.")
    number = max((int(item["request_id"].split("-")[-1]) for item in requests), default=0) + 1
    item = {
        "request_id": f"REQ-{number:05d}",
        "employee_id": employee_id,
        "request_type": "UPDATE",
        "requested_by": requester_id,
        "requester_role": requester_role,
        "field_name": field_name,
        "old_value": old_value,
        "new_value": new_value,
        "reason": str(reason).strip(),
        "status": "PENDING",
        "created_at": _now(),
        "approved_by": None,
        "decided_at": None,
    }
    requests.append(item)
    save_requests(requests)
    return item


def submit_deactivation(employee_id, requester_id, requester_role, reason, employees):
    if employee_id not in employees:
        raise ValueError("Employee not found.")
    if not str(reason).strip():
        raise ValueError("A reason is required.")
    requests = load_requests()
    if any(item["status"] == "PENDING" and item["employee_id"] == employee_id
           and item["request_type"] == "DEACTIVATE" for item in requests):
        raise ValueError("A pending deactivation request already exists for this employee.")
    number = max((int(item["request_id"].split("-")[-1]) for item in requests), default=0) + 1
    item = {
        "request_id": f"REQ-{number:05d}",
        "employee_id": employee_id,
        "request_type": "DEACTIVATE",
        "requested_by": requester_id,
        "requester_role": requester_role,
        "field_name": "account_status",
        "old_value": employees[employee_id].get("account_status", "ACTIVE"),
        "new_value": "INACTIVE",
        "reason": str(reason).strip(),
        "status": "PENDING",
        "created_at": _now(),
        "approved_by": None,
        "decided_at": None,
    }
    requests.append(item)
    save_requests(requests)
    return item


def expected_approver_role(request):
    return "USER" if request["requester_role"] == "ADMIN" else "ADMIN"


def decide_request(request_id, approver_id, approver_role, decision, employees, save_employees_callback, set_account_active_callback):
    requests = load_requests()
    request = next((item for item in requests if item["request_id"] == request_id), None)
    if request is None:
        raise ValueError("Request not found.")
    if request["status"] != "PENDING":
        raise ValueError("This request has already been decided.")
    if approver_id == request["requested_by"]:
        raise PermissionError("The requester cannot approve their own request.")
    if approver_role != expected_approver_role(request):
        raise PermissionError("This request must be decided by the required approver.")
    if request["employee_id"] != approver_id and approver_role == "USER":
        raise PermissionError("Only the specific employee can approve this request.")
    if decision not in ("APPROVED", "REJECTED"):
        raise ValueError("Decision must be APPROVED or REJECTED.")

    if decision == "APPROVED":
        employee = employees.get(request["employee_id"])
        if employee is None:
            raise ValueError("The affected employee record no longer exists.")
        if request["request_type"] == "UPDATE":
            current_value = employee.get(request["field_name"])
            if str(current_value) != str(request["old_value"]):
                raise ValueError("The employee field changed after this request was submitted. Submit a new request.")
            employee[request["field_name"]] = request["new_value"]
            if request["field_name"] == "date_of_birth":
                from datetime import date
                dob = date.fromisoformat(str(request["new_value"]))
                today = date.today()
                employee["age"] = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        elif request["request_type"] == "DEACTIVATE":
            employee["account_status"] = "INACTIVE"
        save_employees_callback()
        if request["request_type"] == "DEACTIVATE":
            set_account_active_callback(request["employee_id"], False)

    request["status"] = decision
    request["approved_by"] = approver_id
    request["decided_at"] = _now()
    save_requests(requests)
    return request
