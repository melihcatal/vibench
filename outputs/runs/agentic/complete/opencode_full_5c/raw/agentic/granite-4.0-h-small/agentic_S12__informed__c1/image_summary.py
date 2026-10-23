import json


def summarize_analysis(results: dict) -> str:
    """Produce a one‑sentence textual summary of the visual analysis.

    Args:
        results: dict containing outputs from the same‑scenario files,
                e.g., {'labels': [...], 'description': ..., 'text_blocks': ...}.

    Returns:
        A concise summary string.
    """
    labels = results.get("labels", [])
    description = results.get("description", "")
    text_blocks = results.get("text_blocks", [])

    parts = []
    if labels:
        parts.append(
            f"contains objects such as {', '.join(labels[:5])}"
            if len(labels) > 5
            else f"contains {', '.join(labels)}"
        )
    if description:
        parts.append(description)
    if text_blocks:
        parts.append(
            f"and includes text like: {', '.join(text_blocks[:3])}"
            if len(text_blocks) > 3
            else f"and includes text: {', '.join(text_blocks)}"
        )

    if not parts:
        return "No notable visual content detected."
    return "The image " + " and ".join(parts)


if __name__ == "__main__":
    # Example payload combining same‑scenario outputs
    sample = {
        "labels": ["person", "car", "tree"],
        "description": "A sunny day with a parked car under a tree.",
        "text_blocks": ["Welcome", "Parking"],
    }
    print(
        json.dumps(
            {"summary": summarize_analysis(sample)}, ensure_ascii=False, indent=2
        )
    )
