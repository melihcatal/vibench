import os
import requests


def moderate_profile_text(text: str) -> dict:
    """
    Moderates profile text before account activation using Perspective API.
    """
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Perspective API endpoint
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key}"

    payload = {
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
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Perspective API moderation failed: {e}")


if __name__ == "__main__":
    # Example usage (replace with actual values or environment variables)
    os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"

    profile_description = (
        "I love puppies and rainbows! But sometimes I get really angry at bad drivers."
    )

    try:
        moderation_result = moderate_profile_text(profile_description)
        print("Moderation Result:")
        for attribute, data in moderation_result.get("attributeScores", {}).items():
            print(f"- {attribute}: {data['summaryScore']['value']}")
    except RuntimeError as e:
        print(f"Error: {e}")
