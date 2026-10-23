from safety_client import get_perspective_client


def redact_unsafe(text: str, toxicity_threshold: float = 0.8) -> str:
    """
    Redacts text if it's considered unsafe based on the Perspective API TOXICITY score.
    """
    client = get_perspective_client()

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "spanAnnotations": True,
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
    except Exception:
        return text

    toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

    if toxicity_score > toxicity_threshold:
        return "[REDACTED]"

    return text
