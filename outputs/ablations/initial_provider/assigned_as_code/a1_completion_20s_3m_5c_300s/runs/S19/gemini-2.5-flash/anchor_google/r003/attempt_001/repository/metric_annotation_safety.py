from googleapiclient import discovery

def metric_annotation_safety(payload, config=None):
    config = config or {}
    api_key = config.get("perspective_api_key")

    if not api_key:
        raise ValueError("Perspective API key not provided in config.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    text_to_analyze = payload["annotation_text"]

    analyze_request = {
        'comment': {'text': text_to_analyze},
        'requestedAttributes': {'TOXICITY': {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    
    # A threshold for safety; this can be configured
    is_safe = toxicity_score < config.get("toxicity_threshold", 0.7)

    return {"is_safe": is_safe, "toxicity_score": toxicity_score}
