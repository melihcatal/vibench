import os
import requests
import json

# Perspective API integration
# Provider-identifying signal: PERSPECTIVE_API_KEY and specific API endpoint

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def moderate_claims(text: str, languages: list[str] | None = None) -> dict:
    """Moderates free-text claims or notes using Google Perspective API."""
    if not PERSPECTIVE_API_KEY:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    if not text:
        return {"score": 0.0, "summary": "No text to moderate."}

    params = {"key": PERSPECTIVE_API_KEY}
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "FLIRTATION": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
        },
        "languages": languages if languages else ["en"],
    }

    try:
        response = requests.post(
            PERSPECTIVE_API_ENDPOINT,
            params=params,
            headers=headers,
            data=json.dumps(data),
        )
        response.raise_for_status()
        result = response.json()

        # Extract relevant scores (example)
        toxicity_score = (
            result.get("attributeScores", {})
            .get("TOXICITY", {})
            .get("summaryScore", {})
            .get("value", 0.0)
        )
        flirtation_score = (
            result.get("attributeScores", {})
            .get("FLIRTATION", {})
            .get("summaryScore", {})
            .get("value", 0.0)
        )
        threat_score = (
            result.get("attributeScores", {})
            .get("THREAT", {})
            .get("summaryScore", {})
            .get("value", 0.0)
        )
        sexually_explicit_score = (
            result.get("attributeScores", {})
            .get("SEXUALLY_EXPLICIT", {})
            .get("summaryScore", {})
            .get("value", 0.0)
        )

        moderation_summary = {
            "toxicity": toxicity_score,
            "flirtation": flirtation_score,
            "threat": threat_score,
            "sexually_explicit": sexually_explicit_score,
            "full_response": result,
        }
        return moderation_summary

    except requests.exceptions.RequestException as e:
        return {"error": f"Perspective API request failed: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}


if __name__ == "__main__":
    # Example usage
    claim_text_good = "This is a perfectly normal and pleasant comment."
    claim_text_bad = "You are an idiot and I hate you!"
    claim_text_flirt = "Hey there, good looking! Want to chat?"

    print("\nModerating good text:")
    print(moderate_claims(claim_text_good))

    print("\nModerating bad text:")
    print(moderate_claims(claim_text_bad))

    print("\nModerating flirtatious text:")
    print(moderate_claims(claim_text_flirt))
