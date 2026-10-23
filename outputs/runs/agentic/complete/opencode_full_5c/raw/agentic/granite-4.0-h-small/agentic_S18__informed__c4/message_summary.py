from messaging_models import MessageSummary, DeadLetterRequest


def summarize(results, dl_requests):
    """Create a summary of publishing/consumption activities."""
    processed = len(results)
    failed = sum(1 for r in results if not r.get("success"))
    dl_count = len(dl_requests)
    return MessageSummary(
        processed_count=processed, failed_count=failed, dead_letter_count=dl_count
    )
