from google.cloud import logging

def summarize_results(results: dict):
    """
    Summarizes message processing results and logs them to Google Cloud Logging.
    """
    client = logging.Client()
    logger = client.logger("message_processing_summary")

    logger.log_struct(
        {"summary": "Message processing results", "results": results},
        severity="INFO"
    )
