import requests
from observability_client import get_aws_credentials

# Using Perspective API for content safety (could be replaced with other providers)


def check_metric_annotations_safety(annotations, api_key):
    """Check free-text metric labels or annotations for unsafe text.

    Parameters:
        annotations (list[str]): List of text snippets to evaluate.
        api_key (str): Perspective API key.

    Returns:
        list[dict]: Evaluation results with safety scores per snippet.
    """
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json", "x-api-key": api_key}
    results = []
    for txt in annotations:
        payload = {"comment": {"text": txt}, "requestedAttributes": {"TOXICITY": {}}}
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        results.append({"text": txt, "toxicity_score": float(score)})
    return results
