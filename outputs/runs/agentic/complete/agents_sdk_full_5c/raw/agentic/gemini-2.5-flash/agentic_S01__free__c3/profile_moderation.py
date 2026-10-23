import os
import requests
from identity_models import ProfileModerationRequest, ProfileModerationResponse, ProfileModerationScore

# Perspective API (part of Jigsaw tools, often used with Google Cloud APIs)
# API Host: commentanalyzer.googleapis.com
PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def profile_moderation(request: ProfileModerationRequest) -> ProfileModerationResponse:
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set.")

    headers = {"Content-Type": "application/json"}
    params = {"key": PERSPECTIVE_API_KEY}
    
    # Supported attributes can be found in Perspective API documentation.
    # Common ones include TOXICITY, SEVERE_TOXICITY, IDENTITY_ATTACK, INSULT, PROFANITY, THREAT.
    attributes_to_analyze = {
        "TOXICITY": {},
        "PROFANITY": {},
        "THREAT": {}
    }

    payload = {
        "comment": {"text": request.text},
        "requestedAttributes": attributes_to_analyze,
        "languages": ["en"] # Specify languages if known, or omit for auto-detection
    }

    try:
        response = requests.post(PERSPECTIVE_API_ENDPOINT, headers=headers, params=params, json=payload)
        response.raise_for_status()
        data = response.json()

        is_flagged = False
        scores = []
        for attr, result in data.get("attributeScores", {}).items():
            score_value = result.get("summaryScore", {}).get("value", 0.0)
            scores.append(ProfileModerationScore(attribute=attr, score=score_value))
            # Example threshold: flag if any score is above 0.7
            if score_value > 0.7:
                is_flagged = True
        
        return ProfileModerationResponse(is_flagged=is_flagged, scores=scores)

    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get("error", {}).get("message", "Unknown error")
        raise RuntimeError(f"Perspective API error: {error_message}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to moderate profile text: {e}")

if __name__ == '__main__':
    # This block is for demonstration/testing only
    # os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"
    # try:
    #     moderation_req_clean = ProfileModerationRequest(text="Hello, this is a clean profile description.")
    #     moderation_res_clean = profile_moderation(moderation_req_clean)
    #     print(f"Clean text moderation: Flagged={moderation_res_clean.is_flagged}, Scores={[f'{s.attribute}:{s.score:.2f}' for s in moderation_res_clean.scores]}")

    #     moderation_req_toxic = ProfileModerationRequest(text="I will hurt you for sure!")
    #     moderation_res_toxic = profile_moderation(moderation_req_toxic)
    #     print(f"Toxic text moderation: Flagged={moderation_res_toxic.is_flagged}, Scores={[f'{s.attribute}:{s.score:.2f}' for s in moderation_res_toxic.scores]}")

    # except RuntimeError as e:
    #     print(f"Moderation error: {e}")
    pass
