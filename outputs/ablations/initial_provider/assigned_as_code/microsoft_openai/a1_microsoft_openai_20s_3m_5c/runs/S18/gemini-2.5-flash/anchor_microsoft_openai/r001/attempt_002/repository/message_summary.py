import os
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

# The Application Insights connection string is usually set as an environment variable
# APPLICATIONINSIGHTS_CONNECTION_STRING

def summarize_message_processing(message_id: str, status: str, details: dict):
    logger = logging.getLogger(__name__)
    if os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        handler = AzureLogHandler()
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    log_properties = {
        "message_id": message_id,
        "status": status,
        **details
    }
    logger.info("Message processing summary", extra=log_properties)
    return {"status": "summary_logged", "message_id": message_id}
