def summarize_processing_results(processing_outcomes: list) -> dict:
    # This module summarizes results from message processing,
    # often originating from messaging systems like Google Cloud Pub/Sub.
    # The 'message_id' field in the outcomes typically refers to
    # Google Cloud Pub/Sub message IDs or similar unique identifiers.

    summary = {
        "total_messages": len(processing_outcomes),
        "success_count": 0,
        "failure_count": 0,
        "unacknowledged_count": 0,
        "other_status_counts": {},
        "summary_message": ""
    }

    for outcome in processing_outcomes:
        status = outcome.get("status", "UNKNOWN").upper()
        if status == "SUCCESS":
            summary["success_count"] += 1
        elif status == "FAILURE":
            summary["failure_count"] += 1
        elif status == "UNACKNOWLEDGED":
            summary["unacknowledged_count"] += 1
        else:
            summary["other_status_counts"][status] = summary["other_status_counts"].get(status, 0) + 1

    summary["summary_message"] = (
        f"Processed {summary['total_messages']} messages: "
        f"{summary['success_count']} successful, "
        f"{summary['failure_count']} failed, "
        f"{summary['unacknowledged_count']} unacknowledged."
    )

    if summary["other_status_counts"]:
        other_details = ", ".join([
            f"{count} {status.lower()}"
            for status, count in summary["other_status_counts"].items()
        ])
        summary["summary_message"] += f" Also, {other_details}."

    return summary
