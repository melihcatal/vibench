from google.cloud import logging

def summarize_message_processing(message_id: str, status: str, details: dict):
    """
    Summarizes message processing results by logging them to Google Cloud Logging.

    Args:
        message_id: The ID of the processed message.
        status: The processing status (e.g., "success", "failure", "skipped").
        details: A dictionary containing additional processing details.
    """
    logging_client = logging.Client()
    logger = logging_client.logger("message_processing_summary")

    log_entry = {
        "message_id": message_id,
        "status": status,
        "details": details,
    }

    logger.log_struct(log_entry, severity="INFO")
