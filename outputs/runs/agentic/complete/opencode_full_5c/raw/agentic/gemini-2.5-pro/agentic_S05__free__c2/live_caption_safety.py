import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError


def check_caption_for_safety(text: str):
    """Checks live transcript text for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"][
            "value"
        ]
        return {"toxicity_score": toxicity_score}
    except HttpError as e:
        # Production applications should handle this error more gracefully
        print(f"Perspective API error: {e}")
        return None
