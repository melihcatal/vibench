import json
import time
from observability_client import write_log

log_group = "my-log-group"
log_stream = "my-log-stream"

log_event = {
    "level": "INFO",
    "message": "This is a structured log event",
    "correlation_id": "12345",
}

write_log(log_group, log_stream, json.dumps(log_event))
