import tempfile
import unittest
import io
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import auth
import request_manager


class SecurityWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        auth.ACCOUNT_FILE = root / "accounts.json"
        request_manager.REQUEST_FILE = root / "requests.json"
        self.employees = {
            "TTBR/0030/18": {"full_name": "Brhanu Kasahun", "phone": "+251911111111"},
            "TTBR/0226/18": {"full_name": "Solomon Amdebirhan", "phone": "+251922222222"},
        }

    def tearDown(self):
        self.temp.cleanup()

    def test_first_run_creates_brhanu_as_admin_and_users_as_temporary_accounts(self):
        with patch.object(auth, "read_password", side_effect=["StrongPass1", "StrongPass1"]), \
             patch.object(auth.secrets, "token_urlsafe", return_value="TempPass123"), \
             redirect_stdout(io.StringIO()):
            accounts = auth.initialize_accounts(list(self.employees.keys()))
        self.assertEqual(accounts["TTBR/0030/18"]["role"], "ADMIN")
        self.assertEqual(accounts["TTBR/0226/18"]["role"], "USER")
        self.assertTrue(accounts["TTBR/0226/18"]["must_change_password"])
        self.assertIsNotNone(auth.authenticate("TTBR/0030/18", "StrongPass1"))
        self.assertIsNotNone(auth.authenticate("TTBR/0226/18", "TempPass123"))

    def test_admin_can_grant_and_revoke_limited_permissions(self):
        auth._save_accounts({
            "TTBR/0030/18": auth._new_account("ADMIN", "admin-test"),
            "TTBR/0226/18": auth._new_account("USER", "employee-test", True),
        })
        granted = auth.update_account_permissions("TTBR/0030/18", "TTBR/0226/18", "VIEW_ALL_PAYROLL", True)
        self.assertEqual(granted, ["VIEW_ALL_PAYROLL"])
        self.assertEqual(auth.get_account_permissions("TTBR/0226/18"), ["VIEW_ALL_PAYROLL"])
        revoked = auth.update_account_permissions("TTBR/0030/18", "TTBR/0226/18", "VIEW_ALL_PAYROLL", False)
        self.assertEqual(revoked, [])
        with self.assertRaises(PermissionError):
            auth.update_account_permissions("TTBR/0226/18", "TTBR/0226/18", "VIEW_ALL_PAYROLL", True)

    def test_password_hash_and_change(self):
        accounts = {"TTBR/0226/18": auth._new_account("USER", "StartPass1", True)}
        auth._save_accounts(accounts)
        self.assertIsNotNone(auth.authenticate("TTBR/0226/18", "StartPass1"))
        self.assertTrue(auth.authenticate("TTBR/0226/18", "StartPass1")["must_change_password"])
        auth.change_password("TTBR/0226/18", "NewPass123")
        session = auth.authenticate("TTBR/0226/18", "NewPass123")
        self.assertIsNotNone(session)
        self.assertFalse(session["must_change_password"])
        self.assertIsNone(auth.authenticate("TTBR/0226/18", "StartPass1"))

    def test_employee_request_requires_admin_approval(self):
        item = request_manager.submit_change(
            "TTBR/0226/18", "TTBR/0226/18", "USER",
            "phone", "+251933333333", "Correcting phone", self.employees
        )
        with self.assertRaises(PermissionError):
            request_manager.decide_request(
                item["request_id"], "TTBR/0226/18", "USER", "APPROVED",
                self.employees, lambda: None, lambda *_: None
            )
        request_manager.decide_request(
            item["request_id"], "TTBR/0030/18", "ADMIN", "APPROVED",
            self.employees, lambda: None, lambda *_: None
        )
        self.assertEqual(self.employees["TTBR/0226/18"]["phone"], "+251933333333")

    def test_admin_request_requires_specific_employee(self):
        item = request_manager.submit_change(
            "TTBR/0226/18", "TTBR/0030/18", "ADMIN",
            "full_name", "Solomon A. Amdebirhan", "Correct official name", self.employees
        )
        with self.assertRaises(PermissionError):
            request_manager.decide_request(
                item["request_id"], "TTBR/0030/18", "ADMIN", "APPROVED",
                self.employees, lambda: None, lambda *_: None
            )
        request_manager.decide_request(
            item["request_id"], "TTBR/0226/18", "USER", "APPROVED",
            self.employees, lambda: None, lambda *_: None
        )
        self.assertEqual(self.employees["TTBR/0226/18"]["full_name"], "Solomon A. Amdebirhan")

    def test_requester_cannot_approve_own_request(self):
        item = request_manager.submit_change(
            "TTBR/0226/18", "TTBR/0226/18", "USER",
            "phone", "+251944444444", "Test own approval block", self.employees
        )
        with self.assertRaises(PermissionError):
            request_manager.decide_request(
                item["request_id"], "TTBR/0226/18", "USER", "APPROVED",
                self.employees, lambda: None, lambda *_: None
            )

    def test_deactivation_is_not_hard_delete(self):
        item = request_manager.submit_deactivation(
            "TTBR/0226/18", "TTBR/0226/18", "USER", "Leaving organization", self.employees
        )
        request_manager.decide_request(
            item["request_id"], "TTBR/0030/18", "ADMIN", "APPROVED",
            self.employees, lambda: None, lambda *_: None
        )
        self.assertIn("TTBR/0226/18", self.employees)
        self.assertEqual(self.employees["TTBR/0226/18"]["account_status"], "INACTIVE")

    def test_rejected_request_does_not_change_employee_data(self):
        item = request_manager.submit_change(
            "TTBR/0226/18", "TTBR/0226/18", "USER",
            "phone", "+251955555555", "Correction request", self.employees
        )
        request_manager.decide_request(
            item["request_id"], "TTBR/0030/18", "ADMIN", "REJECTED",
            self.employees, lambda: None, lambda *_: None
        )
        self.assertEqual(self.employees["TTBR/0226/18"]["phone"], "+251922222222")

    def test_duplicate_pending_change_is_blocked(self):
        request_manager.submit_change(
            "TTBR/0226/18", "TTBR/0226/18", "USER",
            "phone", "+251966666666", "First request", self.employees
        )
        with self.assertRaises(ValueError):
            request_manager.submit_change(
                "TTBR/0226/18", "TTBR/0226/18", "USER",
                "phone", "+251977777777", "Second request", self.employees
            )


if __name__ == "__main__":
    unittest.main()
