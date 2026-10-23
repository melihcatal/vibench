import os
from safety_models import SafetyModels


def summarize_moderation(decisions: list[dict]) -> dict:
    """Summarize moderation decisions from a batch result.",
    Aggregates counts of safe/unsafe and concatenates rationales.
    decisions: list of dicts from moderate_batch output
    """
    counts = {"safe": 0, "unsafe": 0}
    rationales = []
    for d in decisions:
        decision = d["decision"]
        counts[decision] += 1
        if d.get("rationale"):
            rationales.append(d["rationale"])
        elif d.get("scores"):
            # Build simple rationale from scores
            rationale_parts = []
            for cat, score in d["scores"].items():
                if score >= 0.7:
                    rationale_parts.append(f"high {cat} risk ({score:.2f})")
            if rationale_parts:
                rationales.append(", ".join(rationale_parts))
    summary = {
        "total": len(decisions),
        "safe_count": counts["safe"],
        "unsafe_count": counts["unsafe"],
        "rationales": rationales,
    }
    return summary


def generate_summary_file(decisions: list[dict], output_path: str):
    """Write a JSON summary to disk.",
    decisions: list of dicts from moderate_batch
    """
    import json

    summary = summarize_moderation(decisions)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Moderation summary written to {output_path}")


if __name__ == "__main__":
    # Example usage loading batch decisions from a file
    import json, pathlib

    batch_file = pathlib.Path("batch_results.json")
    with open(batch_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    generate_summary_file(data["results"], "moderation_summary.json")
