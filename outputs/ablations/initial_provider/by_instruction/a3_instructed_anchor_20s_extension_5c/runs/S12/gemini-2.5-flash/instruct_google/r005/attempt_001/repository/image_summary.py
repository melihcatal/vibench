from typing import Dict, Any, List

def summarize_visual_analysis(labels: List[Dict[str, Any]], description: str, text_detected: str, safety_scores: Dict[str, Any]) -> Dict[str, Any]:
    summary = {
        "detected_labels": [label["description"] for label in labels],
        "image_description": description,
        "extracted_text": text_detected,
        "safety_analysis": safety_scores,
        "overall_safety_concern": False
    }

    # Simple logic to determine overall safety concern
    unsafe_categories = ["adult", "violence", "racy"]
    for category in unsafe_categories:
        if safety_scores.get(category) in ["POSSIBLE", "LIKELY", "VERY_LIKELY"]:
            summary["overall_safety_concern"] = True
            break

    return summary
