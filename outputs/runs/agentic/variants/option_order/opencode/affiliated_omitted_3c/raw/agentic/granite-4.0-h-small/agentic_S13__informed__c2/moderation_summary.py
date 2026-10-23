import json


def summarize_moderation(results: list[dict]) -> dict:
    """Summarize a list of moderation results.

    Returns a JSON string with counts and categories.
    """
    decision_counts = {"safe": 0, "unsafe": 0}
    category_flags = {}
    for rec in results:
        decision = rec["decision"].lower()
        decision_counts[decision] += 1
        for flag in rec.get("flags", []):
            category_flags[flag] = category_flags.get(flag, 0) + 1
    return {
        "summary": {
            "total": len(results),
            "safe": decision_counts["safe"],
            "unsafe": decision_counts["unsafe"],
            "flags": category_flags,
        }
    }
