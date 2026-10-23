import os
import requests
import json


def moderate_vendor_text_safety(text: str) -> dict:
    """
    Moderates vendor notes or memo fields using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        print("Perspective API key not configured.")
        return {"moderation_status": "skipped", "scores": {}}

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
        "SEXUALLY_EXPLICIT": {},
        "FLIRTATION": {},
    }

    data = {
        "comment": {"text": text},
        "languages": ["en"],  # Assuming English for this example
        "requestedAttributes": requested_attributes,
    }

    try:
        response = requests.post(url, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        analysis_result = response.json()

        scores = {
            attr: analysis_result["attributeScores"][attr]["summaryScore"]["value"]
            for attr in requested_attributes
            if attr in analysis_result["attributeScores"]
        }

        # Determine overall safety status (e.g., if any score exceeds a threshold)
        moderation_status = "safe"
        for attr, score in scores.items():
            if score > 0.7:  # Example threshold
                moderation_status = "flagged"
                break

        return {"moderation_status": moderation_status, "scores": scores}

    except requests.exceptions.RequestException as e:
        print(f"Perspective API request failed: {e}")
        return {"moderation_status": "error", "scores": {}, "error": str(e)}


if __name__ == "__main__":
    # Example usage - replace with actual text
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")

    if not perspective_api_key:
        print("Please set PERSPECTIVE_API_KEY environment variable.")
    else:
        vendor_note_safe = (
            "Thanks for your business! We appreciate your prompt payment."
        )
        vendor_note_unsafe = (
            "This is a really bad product and your service is terrible!"
        )

        print(f"Moderating safe vendor note using Perspective API...")
        # result_safe = moderate_vendor_text_safety(vendor_note_safe)
        # print(f"Safe Note Moderation: {json.dumps(result_safe, indent=2)}")

        print(f"\nModerating potentially unsafe vendor note using Perspective API...")
        # result_unsafe = moderate_vendor_text_safety(vendor_note_unsafe)
        # print(f"Unsafe Note Moderation: {json.dumps(result_unsafe, indent=2)}")
