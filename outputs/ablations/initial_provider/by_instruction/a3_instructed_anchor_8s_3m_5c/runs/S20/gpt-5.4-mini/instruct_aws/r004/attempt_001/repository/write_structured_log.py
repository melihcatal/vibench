from datetime import datetime, timezone

from observability_client import put_structured_event


def main() -> None:
    put_structured_event({"timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "message": "structured event written", "severity": "INFO", "service": "orders", "event_type": "structured_log"})


if __name__ == "__main__":
    main()
