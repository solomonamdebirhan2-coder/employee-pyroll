"""Storage adapter: local JSON for development, PostgreSQL for hosted deployment."""
import json
import os

_TABLES = {
    "employees": "payroll_employees",
    "accounts": "payroll_accounts",
    "requests": "payroll_requests",
}

def database_url():
    value = os.environ.get("DATABASE_URL", "").strip()
    if value.startswith("postgres://"):
        value = "postgresql://" + value[len("postgres://"):]
    return value

def postgres_enabled():
    return bool(database_url())

def _connect():
    dsn = database_url()
    if not dsn:
        raise RuntimeError("DATABASE_URL is not configured.")
    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError("Install the PostgreSQL dependency with pip install -r requirements.txt.") from exc
    connection = psycopg.connect(dsn, connect_timeout=10)
    with connection.cursor() as cursor:
        for table in _TABLES.values():
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table} (record_key TEXT PRIMARY KEY, payload JSONB NOT NULL)"
            )
    connection.commit()
    return connection

def _pairs(name, records):
    if name == "requests":
        return [(str(item["request_id"]), item) for item in records]
    return [(str(key), value) for key, value in records.items()]

def load_collection(name, default):
    if name not in _TABLES:
        raise ValueError("Unknown storage collection.")
    if not postgres_enabled():
        return default
    table = _TABLES[name]
    with _connect() as connection:
        rows = connection.execute(f"SELECT record_key, payload FROM {table}").fetchall()
    if name == "requests":
        return [payload for _, payload in rows]
    return {key: payload for key, payload in rows}

def save_collection(name, records):
    if name not in _TABLES:
        raise ValueError("Unknown storage collection.")
    if not postgres_enabled():
        raise RuntimeError("PostgreSQL storage is not enabled.")
    table = _TABLES[name]
    pairs = _pairs(name, records)
    with _connect() as connection:
        with connection.transaction():
            connection.execute(f"LOCK TABLE {table} IN EXCLUSIVE MODE")
            connection.execute(f"DELETE FROM {table}")
            if pairs:
                connection.executemany(
                    f"INSERT INTO {table} (record_key, payload) VALUES (%s, %s::jsonb)",
                    [(key, json.dumps(value, ensure_ascii=False)) for key, value in pairs],
                )

def import_local_json(employees, accounts, requests):
    """Import local JSON records into an empty PostgreSQL database atomically."""
    if not postgres_enabled():
        raise RuntimeError("Set DATABASE_URL before importing.")
    if not employees or not accounts:
        raise ValueError("Employee and account data must both be non-empty.")
    collections = {"employees": employees, "accounts": accounts, "requests": requests}
    with _connect() as connection:
        with connection.transaction():
            for table in _TABLES.values():
                connection.execute(f"LOCK TABLE {table} IN EXCLUSIVE MODE")
                count = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                if count:
                    raise RuntimeError("The destination database is not empty. Import cancelled to prevent overwriting.")
            for name, records in collections.items():
                table = _TABLES[name]
                pairs = _pairs(name, records)
                if pairs:
                    connection.executemany(
                        f"INSERT INTO {table} (record_key, payload) VALUES (%s, %s::jsonb)",
                        [(key, json.dumps(value, ensure_ascii=False)) for key, value in pairs],
                    )
    return {"employees": len(employees), "accounts": len(accounts), "requests": len(requests)}

def save_audit_event(event):
    if not postgres_enabled():
        raise RuntimeError("PostgreSQL storage is not enabled.")
    with _connect() as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS payroll_audit_events (event_id BIGSERIAL PRIMARY KEY, payload JSONB NOT NULL)"
        )
        connection.execute(
            "INSERT INTO payroll_audit_events (payload) VALUES (%s::jsonb)",
            [json.dumps(event, ensure_ascii=False)],
        )

def load_audit_events(limit=300):
    if not postgres_enabled():
        return []
    with _connect() as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS payroll_audit_events (event_id BIGSERIAL PRIMARY KEY, payload JSONB NOT NULL)"
        )
        rows = connection.execute(
            "SELECT payload FROM payroll_audit_events ORDER BY event_id DESC LIMIT %s",
            [max(1, min(int(limit), 1000))],
        ).fetchall()
    return [payload for (payload,) in rows]
