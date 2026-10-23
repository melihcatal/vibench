from identity_client import get_comprehend_client

def onboarding_summary(payload, config=None):
    config = config or {}
    client = get_comprehend_client()

    onboarding_notes = payload["onboarding_notes"]

    # Detect key phrases
    key_phrases_response = client.detect_key_phrases(Text=onboarding_notes, LanguageCode='en')
    key_phrases = [kp["Text"] for kp in key_phrases_response['KeyPhrases']]

    # Detect entities
    entities_response = client.detect_entities(Text=onboarding_notes, LanguageCode='en')
    entities = [{ "text": e["Text"], "type": e["Type"] } for e in entities_response['Entities']]

    # A simple summary could be a combination of key phrases and entities
    summary = f"Key points: {\". \".join(key_phrases)}. Entities mentioned: {\". \".join([e['text'] for e in entities])}."

    return {
        "summary": summary,
        "key_phrases": key_phrases,
        "entities": entities,
    }
