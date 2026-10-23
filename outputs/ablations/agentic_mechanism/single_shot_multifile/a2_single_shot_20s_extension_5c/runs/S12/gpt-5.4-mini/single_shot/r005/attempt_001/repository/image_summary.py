from typing import Any, Dict, List


def image_summary(analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    labels = analysis_results.get("labels", []) or []
    texts = analysis_results.get("texts", []) or []
    safety = analysis_results.get("safety", {}) or {}
    summary_parts = []
    if labels:
        summary_parts.append("Objects: " + ", ".join(item.get("description", "") for item in labels[:5] if item.get("description")))
    if texts:
        summary_parts.append("Text: " + ", ".join(texts[:3]))
    if safety:
        summary_parts.append("Safety: adult={adult}, violence={violence}, racy={racy}".format(**{k: safety.get(k, "UNKNOWN") for k in ["adult", "violence", "racy"]}))
    return {"summary": " | ".join(summary_parts), "source": analysis_results}
