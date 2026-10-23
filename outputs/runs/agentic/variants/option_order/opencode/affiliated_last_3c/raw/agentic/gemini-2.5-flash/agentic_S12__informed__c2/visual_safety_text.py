import os
import requests
from vision_models import TextSafetyCheck


def check_visual_labels_safety(text: str) -> TextSafetyCheck:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # Perspective API can analyze various attributes, here we check for TOXICITY.
    # You can add more attributes as needed.
    data = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}

    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()

    unsafe_categories = []
    overall_safety_score = 0.0

    if "attributeScores" in result:
        toxicity_score = (
            result["attributeScores"]
            .get("TOXICITY", {})
            .get("summaryScore", {})
            .get("value", 0.0)
        )
        overall_safety_score = toxicity_score
        if toxicity_score > 0.5:  # Threshold for considering it unsafe
            unsafe_categories.append("TOXICITY")

    return TextSafetyCheck(
        unsafe_categories=unsafe_categories, overall_safety_score=overall_safety_score
    )
