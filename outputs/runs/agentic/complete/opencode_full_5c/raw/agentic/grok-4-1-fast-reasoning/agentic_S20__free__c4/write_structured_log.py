from typing import Dict, Any, Optional
from observability_client import CloudWatchLogWriter, get_log_group, get_log_stream
import json


def write_structured_log(
    level: str, message: str, extra: Optional[Dict[str, Any]] = None
):
    log_data = {"level": level, "message": message}
    if extra is not None:
        log_data["extra"] = extra
    writer = CloudWatchLogWriter(get_log_group(), get_log_stream())
    writer.write(log_data)
