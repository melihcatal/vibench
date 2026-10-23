import json

def image_summary(vision_results: dict) -> str:
    """Summarize the outputs from various visual analysis steps into a concise paragraph.
    Expects a dict with keys: labels, description, detected_text, safety.
    """
    labels = vision_results.get('labels', [])
    description = vision_results.get('description', '')
    text_lines = vision_results.get('detected_text', [])
    safe = vision_results.get('safe', True)

    parts = []
    if labels:
        parts.append(f"Objects detected: {', '.join(labels)}.")
    if description:
        parts.append(f"Image description: {description}.")
    if text_lines:
        parts.append(f"Text found in image: {', '.join(text_lines[:5])}{' ...' if len(text_lines) > 5 else ''}.")
    if safe is False:
        parts.append("Safety check: Unsafe content detected.")
    else:
        parts.append("Safety check: Content appears safe.")
    return ' '.join(parts)
