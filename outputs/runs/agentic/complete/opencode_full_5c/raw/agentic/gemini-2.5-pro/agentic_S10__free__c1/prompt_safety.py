import os
from googleapiclient import discovery
from dotenv import load_dotenv

load_dotenv()


def check_prompt_safety(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    attribute_scores = response.get("attributeScores", {})
    toxicity_score = (
        attribute_scores.get("TOXICITY", {}).get("summaryScore", {}).get("value")
    )

    return {"toxicity_score": toxicity_score}
