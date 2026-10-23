import os
from googleapiclient import discovery

def moderate_vendor_notes(text_content: str) -> Dict[str, Any]:
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
        'comment': {'text': text_content},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en'] # Assuming English for now
    }

    response = client.comments().analyze(body=analyze_request).execute()

    # Extracting relevant scores, could be extended for other attributes
    toxicity_score = response.get("attributeScores", {}).get("TOXICITY", {})
    return {"toxicity_score": toxicity_score.get("summaryScore", {}).get("value"), "raw_response": response}
