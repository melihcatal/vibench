from observability_client import ObservabilityClient
from observability_models import LogEvent


def write_structured_log(message: str, level: str = "info") -> dict:
    event = LogEvent(message=message, level=level)
    client = ObservabilityClient()
    dd_log = {
        "message": event.message,
        "service": event.service,
        "status": event.level,
        "env": event.env,
    }
    response = client.submit_logs([dd_log])
    return {"status": response.status_code, "ingested": True}
