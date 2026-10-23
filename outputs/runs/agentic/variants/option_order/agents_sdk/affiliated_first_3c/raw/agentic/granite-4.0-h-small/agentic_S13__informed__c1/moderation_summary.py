# [LATER-STEP] moderation_summary.py

from safety_models import SafetyResponseBatch
from collections import Counter

# Concise summary of moderation decisions for a batch of texts

def moderation_summary(batch_response: SafetyResponseBatch) -> Dict[str, Any]:
    """Returns a short report summarizing per‑category safety scores.

    The report includes total unsafe counts, highest‑scoring category, and overall safe rate.
    """
    results = batch_response.results
    total_unsafe = sum(1 for r in results if r.overall_verdict == "unsafe")
    verdicts = [r.overall_verdict for r in results]
    overall_safe_rate = verdicts.count("safe") / len(verdicts)

    # Highest scoring unsafe category across the batch (ignoring neutral / safe scores)
    unsafe_scores = Counter()
    for r in results:
        if r.overall_verdict == "unsafe":
            for cat, score in r.category_scores.items():
                unsafe_scores[cat] += score
    top_unsafe_category = unsafe_scores.most_common(1)[0][0] if unsafe_scores else "none"

    return {
        "total_unsafe": total_unsafe,
        "overall_safe_rate": overall_safe_rate,
        "top_unsafe_category": top_unsafe_category,
        "batch_details": [asdict(r) for r in results],
    }
