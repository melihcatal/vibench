import os
import requests
from messaging_models import SafetyCheckResult, extract_text_from_payload


def check_message_safety(message_id: str, payload: dict) -> SafetyCheckResult:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    text = extract_text_from_payload(payload)
    if not text:
        return SafetyCheckResult(
            message_id=message_id,
            is_safe=True,
        )
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }
    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    data = response.json()
    categories = {}
    confidence_scores = {}
    flagged_content = []
    is_safe = True
    for analysis in data.get("categoriesAnalysis", []):
        category = analysis.get("category", "")
        severity = analysis.get("severity", 0)
        categories[category] = severity
        confidence_scores[category] = severity / 7.0 if severity > 0 else 0.0
        if severity >= 4:
            is_safe = False
            flagged_content.append({"category": category, "severity": severity})
    return SafetyCheckResult(
        message_id=message_id,
        is_safe=is_safe,
        categories=categories,
        confidence_scores=confidence_scores,
        flagged_content=flagged_content,
    )


if __name__ == "__main__":
    result = check_message_safety(
        message_id="evt-001",
        payload={"text": "This is a friendly message with no harmful content."},
    )
    print(result.to_dict())
