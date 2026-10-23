import requests
import os


def check_text_safety_perspective_api(text: str) -> dict:
    API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
    if not API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={API_KEY}"

    # Define the attributes to analyze. Perspective API can check for more.
    attributes = [
        "TOXICITY",
        "SEVERE_TOXICITY",
        "IDENTITY_ATTACK",
        "INSULT",
        "PROFANITY",
        "THREAT",
        "SEXUALLY_EXPLICIT",
        "CRUDE",
        "FLIRTATION",
    ]

    request_body = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
    }

    try:
        response = requests.post(url, json=request_body)
        response.raise_for_status()  # Raise an exception for HTTP errors

        analysis_results = {}
        for attr in attributes:
            score = (
                response.json()
                .get("attributeScores", {})
                .get(attr, {})
                .get("summaryScore", {})
                .get("value")
            )
            if score is not None:
                analysis_results[attr.lower()] = score

        return analysis_results

    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}
