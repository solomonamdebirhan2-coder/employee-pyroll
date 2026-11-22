"""Private web interface for Employee Payroll Management System."""
import json
import os
import secrets
import time
from collections import defaultdict, deque
from pathlib import Path
from functools import wraps

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

from auth import authenticate, change_password as save_new_password, get_account_permissions, is_account_active
from audit_log import record_event

BASE_DIR = Path(__file__).resolve().parent
EMPLOYEE_FILE = BASE_DIR / "employees.txt"
SECRET_FILE = BASE_DIR / ".flask_secret"

def load_employees():
    from storage import postgres_enabled, load_collection
    if postgres_enabled():
        return load_collection("employees", {})
    try:
        data = json.loads(EMPLOYEE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("Employee data could not be loaded safely.") from exc
    if not isinstance(data, dict):
        raise RuntimeError("Employee data has an invalid format.")
    return data

def get_secret():
    configured = os.environ.get("SECRET_KEY")
    if configured:
        if len(configured) < 32:
            raise RuntimeError("SECRET_KEY must contain at least 32 characters.")
        return configured
    if SECRET_FILE.exists():
        value = SECRET_FILE.read_text(encoding="utf-8").strip()
        if len(value) < 32:
            raise RuntimeError("The local Flask secret is invalid. Remove .flask_secret and restart.")
        return value
    value = secrets.token_urlsafe(48)
    SECRET_FILE.write_text(value, encoding="utf-8")
    try:
        os.chmod(SECRET_FILE, 0o600)
    except OSError:
        pass
    return value

app = Flask(__name__)
app.config.update(
    SECRET_KEY=get_secret(),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "0") == "1",
    PERMANENT_SESSION_LIFETIME=1800,
    MAX_CONTENT_LENGTH=16 * 1024,
)

# Basic per-IP login throttling. Production deployment should also use proxy/server limits.
login_attempts = defaultdict(deque)

@app.before_request
def csrf_and_session_guard():
    if request.method == "POST":
        token = session.get("_csrf")
        supplied = request.form.get("_csrf", "")
        if not token or not secrets.compare_digest(token, supplied):
            abort(400, "Invalid form token. Refresh the page and try again.")
    if session.get("employee_id"):
        session.permanent = True

@app.context_processor
def inject_csrf():
    if "_csrf" not in session:
        session["_csrf"] = secrets.token_urlsafe(32)
    return {"csrf_token": session["_csrf"]}

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("employee_id"):
            return redirect(url_for("login"))
        employee_id = session["employee_id"]
        employee = load_employees().get(employee_id)
        if not is_account_active(employee_id) or not employee or employee.get("account_status", "ACTIVE") != "ACTIVE":
            session.clear()
            flash("Your account is inactive. Contact the administrator.", "error")
            return redirect(url_for("login"))
        if session.get("must_change_password") and request.endpoint != "change_password":
            return redirect(url_for("change_password"))
        return view(*args, **kwargs)
    return wrapped

def payroll(record):
    basic = float(record.get("basic_salary", 0) or 0)
    allowances = sum(float(record.get(key, 0) or 0) for key in
                     ("house_allowance", "transport_allowance", "other_allowance"))
    gross = basic + allowances
    pension = basic * 0.07
    if gross <= 2000:
        rate, deduction = 0, 0
    elif gross <= 4000:
        rate, deduction = .15, 300
    elif gross <= 7000:
        rate, deduction = .20, 500
    elif gross <= 10000:
        rate, deduction = .25, 850
    elif gross <= 14000:
        rate, deduction = .30, 1350
    else:
        rate, deduction = .35, 2050
    tax = max(0, gross * rate - deduction)
    return {"basic": basic, "allowances": allowances, "gross": gross,
            "pension": pension, "tax": tax, "net": gross - pension - tax}

@app.get("/")
def index():
    return redirect(url_for("dashboard") if session.get("employee_id") else url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        ip = request.remote_addr or "unknown"
        now = time.time()
        attempts = login_attempts[ip]
        while attempts and now - attempts[0] > 600:
            attempts.popleft()
        if len(attempts) >= 5:
            flash("Too many login attempts. Wait 10 minutes and try again.", "error")
            return render_template("login.html"), 429
        employee_id = request.form.get("employee_id", "").strip().upper()
        password = request.form.get("password", "")
        result = authenticate(employee_id, password)
        if not result:
            attempts.append(now)
            flash("Employee ID or password is incorrect, or the account is inactive.", "error")
            return render_template("login.html"), 401
        employee = load_employees().get(employee_id)
        if not employee or employee.get("account_status", "ACTIVE") != "ACTIVE":
            attempts.append(now)
            flash("This employee record is inactive. Contact the administrator.", "error")
            return render_template("login.html"), 403
        attempts.clear()
        session.clear()
        session["employee_id"] = employee_id
        session["role"] = result["role"]
        session["must_change_password"] = result["must_change_password"]
        session["_csrf"] = secrets.token_urlsafe(32)
        try:
            record_event(employee_id, "LOGIN_SUCCESS", employee_id, {"role": result["role"]})
        except OSError:
            app.logger.exception("Could not write login audit event.")
        if result["must_change_password"]:
            return redirect(url_for("change_password"))
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.get("/dashboard")
@login_required
def dashboard():
    employees = load_employees()
    employee_id = session["employee_id"]
    own = employees.get(employee_id)
    if not own or own.get("account_status", "ACTIVE") != "ACTIVE":
        session.clear()
        flash("Your account is inactive. Contact the administrator.", "error")
        return redirect(url_for("login"))
    own_payroll = payroll(own)
    is_admin = session["role"] == "ADMIN"
    all_employees = []
    if is_admin:
        for key, record in employees.items():
            all_employees.append({"id": key, "name": record.get("full_name", ""),
                                  "department": record.get("department", ""),
                                  "position": record.get("position", ""),
                                  "payroll": payroll(record)})
    return render_template("dashboard.html", employee=own, employee_id=employee_id,
                           payroll=own_payroll, is_admin=is_admin,
                           all_employees=all_employees,
                           permissions=get_account_permissions(employee_id))

@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        new = request.form.get("new_password", "")
        confirm = request.form.get("confirm_password", "")
        if new != confirm:
            flash("The passwords do not match.", "error")
        else:
            try:
                if not session.get("must_change_password"):
                    current = request.form.get("current_password", "")
                    if not authenticate(session["employee_id"], current):
                        raise ValueError("Current password is incorrect.")
                save_new_password(session["employee_id"], new)
                try:
                    record_event(session["employee_id"], "PASSWORD_CHANGED", session["employee_id"])
                except OSError:
                    app.logger.exception("Could not write password-change audit event.")
                session["must_change_password"] = False
                flash("Password updated successfully.", "success")
                return redirect(url_for("dashboard"))
            except ValueError as exc:
                flash(str(exc), "error")
    return render_template("change_password.html")

@app.post("/logout")
@login_required
def logout():
    try:
        record_event(session.get("employee_id"), "LOGOUT", session.get("employee_id"))
    except OSError:
        app.logger.exception("Could not write logout audit event.")
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

@app.errorhandler(403)
@app.errorhandler(404)
def access_error(error):
    message = "You do not have permission to access this page." if error.code == 403 else "The requested page or record was not found."
    return render_template("error.html", message=message), error.code

@app.errorhandler(400)
def bad_request(error):
    return render_template("error.html", message=getattr(error, "description", "Bad request.")), 400

from web_features import setup_web_routes
setup_web_routes(app, login_required, load_employees, payroll)

if __name__ == "__main__":
    # Safe local default. Set HOST=0.0.0.0 only for deliberate LAN testing or deployment.
    app.run(host=os.environ.get("HOST", "127.0.0.1"),
            port=int(os.environ.get("PORT", "5000")), debug=False)
