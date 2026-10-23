from google.cloud import videointelligence_v1 as videointelligence


def script_safety(payload, config=None):
    config = config or {}
    client = videointelligence.VideoIntelligenceServiceClient()
    text = payload.get("text", "")
    unsafe_terms = config.get("unsafe_terms", ["violence", "self-harm", "hate"])
    matches = [term for term in unsafe_terms if term.lower() in text.lower()]
    return {"safe": not matches, "matches": matches}
