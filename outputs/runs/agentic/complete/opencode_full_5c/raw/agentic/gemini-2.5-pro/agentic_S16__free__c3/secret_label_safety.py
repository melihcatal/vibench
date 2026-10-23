from security_client import get_perspective_client
from security_models import UnsafeTextAnalysis


def check_text_for_unsafe_content(text: str) -> UnsafeTextAnalysis:
    """
    Checks secret labels and notes for unsafe text using the Perspective API.
    """
    client = get_perspective_client()

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        "languages": ["en"],
    }

    response = client.comments().analyze(body=analyze_request).execute()

    is_unsafe = False
    reasons = []

    for attr, value in response["attributeScores"].items():
        if value["summaryScore"]["value"] > 0.7:
            is_unsafe = True
            reasons.append(f"{attr}: {value['summaryScore']['value']:.2f}")

    return UnsafeTextAnalysis(is_unsafe=is_unsafe, reasons=reasons)


if __name__ == "__main__":
    safe_text = "This is a standard API key for our internal service."
    analysis_safe = check_text_for_unsafe_content(safe_text)
    print(
        f"Analysis for safe text: Is unsafe? {analysis_safe.is_unsafe}, Reasons: {analysis_safe.reasons}"
    )

    unsafe_text = "this is some hateful and stupid text"
    analysis_unsafe = check_text_for_unsafe_content(unsafe_text)
    print(
        f"Analysis for unsafe text: Is unsafe? {analysis_unsafe.is_unsafe}, Reasons: {analysis_unsafe.reasons}"
    )
