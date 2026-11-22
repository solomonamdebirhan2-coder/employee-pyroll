"""Web routes for employee management, approval workflows, and permissions."""
import re
from datetime import date, datetime
from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, session, url_for

import request_manager as requests
from auth import (AVAILABLE_PERMISSIONS, account_exists, create_employee_account,
                  get_account_permissions, set_account_active,
                  update_account_permissions)

web = Blueprint("web", __name__)

def setup_web_routes(app, login_required, load_employees, payroll):
    def save_employees(data):
        from storage import postgres_enabled, save_collection
        if postgres_enabled():
            save_collection("employees", data)
            return
        import json
        from pathlib import Path
        target = Path(__file__).resolve().parent / "employees.txt"
        temp = target.with_suffix(".tmp")
        temp.write_text(json.dumps(data, indent=4), encoding="utf-8")
        temp.replace(target)

    from audit_log import record_event

    def can(permission):
        if session.get("role") == "ADMIN":
            return True
        return permission in get_account_permissions(session["employee_id"])

    def require(permission):
        if not can(permission):
            abort(403, "You do not have permission to perform this action.")

    def validate_requested_value(field, value):
        if field in {"basic_salary", "house_allowance", "transport_allowance", "other_allowance"}:
            number = float(value)
            if number < 0 or number != number or number == float("inf"):
                raise ValueError("Salary values must be valid non-negative numbers.")
            return number
        if field == "date_of_birth":
            dob = date.fromisoformat(value)
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if dob >= today or not 18 <= age <= 100:
                raise ValueError("Date of birth must give an employee age between 18 and 100.")
            return dob.isoformat()
        if field == "email":
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._%+-]*@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}", value):
                raise ValueError("Enter a valid email address.")
            return value
        if field == "phone":
            phone = value.replace(" ", "").replace("-", "")
            if phone.startswith(("09", "07")):
                phone = "+251" + phone[1:]
            elif phone.startswith(("2519", "2517")):
                phone = "+" + phone
            if not (len(phone) == 13 and phone.startswith(("+2519", "+2517")) and phone[1:].isdigit()):
                raise ValueError("Enter a valid Ethiopian mobile number.")
            return phone
        if field in {"full_name", "department", "position"}:
            if not re.fullmatch(r"[A-Za-z]+(?:[ '&-][A-Za-z]+)*", value) or len(value) > 100:
                raise ValueError("Enter valid text for this field.")
            return value
        raise ValueError("This field cannot be changed.")

    @web.get("/employees")
    @login_required
    def employees():
        if session.get("role") != "ADMIN" and not (
            can("VIEW_ALL_EMPLOYEES") or can("SEARCH_EMPLOYEES")
        ):
            abort(403, "You do not have permission to view or search employee records.")
        data = load_employees()
        query = request.args.get("q", "").strip().casefold()
        rows = []
        can_view_all = session.get("role") == "ADMIN" or can("VIEW_ALL_EMPLOYEES")
        can_view_payroll = session.get("role") == "ADMIN" or can("VIEW_ALL_PAYROLL")
        for emp_id, record in data.items():
            text = " ".join([emp_id, str(record.get("full_name", "")),
                             str(record.get("department", "")), str(record.get("position", ""))]).casefold()
            if not query or query in text:
                rows.append({"id": emp_id, "record": record if can_view_all else {
                    "full_name": record.get("full_name", ""),
                    "department": record.get("department", ""),
                    "position": record.get("position", ""),
                    "account_status": record.get("account_status", "ACTIVE")
                }, "pay": payroll(record) if can_view_payroll else None})
        return render_template("employees.html", rows=rows, query=query,
                               can_view_all=can_view_all, can_view_payroll=can_view_payroll,
                               permissions=get_account_permissions(session["employee_id"]))

    @web.get("/employees/<path:employee_id>")
    @login_required
    def employee_detail(employee_id):
        if session.get("role") != "ADMIN" and not can("VIEW_ALL_EMPLOYEES"):
            abort(403, "You do not have permission to view full employee records.")
        record = load_employees().get(employee_id)
        if record is None:
            abort(404)
        return render_template("employee_detail.html", employee=record, employee_id=employee_id)

    @web.route("/employees/register", methods=["GET", "POST"])
    @login_required
    def register_employee():
        require("REGISTER_EMPLOYEE")
        if request.method == "POST":
            data = load_employees()
            emp_id = request.form.get("employee_id", "").strip().upper()
            name = request.form.get("full_name", "").strip()
            dob_text = request.form.get("date_of_birth", "").strip()
            department = request.form.get("department", "").strip()
            position = request.form.get("position", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()
            if not re.fullmatch(r"[A-Z0-9/\-]{4,30}", emp_id) or emp_id in data or account_exists(emp_id):
                flash("Enter a valid, unused employee ID.", "error")
            elif not re.fullmatch(r"[A-Za-z]+(?:[ '&-][A-Za-z]+)+", name):
                flash("Enter a valid full name.", "error")
            elif not re.fullmatch(r"[A-Za-z]+(?:[ '&-][A-Za-z]+)*", department) or not re.fullmatch(r"[A-Za-z]+(?:[ '&-][A-Za-z]+)*", position):
                flash("Department and position must contain valid text.", "error")
            elif not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._%+-]*@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}", email):
                flash("Enter a valid email address.", "error")
            else:
                try:
                    dob = datetime.strptime(dob_text, "%Y-%m-%d").date()
                    age = date.today().year - dob.year - ((date.today().month, date.today().day) < (dob.month, dob.day))
                    if dob >= date.today() or not 18 <= age <= 100:
                        raise ValueError
                    normalized_phone = phone.replace(" ", "").replace("-", "")
                    if normalized_phone.startswith(("09", "07")):
                        normalized_phone = "+251" + normalized_phone[1:]
                    elif normalized_phone.startswith(("2519", "2517")):
                        normalized_phone = "+" + normalized_phone
                    if not (len(normalized_phone) == 13 and normalized_phone.startswith(("+2519", "+2517")) and normalized_phone[1:].isdigit()):
                        raise ValueError
                    amounts = {}
                    for field in ("basic_salary", "house_allowance", "transport_allowance", "other_allowance"):
                        value = float(request.form.get(field, ""))
                        if value < 0 or value != value or value == float("inf"):
                            raise ValueError
                        amounts[field] = value
                    record = {"full_name": name, "date_of_birth": dob.isoformat(), "age": age,
                              "phone": normalized_phone, "email": email, "department": department,
                              "position": position, **amounts, "account_status": "ACTIVE"}
                    data[emp_id] = record
                    save_employees(data)
                    temporary = create_employee_account(emp_id)
                    record_event(session["employee_id"], "EMPLOYEE_REGISTERED", emp_id,
                                 {"department": department, "position": position})
                    flash("Employee registered. Give this temporary password privately: " + temporary, "success")
                    return redirect(url_for("web.employees"))
                except (ValueError, OverflowError):
                    flash("Check the date, Ethiopian mobile number, and non-negative salary values.", "error")
        return render_template("employee_form.html")

    @web.route("/requests", methods=["GET", "POST"])
    @login_required
    def request_center():
        data = load_employees()
        own_id = session["employee_id"]
        if request.method == "POST":
            target = request.form.get("employee_id", own_id).strip().upper()
            role = session["role"]
            if role != "ADMIN":
                target = own_id
            elif target == own_id:
                flash("You cannot submit a request about your own record as administrator.", "error")
                return redirect(url_for("web.request_center"))
            if target not in data:
                abort(404)
            if data[target].get("account_status", "ACTIVE") != "ACTIVE":
                flash("An inactive employee account cannot receive new requests.", "error")
                return redirect(url_for("web.request_center"))
            kind = request.form.get("kind")
            reason = request.form.get("reason", "").strip()
            try:
                if kind == "DEACTIVATE":
                    item = requests.submit_deactivation(target, own_id, role, reason, data)
                else:
                    field = request.form.get("field_name", "")
                    value = request.form.get("new_value", "").strip()
                    if field not in requests.EDITABLE_FIELDS or not value:
                        raise ValueError("Choose an editable field and provide a new value.")
                    value = validate_requested_value(field, value)
                    item = requests.submit_change(target, own_id, role, field, value, reason, data)
                record_event(own_id, "REQUEST_SUBMITTED", target,
                             {"request_id": item["request_id"], "request_type": item["request_type"]})
                flash("Request " + item["request_id"] + " submitted for approval.", "success")
            except (ValueError, RuntimeError) as exc:
                flash(str(exc), "error")
            return redirect(url_for("web.request_center"))
        all_items = requests.load_requests()
        if session["role"] == "ADMIN":
            visible = all_items
        else:
            visible = [item for item in all_items if item["employee_id"] == own_id]
        return render_template("requests.html", items=visible, employees=data,
                               editable_fields=sorted(requests.EDITABLE_FIELDS),
                               is_admin=session["role"] == "ADMIN")

    @web.post("/requests/<request_id>/decision")
    @login_required
    def decide(request_id):
        data = load_employees()
        decision = request.form.get("decision", "")
        try:
            item = requests.decide_request(
                request_id, session["employee_id"], session["role"], decision,
                data, lambda: save_employees(data), set_account_active
            )
            record_event(session["employee_id"], "REQUEST_" + item["status"], item["employee_id"],
                         {"request_id": item["request_id"], "request_type": item["request_type"]})
            flash(item["request_id"] + " " + item["status"].lower() + ".", "success")
        except (ValueError, PermissionError, RuntimeError, OSError) as exc:
            flash(str(exc), "error")
        return redirect(url_for("web.request_center"))

    @web.route("/permissions", methods=["GET", "POST"])
    @login_required
    def permissions():
        if session["role"] != "ADMIN":
            abort(403)
        data = load_employees()
        if request.method == "POST":
            target = request.form.get("employee_id", "").strip().upper()
            permission = request.form.get("permission", "")
            action = request.form.get("action", "")
            try:
                if target not in data:
                    raise ValueError("Employee not found.")
                if action not in {"GRANT", "REVOKE"}:
                    raise ValueError("Choose grant or revoke.")
                updated = update_account_permissions(session["employee_id"], target, permission, action == "GRANT")
                record_event(session["employee_id"], "PERMISSION_" + action, target,
                             {"permission": permission})
                flash("Permissions updated: " + (", ".join(updated) if updated else "none"), "success")
            except (ValueError, PermissionError) as exc:
                flash(str(exc), "error")
            return redirect(url_for("web.permissions"))
        users = []
        for emp_id, record in data.items():
            if emp_id == session["employee_id"]:
                continue
            users.append({"id": emp_id, "name": record.get("full_name", ""),
                          "permissions": get_account_permissions(emp_id)})
        return render_template("permissions.html", users=users, available=AVAILABLE_PERMISSIONS)

    @web.get("/payroll")
    @login_required
    def payroll_overview():
        if session.get("role") != "ADMIN" and not can("VIEW_ALL_PAYROLL"):
            abort(403, "You do not have permission to view organization payroll.")
        data = load_employees()
        rows = [{"id": emp_id, "name": record.get("full_name", ""),
                 "department": record.get("department", ""),
                 "pay": payroll(record)}
                for emp_id, record in data.items()]
        return render_template("payroll.html", rows=rows)

    @web.get("/payroll/calculate")
    @login_required
    def calculate_payroll():
        if session["role"] != "ADMIN" and not can("CALCULATE_GROSS_SALARY"):
            abort(403)
        data = load_employees()
        emp_id = request.args.get("employee_id", "").strip().upper()
        record = data.get(emp_id) if emp_id else None
        return render_template("calculate.html", employees=data, employee_id=emp_id,
                               record=record, result=payroll(record) if record else None)

    @web.get("/audit")
    @login_required
    def audit_history():
        if session.get("role") != "ADMIN":
            abort(403, "Only administrators can view the audit trail.")
        from audit_log import load_recent_events
        events = load_recent_events(300)
        return render_template("audit.html", events=events)

    app.register_blueprint(web)
