import uuid

from observability_client import write_event
from observability_models import LogEvent


def main() -> list:
    request_id = str(uuid.uuid4())
    events = [
        LogEvent(message="request received", severity="INFO", fields={"request_id": request_id, "step": "start"}),
        LogEvent(message="request validated", severity="INFO", fields={"request_id": request_id, "step": "validate"}),
        LogEvent(message="request completed", severity="INFO", fields={"request_id": request_id, "step": "end"}),
    ]
    return [write_event(event, log_name="correlated-log") for event in events]


if __name__ == "__main__":
    main()
