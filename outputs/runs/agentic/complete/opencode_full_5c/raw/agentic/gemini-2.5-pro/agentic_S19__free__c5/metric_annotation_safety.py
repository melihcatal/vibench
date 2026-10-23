from typing import List
from observability_client import get_perspective_client
from observability_models import SafetyAnnotation


def check_text_safety(text: str) -> List[SafetyAnnotation]:
    """
    Analyzes a string for various toxicity attributes using the Perspective API.
    """
    client = get_perspective_client()

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()

        annotations = []
        for attr, scores in response["attributeScores"].items():
            annotations.append(
                SafetyAnnotation(attribute=attr, score=scores["summaryScore"]["value"])
            )
        return annotations
    except Exception as e:
        print(f"Error calling Perspective API: {e}")
        return []


if __name__ == "__main__":
    unsafe_text = "You are making a terrible mistake and this code is stupid."
    safe_text = "This metric indicates a slight increase in latency over the last hour."

    print("--- Checking unsafe text ---")
    unsafe_analysis = check_text_safety(unsafe_text)
    for annotation in unsafe_analysis:
        print(f"{annotation.attribute}: {annotation.score:.4f}")

    print("\n--- Checking safe text ---")
    safe_analysis = check_text_safety(safe_text)
    for annotation in safe_analysis:
        print(f"{annotation.attribute}: {annotation.score:.4f}")
