from googleapiclient import discovery
import os
from typing import Dict, Any

def check_output_safety(text: str) -> Dict[str, Any]:
    client = discovery.build(
        "commentanalyzer", 
        "v1alpha1", 
        developerKey=os.getenv("GOOGLE_PERSPECTIVE_API_KEY"),
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False
    )
    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}}
    }
    response = client.comments().analyze(body=analyze_request).execute()
    return response