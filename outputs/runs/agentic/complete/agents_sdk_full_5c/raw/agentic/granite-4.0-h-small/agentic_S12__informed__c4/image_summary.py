import json
from typing import Dict, List

from vision_models import normalize_labels, normalize_description, normalize_text_detection

# -------------------------------------------------------------------
# Aggregation / summarization of the static‑image analysis results
# -------------------------------------------------------------------

def summarize_analysis(label_result: Dict, caption_result: Dict, text_result: List[str], safety_result: bool) -> Dict:
    """Create a concise combined summary for downstream pipelines.

    Parameters:
        label_result   - dict returned by detect_image_labels (list of normalized labels)
        caption_result - dict returned by describe_image (list of captions, usually one)
        text_result    - list of strings from detect_image_text
        safety_result  - bool from score_image_safety

    Returns a JSON‑serializable dict with sections:
        * objects: list of detected objects with confidence
        * caption: short human‑readable description (if any)
        * extracted_text: list of recognized text strings
        * safety: boolean indicating safe / policy‑compliant status
    """
    summary = {
        'objects': label_result,
        'caption': caption_result.get('Captions', [{}])[0].get('Caption', ''),
        'extracted_text': text_result,
        'safety': safety_result
    }
    return summary


def write_summary_to_file(summary: Dict, output_path: str) -> None:
    """Persist the summary as pretty‑printed JSON.",
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
