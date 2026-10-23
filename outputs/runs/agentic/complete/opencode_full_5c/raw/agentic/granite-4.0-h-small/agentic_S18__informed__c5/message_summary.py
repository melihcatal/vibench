from typing import List, Dict, Any

from .messaging_models import PublishResponse, ConsumeResponse, BatchPublishResponse


def message_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize processing results after batch publish and consume.
    Returns a summary dict.
    """
    return {
        "total_published": len(results),
        "total_consumed": sum(1 for r in results if r.get("consumed")),
        "unprocessed": sum(1 for r in results if not r.get("consumed")),
    }


# Example usage helper (not required by spec)
def summarize_processed(published_ids: List[str], consumed: List[ConsumeResponse]):
    published_cnt = len(published_ids)
    consumed_cnt = len(consumed)
    return {
        "published_count": published_cnt,
        "consumed_count": consumed_cnt,
        "pending_count": published_cnt - consumed_cnt,
    }


# No return needed for the tool, just write the file
