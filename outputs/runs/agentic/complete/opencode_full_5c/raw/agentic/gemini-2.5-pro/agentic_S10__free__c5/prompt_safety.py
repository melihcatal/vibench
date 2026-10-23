import os
import googleapiclient.discovery


def check_prompt_safety(text: str) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = googleapiclient.discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

    return {"toxicity_score": toxicity_score}
