from safety_client import get_comprehend_client
from safety_models import normalize_messages


def moderate_batch(payload, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    messages = normalize_messages(payload)
    texts = [message.get("text", "") for message in messages]
    response = client.detect_toxic_content(TextSegments=[{"Text": text} for text in texts], LanguageCode=config.get("language", "en"))
    decisions = []
    for index, result in enumerate(response.get("ResultList", [])):
        decisions.append({
            "index": index,
            "text": texts[index],
            "toxicity": result.get("Toxicity"),
            "decision": "reject" if result.get("Toxicity", 0) >= config.get("threshold", 0.5) else "allow",
        })
    return {"decisions": decisions}
