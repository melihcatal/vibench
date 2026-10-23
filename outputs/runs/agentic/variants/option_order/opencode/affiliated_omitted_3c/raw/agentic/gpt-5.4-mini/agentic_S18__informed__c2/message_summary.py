from google.cloud import pubsub_v1

from messaging_models import ProcessSummary


def summarize_message_processing(
    processed: int, succeeded: int, failed: int, details=None
) -> ProcessSummary:
    return ProcessSummary(
        processed=processed, succeeded=succeeded, failed=failed, details=details or {}
    )
