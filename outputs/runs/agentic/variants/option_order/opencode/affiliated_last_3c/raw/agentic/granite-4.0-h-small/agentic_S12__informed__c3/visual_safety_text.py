import json
from typing import List, Dict, Any

from vision_client import VisionClient
from vision_models import VisionModels


def visual_safety_text(label_list: List[Dict[str, Any]],
                       safety_annotations: List[List[Dict[str, Any]]]) -> str:
    """Check generated visual labels for unsafe text and return a safety report.\n    \n    Args:\n        label_list (List[Dict[str, Any]]): List of label dicts (each has 'label' and 'confidence').\n        safety_annotations (List[List[Dict[str, Any]]]): List of safety annotation groups\n            per provider.\n    \n    Returns:\n        str: Markdown block describing unsafe detections.\n    """
    unsafe_categories = []
    # Consolidate safety annotations from any provider\n    for provider_annos in safety_annotations:
        for anno in provider_annos:
            cat = anno.get("category")
            conf = anno.get("confidence", "N/A")
            unsafe_categories.append(f"{cat}: {conf}")\n
    if not unsafe_categories:
        return "- *No unsafe visual labels detected.*"

    # Simple formatting\n    lines = ["- *Unsafe categories detected:*"]
    lines.extend(unsafe_categories)
    return "\\n".join(lines)
