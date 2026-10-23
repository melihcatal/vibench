from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import openai

from vision_models import (
    DescriptionResponse,
    ImageInput,
    ImageSource,
    LabelItem,
    LabelResponse,
    SafetyCategory,
    SafetyResponse,
    SafetyScore,
    TextDetectionResponse,
    TextRegion,
    normalize_label_confidence,
    normalize_safety_score,
)

OPENAI_API_BASE = "https://api.openai.com/v1"
VISION_MODEL_ID = "gpt-4o-2024-08-06"
VISION_MODEL_FAMILY = "gpt-4o"


def get_openai_client(api_key: Optional[str] = None) -> openai.OpenAI:
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return openai.OpenAI(api_key=key, base_url=OPENAI_API_BASE)


def build_vision_message(
    image_input: ImageInput,
    prompt: str,
    detail: str = "auto",
) -> List[Dict[str, Any]]:
    content: List[Dict[str, Any]] = [{"type": "text", "text": prompt}]

    if image_input.source == ImageSource.BASE64:
        data_url = f"data:{image_input.mime_type};base64,{image_input.value}"
        content.append(
            {"type": "image_url", "image_url": {"url": data_url, "detail": detail}}
        )
    elif image_input.source == ImageSource.URL:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": image_input.value, "detail": detail},
            }
        )
    else:
        raise ValueError(f"Unsupported image source: {image_input.source}")

    return content


def call_vision_api(
    client: openai.OpenAI,
    messages: List[Dict[str, Any]],
    model: str = VISION_MODEL_ID,
    max_tokens: int = 1024,
    temperature: float = 0.0,
) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": messages}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()


def call_vision_api_with_json(
    client: openai.OpenAI,
    messages: List[Dict[str, Any]],
    model: str = VISION_MODEL_ID,
    max_tokens: int = 2048,
    temperature: float = 0.0,
) -> Dict[str, Any]:
    import json

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": messages}],
        max_tokens=max_tokens,
        temperature=temperature,
        response_format={"type": "json_object"},
    )
    raw_text = response.choices[0].message.content.strip()
    return json.loads(raw_text)


def parse_labels_from_json(raw: Dict[str, Any], image_id: str = "") -> LabelResponse:
    items = raw.get("labels", raw.get("objects", []))
    labels = []
    for item in items:
        name = item.get("name", item.get("label", item.get("category", "unknown")))
        conf = normalize_label_confidence(
            item.get("confidence", item.get("score", 0.0))
        )
        bbox = item.get("bounding_box", item.get("bbox"))
        labels.append(LabelItem(name=name, confidence=conf, bounding_box=bbox))
    return LabelResponse(labels=labels, image_id=image_id, raw_response=raw)


def parse_description_from_text(text: str, image_id: str = "") -> DescriptionResponse:
    return DescriptionResponse(
        description=text,
        confidence=0.95,
        image_id=image_id,
        raw_response={"text": text},
    )


def parse_text_detection_from_json(
    raw: Dict[str, Any], image_id: str = ""
) -> TextDetectionResponse:
    regions_raw = raw.get("regions", raw.get("text_blocks", []))
    regions = []
    for r in regions_raw:
        regions.append(
            TextRegion(
                text=r.get("text", ""),
                confidence=normalize_label_confidence(
                    r.get("confidence", r.get("score", 0.0))
                ),
                bounding_box=r.get("bounding_box", r.get("bbox")),
                language=r.get("language", "en"),
            )
        )
    full_text = raw.get("full_text", " ".join(r.text for r in regions))
    return TextDetectionResponse(
        regions=regions, full_text=full_text, image_id=image_id, raw_response=raw
    )


def parse_safety_from_json(raw: Dict[str, Any], image_id: str = "") -> SafetyResponse:
    scores_raw = raw.get("scores", raw.get("categories", []))
    scores = []
    flagged_any = False
    for s in scores_raw:
        cat_str = s.get("category", s.get("name", "unknown")).lower()
        try:
            category = SafetyCategory(cat_str)
        except ValueError:
            category = SafetyCategory.ILLEGAL
        score_val = normalize_safety_score(s.get("score", s.get("confidence", 0.0)))
        is_flagged = score_val > 0.6
        if is_flagged:
            flagged_any = True
        scores.append(
            SafetyScore(category=category, score=score_val, flagged=is_flagged)
        )
    return SafetyResponse(
        scores=scores, overall_safe=not flagged_any, image_id=image_id, raw_response=raw
    )
