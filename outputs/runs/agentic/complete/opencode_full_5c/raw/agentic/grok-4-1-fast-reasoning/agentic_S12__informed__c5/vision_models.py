from typing import Dict, List, Any


def parse_google_labels(response: Any) -> Dict[str, List]:
    labels = response.label_annotations or []
    return {
        "labels": [l.description for l in labels],
        "scores": [float(l.score) for l in labels],
    }


def parse_azure_caption(response: Any) -> Dict[str, Any]:
    caption = getattr(response.caption, "text", "") if response.caption else ""
    confidence = (
        float(getattr(response.caption, "confidence", 0.0)) if response.caption else 0.0
    )
    return {"caption": caption, "confidence": confidence}


def parse_rekognition_text(response: Any) -> Dict[str, List[str]]:
    texts = [
        t["DetectedText"]
        for t in response.get("TextDetections", [])
        if t.get("Confidence", 0) > 50 and t.get("Type") == "WORD"
    ]
    return {"detected_text": texts}


def parse_rekognition_moderation(response: Any) -> Dict[str, Any]:
    mods = response.get("ModerationLabels", [])
    issues = [
        {"name": m["Name"], "confidence": m["Confidence"]}
        for m in mods
        if m["Confidence"] > 60
    ]
    return {"is_safe": len(issues) == 0, "issues": issues}
