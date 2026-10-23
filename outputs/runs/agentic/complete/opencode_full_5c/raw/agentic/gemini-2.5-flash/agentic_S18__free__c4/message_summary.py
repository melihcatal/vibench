from typing import List, Dict, Any


def summarize_message_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarizes a list of message processing results.

    Args:
        results: A list of dictionaries, where each dictionary represents the
                 result of processing a single message. Each result should ideally
                 contain a 'status' key (e.g., 'success', 'failure', 'dead_letter').

    Returns:
        A dictionary containing the summary, e.g., total messages, counts by status.
    """
    summary = {
        "total_messages_processed": len(results),
        "status_counts": {},
        "successful_messages": [],
        "failed_messages": [],
        "dead_lettered_messages": [],
    }

    for result in results:
        status = result.get("status", "unknown")
        summary["status_counts"][status] = summary["status_counts"].get(status, 0) + 1

        if status == "success":
            summary["successful_messages"].append(result.get("message_id", "N/A"))
        elif status == "failure":
            summary["failed_messages"].append(result.get("message_id", "N/A"))
        elif status == "dead_letter":
            summary["dead_lettered_messages"].append(result.get("message_id", "N/A"))

    return summary
