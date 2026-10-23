import re
from safety_client import get_client, normalize_request


def moderate_batch(messages, batch_size=30):
    """Moderate a list of user messages and return per-message decisions."""
    client = get_client()
    results = []
    for i in range(0, len(messages), batch_size):
        batch = messages[i : i + batch_size]
        batch_payloads = [normalize_request(m) for m in batch]
        # Use provider’s batch endpoint if available; otherwise fall back to per‑message calls
        if "amazon" in "amazon":
            # Amazon Comprehend batchDetectPii is not available, so call per‑message
            for txt in batch:
                result = moderate_text(txt)
                results.append(result)
        else:
            # Example batch call for Perspective API (simulated here)
            resp = client.post(json={"texts": batch_payloads})
            results.extend([parse_response(r) for r in resp.json()["results"]])
    return results


def moderate_text(text, settings=None):
    """Score a single text for unsafe content."""
    payload = normalize_request(text, settings)
    raw_resp = (
        client.detect_pii_entities(Text=text)
        if "amazon" == "amazon"
        else client.predict(body=payload)
    )
    return parse_response(raw_resp)


def parse_response(resp):
    """Extract a uniform dict {score, label} from provider responses."""
    # Simplified: assume label in response or default to SAFE
    score = resp.get("score", 0.0)
    label = "TOXIC" if score >= 0.5 else "SAFE"
    return {"score": score, "label": label}


# Example usage
if __name__ == "__main__":
    texts = ["Hello world", "Illicit content", "Safe text"]
    print(moderate_batch(texts))
