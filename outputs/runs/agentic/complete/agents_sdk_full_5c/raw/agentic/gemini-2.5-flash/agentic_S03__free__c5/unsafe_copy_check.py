import os
from googleapiclient import discovery
from translation_models import ContentCheckRequest, ContentCheckResponse

def check_unsafe_content(request: ContentCheckRequest) -> ContentCheckResponse:
    # API key for Perspective API is required
    API_KEY = os.getenv("PERSPECTIVE_API_KEY") # Provider-specific environment variable
    if not API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': request.text},
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()

    # Check for TOXICITY score
    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']

    # Define a threshold for what's considered unsafe
    is_unsafe = toxicity_score > 0.7  # Example threshold
    details = f"Toxicity score: {toxicity_score:.2f}"

    return ContentCheckResponse(is_unsafe=is_unsafe, details=details)
