from datetime import datetime, timezone
from uuid import uuid4

from observability_client import put_structured_event


def main() -> None:
    correlation_id = str(uuid4())
    for step in ["received", "validated", "persisted"]:
        put_structured_event({"timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "message": f"request {step}", "severity": "INFO", "correlation_id": correlation_id, "step": step})


if __name__ == "__main__":
    main()
