"""Explicit one-time import of local JSON data into PostgreSQL.

Run only after setting DATABASE_URL to the intended private database:
    python migrate_to_postgres.py --confirm
"""
import argparse
import json
from pathlib import Path

from storage import import_local_json

BASE = Path(__file__).resolve().parent

def read_json(filename, default):
    path = BASE / filename
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    parser = argparse.ArgumentParser(description="Import local payroll data into PostgreSQL.")
    parser.add_argument("--confirm", action="store_true",
                        help="Confirm that private employee/account data may be copied to DATABASE_URL.")
    args = parser.parse_args()
    if not args.confirm:
        parser.error("No data was transferred. Re-run with --confirm only after checking DATABASE_URL.")
    employees = read_json("employees.txt", {})
    accounts = read_json("accounts.txt", {})
    requests = read_json("requests.txt", [])
    counts = import_local_json(employees, accounts, requests)
    print("Import completed. Record counts:", counts)
    print("Keep local JSON backups securely. Do not upload them to GitHub.")

if __name__ == "__main__":
    main()
