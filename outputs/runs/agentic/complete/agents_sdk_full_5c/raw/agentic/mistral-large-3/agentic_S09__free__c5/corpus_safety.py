import os
from typing import List
from googleapiclient import discovery

def check_corpus_safety(texts: List[str]) -> List[Dict]:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    client = discovery.build(
        "commentanalyzer", 
        "v1alpha1", 
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )
    
    results = []
    for text in texts:
        analyze_request = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}},
        }
        response = client.comments().analyze(body=analyze_request).execute()
        results.append({
            "text": text,
            "toxicity_score": response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        })
    
    return results