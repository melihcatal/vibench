import os
import googleapiclient.discovery

def check_annotation_safety(text: str, config=None):
    config = config or {}

    # Initialize the Perspective API client
    # API key is typically managed outside, e.g., via environment variables or a config file.
    # For this example, we assume it's available via config.
    # Make sure to enable the Perspective API in your Google Cloud project.
    client = googleapiclient.discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=os.environ.get("PERSPECTIVE_API_KEY", config.get("perspective_api_key"))
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']

    is_unsafe = toxicity_score > config.get("toxicity_threshold", 0.7)

    return {"is_unsafe": is_unsafe, "toxicity_score": toxicity_score}
