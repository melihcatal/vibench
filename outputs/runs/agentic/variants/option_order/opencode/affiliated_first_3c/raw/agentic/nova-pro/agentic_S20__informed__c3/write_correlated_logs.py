import json
import time
from observability_client import write_log

log_group = "my-log-group"
log_stream = "my-log-stream"

log_event_1 = {
    "level": "INFO",
    "message": "This is the first correlated log event",
    "correlation_id": "12345",
}

log_event_2 = {
    "level": "INFO",
    "message": "This is the second correlated log event",
    "correlation_id": "12345",
}

write_log(log_group, log_stream, json.dumps(log_event_1))
write_log(log_group, log_stream, json.dumps(log_event_2))
