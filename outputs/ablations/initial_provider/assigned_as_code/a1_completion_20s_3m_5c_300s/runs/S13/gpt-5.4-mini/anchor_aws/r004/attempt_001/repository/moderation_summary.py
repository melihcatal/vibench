from safety_client import create_comprehend_client


def moderation_summary(payload, config=None):
    client = create_comprehend_client(config)
    text = (payload or {}).get("text", "")
    response = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode="en")
    labels = []
    for item in response.get("ResultList", []):
        labels.extend([label.get("Name", "unknown") for label in item.get("Labels", [])])
    return {"summary": ", ".join(sorted(set(labels))), "provider": "aws-comprehend"}
