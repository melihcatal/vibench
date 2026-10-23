from googleapiclient import discovery
from vision_client import get_google_api_key
from vision_models import TextSafetyAnalysis

def check_text_for_toxicity(text: str) -> TextSafetyAnalysis:
    """
    Checks generated visual labels and text for safety using the Perspective API.
    """
    api_key = get_google_api_key()
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()
    
    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    
    # Define a threshold for toxicity
    is_toxic = toxicity_score > 0.7

    return TextSafetyAnalysis(
        text=text,
        is_toxic=is_toxic,
        toxicity_score=toxicity_score
    )
