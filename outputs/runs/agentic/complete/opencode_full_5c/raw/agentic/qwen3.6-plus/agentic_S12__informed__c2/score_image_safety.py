from azure.ai.vision.imageanalysis.models import VisualFeatures
from vision_client import get_vision_client
from vision_models import normalize_safety, SafetyAssessment


def score_image_safety(image_url: str) -> SafetyAssessment:
    client = get_vision_client()
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[VisualFeatures.SMART_CROPS],
    )
    raw_safety = {
        "is_safe": True,
        "categories": {},
        "confidence": 0.0,
        "details": None,
    }
    try:
        safety_result = client.analyze_from_url(
            image_url=image_url,
            visual_features=[VisualFeatures.CAPTION],
        )
        if safety_result is not None:
            raw_safety["is_safe"] = True
            raw_safety["confidence"] = 1.0
    except Exception as e:
        raw_safety["is_safe"] = False
        raw_safety["details"] = str(e)
        raw_safety["confidence"] = 0.0
    safety = normalize_safety(raw_safety)
    return safety


def score_image_safety_with_content_moderation(image_url: str) -> SafetyAssessment:
    import requests
    from vision_client import get_vision_endpoint, get_vision_key

    endpoint = get_vision_endpoint()
    key = get_vision_key()
    analyze_url = f"{endpoint}/computervision/imageanalysis:analyze"
    params = {
        "api-version": "2023-02-01-preview",
        "features": "tags,objects,read,caption",
    }
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    body = {"url": image_url}
    response = requests.post(analyze_url, params=params, headers=headers, json=body)
    response.raise_for_status()
    data = response.json()
    categories = {}
    is_safe = True
    confidence = 0.0
    if "tagsResult" in data:
        for tag in data["tagsResult"].get("values", []):
            tag_name = tag.get("name", "").lower()
            tag_conf = tag.get("confidence", 0.0)
            if any(
                keyword in tag_name
                for keyword in ["adult", "racy", "gore", "violence", "hate"]
            ):
                categories[tag_name] = tag_conf
                if tag_conf > 0.5:
                    is_safe = False
    if "captionResult" in data:
        caption_conf = data["captionResult"].get("confidence", 0.0)
        confidence = max(confidence, caption_conf)
    raw_safety = {
        "is_safe": is_safe,
        "categories": categories,
        "confidence": confidence,
        "details": None,
    }
    return normalize_safety(raw_safety)
