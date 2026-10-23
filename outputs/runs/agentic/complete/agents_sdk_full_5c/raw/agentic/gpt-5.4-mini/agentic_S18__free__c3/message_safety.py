from messaging_models import normalize_text


# Provider-specific workflow helper for Google Cloud Pub/Sub message payload screening.
def is_safe_payload(text: str) -> bool:
    normalized = normalize_text(text).lower()
    unsafe_tokens = {"password", "credit card", "ssn", "secret key"}
    return not any(token in normalized for token in unsafe_tokens)
