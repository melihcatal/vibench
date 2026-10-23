# message_summary.py
# LATER-STEP: Summarize processing results of messages

import json
from typing import List, Any

from messaging_models import Event, ErrorResponse


def summarize(results: List[dict]) -> dict:
    """
    Aggregate statistics about a batch of message processing attempts.

    Args:
        results: List of dicts containing at least a 'status' field ('success' or 'failure')
                 and optionally the original Event payload.
    Returns:
        dict: Summary with counts and a list of any error details.
    """
    success = 0
    failure = 0
    errors = []

    for res in results:
        if res.get("status") == "success":
            success += 1
        else:
            failure += 1
            # Pull out error info if available
            err = res.get("error")
            if err:
                errors.append(
                    {
                        "eventId": res.get("eventId"),
                        "code": err.get("code"),
                        "message": err.get("message"),
                    }
                )

    return {
        "total": success + failure,
        "success": success,
        "failure": failure,
        "errors": errors,
    }


if __name__ == "__main__":
    # Demo data for quick validation
    demo = [
        {
            "eventId": "e1",
            "status": "success",
            "event": Event(
                event_id="e1", data={}, timestamp="2025-08-01T12:00:00Z"
            ).dict(),
        },
        {
            "eventId": "e2",
            "status": "failure",
            "error": ErrorResponse(
                code="MSG001", message="Payload missing", details={}
            ).dict(),
        },
        {"eventId": "e3", "status": "success"},
    ]
    print("Summary:", json.dumps(summarize(demo), indent=2))
