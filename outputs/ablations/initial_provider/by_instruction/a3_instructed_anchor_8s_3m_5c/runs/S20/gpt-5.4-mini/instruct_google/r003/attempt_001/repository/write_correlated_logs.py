import os
import uuid

from observability_client import write_json_log
from observability_models import LogWriteRequest, utc_now_iso


def main() -> list:
    request_id = str(uuid.uuid4())
    log_name = os.getenv("GOOGLE_CLOUD_LOG_NAME", "structured_app_log")
    return [
        write_json_log(LogWriteRequest(log_name=log_name, payload={"message": "request_started", "request_id": request_id, "timestamp": utc_now_iso()}, severity="INFO")),
        write_json_log(LogWriteRequest(log_name=log_name, payload={"message": "request_finished", "request_id": request_id, "timestamp": utc_now_iso(), "status": "ok"}, severity="INFO")),
    ]
