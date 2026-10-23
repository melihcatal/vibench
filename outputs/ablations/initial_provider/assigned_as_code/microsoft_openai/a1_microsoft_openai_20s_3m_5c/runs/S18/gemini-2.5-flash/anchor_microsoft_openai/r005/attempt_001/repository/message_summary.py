from typing import List
from messaging_models import MessageResult

def summarize_results(results: List[MessageResult]):
    total_messages = len(results)
    successful_messages = sum(1 for r in results if r.status == "published")
    failed_messages = total_messages - successful_messages

    summary = {
        "total_messages": total_messages,
        "successful_messages": successful_messages,
        "failed_messages": failed_messages,
        "details": [
            {"message_id": r.message_id, "status": r.status, "details": r.details}
            for r in results
        ]
    }
    return summary
