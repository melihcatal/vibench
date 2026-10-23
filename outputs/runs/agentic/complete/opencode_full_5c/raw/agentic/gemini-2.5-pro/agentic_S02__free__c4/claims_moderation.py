from googleapiclient import discovery
from identity_client import get_identity_config


def moderate_text_claim(text: str) -> dict:
    config = get_identity_config()
    api_key = config.GOOGLE_API_KEY

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        return response
    except Exception as e:
        print(f"Error calling Perspective API: {e}")
        return {}


if __name__ == "__main__":
    # This is for verification, not example usage.
    # In a real app, this would be used to moderate user-provided profile fields.
    sample_text = "This is a test claim."
    moderation_result = moderate_text_claim(sample_text)

    if moderation_result:
        toxicity_score = (
            moderation_result.get("attributeScores", {})
            .get("TOXICITY", {})
            .get("summaryScore", {})
            .get("value")
        )
        print(f"Moderation result for '{sample_text}':")
        if toxicity_score is not None:
            print(f"  Toxicity score: {toxicity_score:.4f}")
        else:
            print("Could not retrieve toxicity score.")
    else:
        print("Failed to get moderation result.")
