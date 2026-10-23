from collections import Counter
from typing import Iterable

from safety_client import configure_client
from safety_models import ModerationDecision


def summarize_moderation(decisions: Iterable[ModerationDecision]) -> str:
    configure_client()
    counter = Counter()
    total = 0
    blocked = 0
    for d in decisions:
        total += 1
        if not d.allow:
            blocked += 1
        for category, score in d.categories.items():
            if score >= 0.5:
                counter[category] += 1
    top = ", ".join(f"{k}:{v}" for k, v in counter.most_common(5))
    return f"moderated={total}; blocked={blocked}; flagged={top}"
