import os
import logging
from google.cloud import logging as cloud_logging

# Configure logging to send to Google Cloud Logging
client = cloud_logging.Client()
handler = client.get_default_handler()
cloud_logger = logging.getLogger("message_summary_logger")
cloud_logger.setLevel(logging.INFO)
cloud_logger.addHandler(handler)

def summarize_message_processing(message_id: str, status: str, details: dict = None):
    log_entry = {
        "message_id": message_id,
        "status": status,
        "details": details or {}
    }
    cloud_logger.info("Message processing summary", extra={'json_fields': log_entry})
