# [LATER-STEP] moderation_summary.py
"""Summarize moderation decisions for reporting or storage.
Uses data from earlier safety integration files.
"""

from dataclasses import dataclass
from typing import List
from safety_models import ModerationResponse

decision_map = {True: "ALLOWED", False: "FLAGGED"}


@dataclass
class ModerationSummary:
    message_id: str
    text: str
    safe: bool
    reasons: List[str]


def summarize(decision: bool, resp: ModerationResponse) -> ModerationSummary:
    safe = decision
    # Extract categories that triggered the decision (example logic)
    reasons = [cat for cat, score in resp.categories.items() if score > 0.5]
    return ModerationSummary(
        message_id="msg-123", text="Sample user text", safe=safe, reasons=reasons
    )
