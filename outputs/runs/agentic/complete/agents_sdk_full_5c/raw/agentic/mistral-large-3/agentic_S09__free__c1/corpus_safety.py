import os
from typing import List
from googleapiclient import discovery
from google.api_core.client_options import ClientOptions

def check_corpus_safety(texts: List[str]) -> List[Dict]:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    client_options = ClientOptions(api_key=api_key)
    service = discovery.build(
        "commentanalyzer", 
        "v1alpha1", 
        client_options=client_options,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1"
    )
    
    results = []
    for text in texts:
        analyze_request = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}}
        }
        response = service.comments().analyze(body=analyze_request).execute()
        results.append({
            "text": text,
            "toxicity_score": response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        })
    
    return results