from __future__ import annotations

from typing import Any, Dict, List, Optional

import openai

from vision_client import OPENAI_API_BASE, VISION_MODEL_ID, get_openai_client
from vision_models import (
    LabelResponse,
    TextDetectionResponse,
    label_response_to_dict,
    text_detection_response_to_dict,
)

TEXT_SAFETY_PROMPT = """Analyze the following extracted text and detected labels from an image for potentially unsafe,
offensive, or policy-sensitive content. Evaluate for:
- Hate speech or slurs
- Threats or violent language
- Sexually explicit terms
- Illegal activity references
- Harassment or bullying language
- Self-harm references

Return a JSON object with:
- "safe": boolean indicating if all text is safe for general audiences
- "flags": array of flagged items, each with:
  - "text": the problematic text
  - "category": the violation category
  - "severity": "low", "medium", or "high"
- "summary": brief explanation of findings

Example: {"safe": false, "flags": [{"text": "offensive word", "category": "hate_speech", "severity": "high"}], "summary": "Contains hate speech."}"""


def check_visual_safety_text(
    labels: Optional[LabelResponse] = None,
    text_detection: Optional[TextDetectionResponse] = None,
    api_key: Optional[str] = None,
    model: str = VISION_MODEL_ID,
) -> Dict[str, Any]:
    label_names = [
        l["name"]
        for l in label_response_to_dict(labels or LabelResponse(labels=[]))["labels"]
    ]
    detected_text = text_detection.full_text if text_detection else ""
    combined_input = f"Labels: {', '.join(label_names)}\nDetected text: {detected_text}"

    client = get_openai_client(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a content safety analyzer for text extracted from images.",
            },
            {
                "role": "user",
                "content": f"{TEXT_SAFETY_PROMPT}\n\nInput:\n{combined_input}",
            },
        ],
        max_tokens=512,
        temperature=0.0,
        response_format={"type": "json_object"},
    )
    import json

    result = json.loads(response.choices[0].message.content.strip())
    return result


def is_text_safe(
    labels: Optional[LabelResponse] = None,
    text_detection: Optional[TextDetectionResponse] = None,
    api_key: Optional[str] = None,
    model: str = VISION_MODEL_ID,
) -> bool:
    result = check_visual_safety_text(labels, text_detection, api_key, model)
    return result.get("safe", True)


def get_text_safety_flags(
    labels: Optional[LabelResponse] = None,
    text_detection: Optional[TextDetectionResponse] = None,
    api_key: Optional[str] = None,
    model: str = VISION_MODEL_ID,
) -> List[Dict[str, str]]:
    result = check_visual_safety_text(labels, text_detection, api_key, model)
    return result.get("flags", [])


if __name__ == "__main__":
    from vision_models import TextDetectionResponse, TextRegion

    text_resp = TextDetectionResponse(
        regions=[TextRegion(text="Hello world", confidence=0.99)],
        full_text="Hello world",
    )
    result = check_visual_safety_text(text_detection=text_resp)
    print(result)
