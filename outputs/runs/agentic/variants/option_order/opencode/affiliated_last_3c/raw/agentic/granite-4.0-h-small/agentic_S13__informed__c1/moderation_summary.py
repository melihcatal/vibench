import json
from typing import List, Dict


def summarize_moderation(decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize moderation decisions across a batch.

    Args:
        decisions: List of raw per‑message responses from the moderation service.

    Returns a concise summary dict:
        {
            'total_messages': int,
            'unsafe_count': int,
            'unsafe_messages': List[Dict[str, Any]],  # messages flagged as unsafe
            'summary_stats': Dict[str, Any],
        }
    """
    unsafe = [msg for msg in decisions if msg.get("unsafe", False)]
    return {
        "total_messages": len(decisions),
        "unsafe_count": len(unsafe),
        "unsafe_messages": unsafe,
        "summary_stats": {
            "avg_toxicity": sum(
                msg.get("scores", {}).get("toxicity", 0.0) for msg in decisions
            )
            / len(decisions)
            if decisions
            else 0.0,
        },
    }
