# vision_models.py - Local request/response and normalization helpers for Static Image and Visual Understanding

from typing import Any, Dict, List, Optional

# ------------------------------------------------------------------
# Normalization helpers for SAME-SCENARIO response shapes
# ------------------------------------------------------------------

def normalize_labels_response(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convert provider-specific label detection response to a uniform shape:
    [
        {"label": "string", "confidence": float, "region": {"x1": float, "y1": float, "x2": float, "y2": float}},
        ...
    ]
    """
    # Example for Alibaba detection response (adjust if other provider used)
    # raw is expected to contain a top-level key `items` with list of detected objects
    # Each item has `label`, `confidence`, and `region` fields (names may vary)
    items = raw.get("items", [])
    normalized = []
    for it in items:
        normalized.append({
            "label": it.get("label", ""),
            "confidence": float(it.get("confidence", 0)),
            "region": {
                "x1": float(it.get("x", 0)),
                "y1": float(it.get("y", 0)),
                "x2": float(it.get("x2", 0)),
                "y2": float(it.get("y2", 0)),
            },
        })
    return normalized


def normalize_description_response(raw: Dict[str, Any]) -> Dict[str, str]:
    """
    Return a simple dict with a single key "description" containing the generated caption.
    Handles the shape produced by Qwen-VL via DashScope.
    """
    # Raw may look like {"caption": "..."} or {"result": {"text": "..."}} depending on provider
    if raw.get("caption"):
        return {"description": raw["caption"]}
    if raw.get("result") and raw["result"].get("text"):
        return {"description": raw["result"]["text"]}
    # Fallback - concatenate possible text fields
    texts = [str(raw.get(k, "")) for k in ("caption", "text", "description")]
    return {"description": " ".join(filter(None, texts))}


def normalize_text_detection_response(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Normalize OCR text detection output to:
    [
        {
            "text": "string",
            "region": {"x1": float, "y1": float, "x2": float, "y2": float}
        },
        ...
    ]
    """
    # Example for Alibaba OCR response (adjust if other provider used)
    items = raw.get("items", [])
    normalized = []
    for it in items:
        region = it.get("box", [])  # expecting [x1, y1, x2, y2]
        normalized.append({
            "text": it.get("content", ""),
            "region": {
                "x1": float(region[0]) if len(region) > 0 else 0.0,
                "y1": float(region[1]) if len(region) > 1 else 0.0,
                "x2": float(region[2]) if len(region) > 2 else 0.0,
                "y2": float(region[3]) if len(region) > 3 else 0.0,
            },
        })
    return normalized


def normalize_safety_score(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Produce a uniform safety result:
    {
        "unsafe": bool,
        "categories": List[str],   # list of detected unsafe categories
        "scores": Optional[Dict[str, float]]  # optional confidence scores per category
    }
    """
    # Amazon Rekognition moderation response example
    unsafe = False
    categories = []
    scores = {}
    # Assume raw contains 'ModerationLabels' with [{"Name": ..., "Confidence": ..., "ParentName": ...}, ...]
    labels = raw.get("ModerationLabels", [])
    for lbl in labels:
        name = lbl.get("Name")
        confidence = float(lbl.get("Confidence", 0))
        if name and confidence > 0:
            categories.append(name)
            scores[name] = confidence
    if categories:
        unsafe = True
    return {"unsafe": unsafe, "categories": categories, "scores": scores if scores else None}

# ------------------------------------------------------------------
# Helper utilities for later-step files
# ------------------------------------------------------------------

def summarize_analysis(same_scenario_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simple aggregation of same-scenario results into a summary dict.
    Expected keys: labels, description, text, safety.
    Returns a flattened summary.
    """
    summary = {}
    if "labels" in same_scenario_results:
        summary["labels_summary"] = f"{len(same_scenario_results['labels'])} objects detected"
    if "description" in same_scenario_results:
        summary["image_description"] = same_scenario_results["description"]
    if "text" in same_scenario_results:
        summary["extracted_text"] = "\\n".join([t["text"] for t in same_scenario_results["text"]])
    if "safety" in same_scenario_results:
        unsafe = same_scenario_results["safety"].get("unsafe", False)
        summary["safety":]: = {
            "unsafe": unsafe,
            "categories": same_scenario_results["safety"].get("categories", [])
        }
    return summary

# End of vision_models.py