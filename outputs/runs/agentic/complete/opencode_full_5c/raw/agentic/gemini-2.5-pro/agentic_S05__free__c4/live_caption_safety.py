from googleapiclient import discovery
from speech_client import get_perspective_client_config
from speech_models import ContentSafetyResponse


def check_caption_safety(text: str) -> ContentSafetyResponse:
    """
    Checks live transcript text for unsafe content using the Perspective API.

    Args:
        text: The transcript text to analyze.

    Returns:
        A ContentSafetyResponse object with the toxicity score.
    """
    config = get_perspective_client_config()
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        discoveryServiceUrl=config["discoveryServiceUrl"],
        developerKey=config["developerKey"],
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

    return ContentSafetyResponse(toxicity_score=toxicity_score)


if __name__ == "__main__":
    safe_text = "This is a perfectly normal and safe meeting transcript."
    unsafe_text = "I am going to say something really rude and offensive now."

    safe_result = check_caption_safety(safe_text)
    print(f"'{safe_text}' -> Toxicity: {safe_result.toxicity_score:.4f}")

    unsafe_result = check_caption_safety(unsafe_text)
    print(f"'{unsafe_text}' -> Toxicity: {unsafe_result.toxicity_score:.4f}")
