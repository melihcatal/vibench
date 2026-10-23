import json
from typing import List, Dict, Any

from vision_client import VisionClient
from vision_models import VisionModels


def image_summary(
    detection_results: List[List[Dict[str, Any]]],
    description: str,
    ocr_results: List[Dict[str, str]],
    safety_results: List[List[Dict[str, Any]]],
) -> str:
    """Summarize visual analysis results into a concise human‑readable report.\n    \n    Args:\n        detection_results (List[List[Dict]]): Labels from same‑scenario files (list per provider).\n        description (str): Short visual description from `describe_image`.\n        ocr_results (List[Dict]): Text blocks from `detect_image_text`.\n        safety_results (List[List[Dict]]): Safety annotations from `score_image_safety`.\n    \n    Returns:\n        str: Markdown‑formatted summary.\n"""
    # Flatten all label sets (union of providers)\n    all_labels = []
    for provider_labels in detection_results:
        all_labels.extend(provider_labels)
    # Deduplicate by label name (keep highest confidence)\n    unique = {}
    for lbl in all_labels:
        key = lbl["label"].lower()
        if key not in unique or float(lbl["confidence"]) > float(
            unique[key]["confidence"]
        ):
            unique[key] = lbl
    label_report = "\n**Detected objects/labels:**\n"
    if unique:
        for lbl in unique.values():
            label_report += f"- `{lbl['label']} (confidence {lbl['confidence']})`\n"
    else:
        label_report += "- *No objects detected.*\n"

    # OCR block\n    ocr_report = "\n**Extracted text:**\n"
    if ocr_results:
        for txt in ocr_results:
            ocr_report += f"- `{txt['text']}`\n"
    else:
        ocr_report += "- *No text detected.*\n"

    # Safety report\n    safety_report = "\n**Safety check:**\n"
    unsafe_found = False
    for provider_annotations in safety_results:
        for anno in provider_annotations:
            cat = anno["category"]
            conf = anno["confidence"]
            unsafe_found = True
            safety_report += f"- *{cat}: {conf}*\n"
    if not unsafe_found:
        safety_report += "- *No unsafe content detected.*\n"

    # Assemble markdown\n    markdown = f"# Image Analysis Summary\n\n## Visual Description\n{description}\n{label_report}{ocr_report}{safety_report}\n"
    return markdown[:1000]  # truncate to keep reasonable length
