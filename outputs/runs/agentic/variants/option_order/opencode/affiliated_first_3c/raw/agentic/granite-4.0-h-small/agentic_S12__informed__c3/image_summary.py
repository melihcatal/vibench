# [LATER-STEP] image_summary.py
# Summarize results from multiple visual analysis steps into a concise report
from typing import List, Dict
from vision_models import VisionResponse

SENTIMENT_POS = ["beautiful", "amazing", "stunning", "vivid"]
SENTIMENT_NEG = ["gruesome", "disturbing", "horrifying"]


def summarize_responses(responses: List[Dict[str, VisionResponse]]) -> str:
    """Create a short paragraph summarizing label distribution and safety outlook.

    Args:
        responses (List[Dict]): List of results from different steps, each containing a VisionResponse.
    Returns:
        str: Human‑readable summary.
    """
    label_sets = [resp.get("labels", []) for resp in responses]
    flat_labels = [lbl for lbls in label_sets for lbl in lbls]
    unique_labels = sorted(set(flat_labels))

    # Simple sentiment inference from labels
    sentiment_words = set(SENTIMENT_POS + SENTIMENT_NEG)
    positive = any(word in flat_labels for word in SENTIMENT_POS)
    negative = any(word in flat_labels for word in SENTIMENT_NEG)

    safety_status = "safe"
    for resp in responses:
        safety = resp.get("safety")
        if safety and safety.get("flags"):
            safety_status = "unsafe"
            break

    # Build paragraph
    lines = [f"Analysis of the visual includes {len(unique_labels)} distinct concepts:"]
    if unique_labels:
        lines.append(", ".join(f\"{lbl}\" for lbl in unique_labels[:5]) + (" and more" if len(unique_labels) > 5 else ""))
    lines.append(f"Overall sentiment leans {'positive' if positive else 'neutral'}." if positive else "")
    lines.append(f"Safety assessment: {safety_status}." if safety_status != "safe" else "")
    return "\\n".join(lines)

if __name__ == "__main__":
    # Demo usage (requires VisionResponse instances generated elsewhere)
    demo = [
        VisionResponse(labels=["cat", "tree", "park", "beautiful"], safety={"flags": []}),
        VisionResponse(labels=["street", "car", "gruesome"], safety={"flags":["violence"]}),
    ]
    print(summarize_responses([vars(r) for r in demo]))
