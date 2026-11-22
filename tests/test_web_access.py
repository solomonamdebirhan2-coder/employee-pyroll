"""Access-control regression tests for the Flask payroll portal."""
import unittest
from unittest.mock import patch

import app as web_app
from auth import _load_accounts


class WebAccessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.employees = web_app.load_employees()
        cls.accounts = _load_accounts()
        cls.admin_id = "TTBR/0030/18"
        active_users = [
            key for key, record in cls.employees.items()
            if key != cls.admin_id
            and key in cls.accounts
            and cls.accounts[key].get("active", False)
            and record.get("account_status", "ACTIVE") == "ACTIVE"
        ]
        cls.user_id = active_users[0]
        cls.other_id = active_users[1]

    def setUp(self):
        self.client = web_app.app.test_client()

    def login_session(self, employee_id, role):
        with self.client.session_transaction() as state:
            state.clear()
            state["employee_id"] = employee_id
            state["role"] = role
            state["must_change_password"] = False
            state["_csrf"] = "test-csrf-token"

    def test_admin_can_open_management_pages(self):
        self.login_session(self.admin_id, "ADMIN")
        for path in (
            "/dashboard", "/employees", "/employees/register",
            "/requests", "/permissions", "/payroll", "/payroll/calculate", "/audit",
            f"/employees/{self.user_id}"
        ):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_employee_cannot_open_admin_only_pages(self):
        self.login_session(self.user_id, "USER")
        # Isolate the no-special-permissions case; some local accounts may have
        # explicitly delegated employee-search or registration permissions.
        with patch("web_features.get_account_permissions", return_value=[]):
            for path in ("/employees", "/employees/register", "/permissions", "/audit"):
                with self.subTest(path=path):
                    self.assertEqual(self.client.get(path).status_code, 403)

    def test_employee_cannot_open_another_full_employee_record(self):
        self.login_session(self.user_id, "USER")
        with patch("web_features.get_account_permissions", return_value=[]):
            self.assertEqual(self.client.get(f"/employees/{self.other_id}").status_code, 403)

    def test_admin_dashboard_shows_management_actions(self):
        self.login_session(self.admin_id, "ADMIN")
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        for label in ("Register employee", "Search employees", "Change requests",
                      "Organization payroll", "Calculate salary", "Special permissions",
                      "Security audit"):
            with self.subTest(label=label):
                self.assertIn(label, body)

    def test_employee_dashboard_does_not_show_other_employee_names(self):
        self.login_session(self.user_id, "USER")
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        for employee_id, record in self.employees.items():
            if employee_id != self.user_id:
                self.assertNotIn(str(record.get("full_name", "")), body)

    def test_employee_without_permissions_cannot_calculate_other_payroll(self):
        self.login_session(self.user_id, "USER")
        with patch("web_features.get_account_permissions", return_value=[]):
            self.assertEqual(self.client.get("/payroll/calculate").status_code, 403)

    def test_employee_without_permissions_cannot_view_organization_payroll(self):
        self.login_session(self.user_id, "USER")
        with patch("web_features.get_account_permissions", return_value=[]):
            self.assertEqual(self.client.get("/payroll").status_code, 403)

    def test_post_without_csrf_token_is_rejected(self):
        self.login_session(self.admin_id, "ADMIN")
        response = self.client.post("/logout")
        self.assertEqual(response.status_code, 400)

    def test_no_public_employee_registration_route(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
