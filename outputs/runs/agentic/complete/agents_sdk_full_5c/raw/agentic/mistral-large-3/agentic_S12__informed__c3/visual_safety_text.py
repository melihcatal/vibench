from googleapiclient import discovery
from googleapiclient.errors import HttpError
import os

def check_visual_labels_for_unsafe_text(labels: List[str]) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    client = discovery.build(
        "commentanalyzer", 
        "v1alpha1", 
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False
    )
    
    results = {}
    for label in labels:
        analyze_request = {
            "comment": {"text": label},
            "requestedAttributes": {"TOXICITY": {}}
        }
        try:
            response = client.comments().analyze(body=analyze_request).execute()
            results[label] = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        except HttpError as e:
            results[label] = f"Error: {e}"
    
    return results