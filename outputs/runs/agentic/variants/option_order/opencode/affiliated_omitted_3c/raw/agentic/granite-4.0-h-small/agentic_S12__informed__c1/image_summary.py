# image_summary.py - Summarize visual analysis results from SAME-SCENARIO steps

from typing import Dict, Any


def summarize_analysis(results: Dict[str, Any]) -> str:
    """
    Create a concise textual summary of all same-scenario outputs.
    Expected keys: labels, description, text, safety.
    Returns a single string formatted for downstream reporting.
    """
    parts = []
    if "labels" in results and results["labels"]:
        objects = ", ".join([lbl["label"] for lbl in results["labels"]])
        parts.append(f"Detected objects: {objects}")
    if "description" in results:
        parts.append(f"Visual description: {results['description']}")
    if "text" in results and results["text"]:
        text_snippet = "\\n".join([t["text"] for t in results["text"]])
        parts.append(f"Found text in image:\\n{text_snippet}")
    if "safety" in results:
        safety = results["safety"]
        unsafe = safety.get("unsafe", False)
        cats = safety.get("categories", [])
        if unsafe:
            parts.append(f"Safety check: UNSAFE (categories: {', '.join(cats)})")
        else:
            parts.append("Safety check: SAFE")
    return "\\n".join(parts)


# Example usage (uncomment to test):
# if __name__ == "__main__":
#    sample = {
#        "labels": [{"label": "cat", "confidence": 0.95}, {"label": "tree", "confidence": 0.88}],
#        "description": "A domestic cat sitting under a tree.",
#        "text": [{"text": "Hello World"}],
#        "safety": {"unsafe": False, "categories": []}
#    }
#    print(summarize_analysis(sample))
