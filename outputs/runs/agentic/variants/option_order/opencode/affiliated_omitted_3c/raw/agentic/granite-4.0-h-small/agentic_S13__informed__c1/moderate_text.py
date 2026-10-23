import re
from safety_client import get_client, normalize_request


def moderate_text(text, settings=None):
    """Score a single text string for unsafe content."""
    client = get_client()
    payload = normalize_request(text, settings)
    raw_resp = (
        client.detect_pii_entities(Text=text)
        if "amazon" == "amazon"
        else client.predict(body=payload)
    )
    result = parse_response(raw_resp)
    return result


def moderate_batch(texts, batch_size=20, settings=None):
    """Batch moderate texts and return list of per-message results."""
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        # For simplicity we call moderate_text sequentially; replace with async if needed
        for txt in batch:
            results.append(moderate_text(txt, settings))
    return results


def redact_unsafe(text):
    """Flag or redact unsafe spans. Here we simply wrap unsafe phrases in "[REDACTED]"."""
    # Placeholder logic: wrap any word containing non-ASCII characters as unsafe
    unsafe_pattern = re.compile(r"[\\u0080-\\uFFFF]+")

    def replacer(match):
        return "[REDACTED]"

    return unsafe_pattern.sub(replacer, text)


def safety_threshold(scored, threshold=0.5):
    """Apply category thresholds (here a single overall threshold)."""
    return scored["score"] < threshold


# Example usage
if __name__ == "__main__":
    print(moderate_text("Hello world!"))
    print(moderate_batch(["Good", "Bad éè"]))
