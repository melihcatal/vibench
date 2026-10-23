from googleapiclient import discovery
from speech_models import SafetyCheckResult
import os

def check_safety(text: str) -> SafetyCheckResult:
    """Checks text for unsafe content using Google's Perspective API."""
    # Ensure PERSPECTIVE_API_KEY environment variable is set
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en'] # Specify language for analysis
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    
    # Define a threshold for what is considered unsafe. This is an example threshold.
    is_safe = toxicity_score < 0.7 # Example threshold: score above 0.7 is considered unsafe

    return SafetyCheckResult(safe=is_safe, scores={'TOXICITY': toxicity_score})
