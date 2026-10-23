from googleapiclient import discovery

def check_safety(text: str) -> dict:
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey="YOUR_API_KEY"  # Replace with your Perspective API key
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response
