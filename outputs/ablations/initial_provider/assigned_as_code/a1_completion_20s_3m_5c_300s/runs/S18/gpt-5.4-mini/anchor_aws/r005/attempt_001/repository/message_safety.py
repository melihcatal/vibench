import boto3


def message_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("text") or payload.get("message") or ""
    moderation = client.detect_key_phrases(Text=text, LanguageCode=config.get("language_code", "en"))
    phrases = [item.get("Text", "") for item in moderation.get("KeyPhrases", [])]
    unsafe = any(term.lower() in text.lower() for term in (config.get("blocked_terms") or ["fraud", "abuse", "violence"]))
    return {"unsafe": unsafe, "signals": phrases}
