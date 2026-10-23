from googleapiclient import discovery
import os

def check_safety(text: str) -> dict:
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
        'languages': ['en']
    }

    response = client.comments().analyze(body=analyze_request).execute()
    
    # The response structure can be complex, simplifying for this example
    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    return {"toxicity_score": toxicity_score, "is_unsafe": toxicity_score > 0.7}
