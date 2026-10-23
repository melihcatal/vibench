import os
from googleapiclient import discovery
from identity_models import RegisterUserRequest

# Initialize Google Cloud Perspective API client
client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=os.getenv("PERSPECTIVE_API_KEY"),
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1"
)


def moderate_profile_text(text: str) -> dict:
    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {}
        },
        "languages": ["en"]
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response


def is_profile_safe(request: RegisterUserRequest) -> bool:
    if not request.display_name:
        return True
    
    result = moderate_profile_text(request.display_name)
    toxicity_score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return toxicity_score < 0.7