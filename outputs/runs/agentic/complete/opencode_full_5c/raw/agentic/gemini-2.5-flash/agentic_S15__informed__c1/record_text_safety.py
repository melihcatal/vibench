import requests
import os


def check_text_safety(text_content: str):
    # Ensure PERSPECTIVE_API_KEY environment variable is set
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # Perspective API expects a specific request format
    request_body = {
        "comment": {"text": text_content},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = requests.post(url, json=request_body)
    response.raise_for_status()  # Raise an exception for HTTP errors

    result = response.json()

    # Extract toxicity score
    toxicity_score = (
        result.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value")
    )

    return {
        "status": "success",
        "toxicity_score": toxicity_score,
        "raw_response": result,
    }
