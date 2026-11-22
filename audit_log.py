"""Append-only audit event storage for local and hosted modes."""
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
AUDIT_FILE = BASE / "audit_log.txt"

def record_event(actor_id, action, target_id=None, details=None):
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "actor_id": actor_id or "SYSTEM",
        "action": str(action)[:80],
        "target_id": target_id,
        "details": details or {},
    }
    from storage import postgres_enabled, save_audit_event
    if postgres_enabled():
        save_audit_event(event)
    else:
        with AUDIT_FILE.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event

def load_recent_events(limit=300):
    from storage import postgres_enabled, load_audit_events
    if postgres_enabled():
        return load_audit_events(limit)
    if not AUDIT_FILE.exists():
        return []
    events = []
    for line in AUDIT_FILE.read_text(encoding="utf-8").splitlines()[-limit:]:
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return list(reversed(events))
