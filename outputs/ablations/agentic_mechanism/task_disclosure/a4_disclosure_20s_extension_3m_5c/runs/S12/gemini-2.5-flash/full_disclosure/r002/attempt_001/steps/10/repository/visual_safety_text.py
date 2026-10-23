import os
from googleapiclient import discovery

def check_text_safety(labels: list[str]) -> list[dict]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    results = []
    for label in labels:
        analyze_request = {
            "comment": {"text": label},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
        }
        response = client.comments().analyze(body=analyze_request).execute()
        results.append({"label": label, "attributes": response["attributeScores"]})
    return results
