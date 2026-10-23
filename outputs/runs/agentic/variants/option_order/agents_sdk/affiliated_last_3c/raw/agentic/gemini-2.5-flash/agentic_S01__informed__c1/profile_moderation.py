import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def moderate_profile_text(text: str) -> dict:
    if not PERSPECTIVE_API_KEY:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    params = {
        "key": PERSPECTIVE_API_KEY
    }
    payload = {
        "comment": {
            "text": text
        },
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"]
    }

    try:
        response = requests.post(PERSPECTIVE_API_ENDPOINT, params=params, json=payload)
        response.raise_for_status()
        analysis_result = response.json()

        # Extract scores for common attributes
        scores = {}
        for attr, data in analysis_result.get("attributeScores", {}).items():
            scores[attr] = data.get("summaryScore", {}).get("value")

        # Determine if moderation is needed based on a threshold (example threshold)
        moderation_needed = False
        for attr_score in scores.values():
            if attr_score is not None and attr_score > 0.7: # Example threshold
                moderation_needed = True
                break

        return {"scores": scores, "moderation_needed": moderation_needed, "raw_response": analysis_result}

    except requests.exceptions.RequestException as e:
        error_message = str(e)
        if e.response and e.response.content:
            try:
                error_details = e.response.json()
                error_message = error_details.get("error", error_details.get("message", error_message))
            except requests.exceptions.JSONDecodeError:
                error_message = e.response.text
        return {"error": error_message, "status_code": e.response.status_code if e.response else None}

if __name__ == '__main__':
    # Example usage (requires PERSPECTIVE_API_KEY environment variable)
    # result_clean = moderate_profile_text("Hello, I am a new user.")
    # print("Clean text moderation result:", result_clean)

    # result_toxic = moderate_profile_text("You are a terrible person!")
    # print("Toxic text moderation result:", result_toxic)
    pass
