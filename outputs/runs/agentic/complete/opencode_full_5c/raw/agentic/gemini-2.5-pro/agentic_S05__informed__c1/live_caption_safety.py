import os
import requests
import json


def check_caption_for_safety(text: str):
    """
    Checks live transcript text for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }

    try:
        response = requests.post(url, data=json.dumps(analyze_request))
        response.raise_for_status()
        response_dict = response.json()

        toxicity_score = response_dict["attributeScores"]["TOXICITY"]["summaryScore"][
            "value"
        ]
        is_unsafe = toxicity_score > 0.7

        return {
            "is_unsafe": is_unsafe,
            "toxicity_score": toxicity_score,
        }
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"is_unsafe": False, "toxicity_score": 0.0, "error": str(e)}
