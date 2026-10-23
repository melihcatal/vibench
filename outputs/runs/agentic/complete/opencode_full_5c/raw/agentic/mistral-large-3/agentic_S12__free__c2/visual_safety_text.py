from typing import List, Dict
import requests


def check_text_safety(texts: List[str]) -> Dict[str, List[dict]]:
    """Check texts for unsafe content using Perspective API."""
    api_key = (
        "YOUR_PERSPECTIVE_API_KEY"  # Replace with environment variable in production
    )
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    unsafe_categories = {
        "TOXICITY": [],
        "SEVERE_TOXICITY": [],
        "IDENTITY_ATTACK": [],
        "INSULT": [],
        "PROFANITY": [],
        "THREAT": [],
    }

    for text in texts:
        data = {
            "comment": {"text": text},
            "requestedAttributes": {
                category: {} for category in unsafe_categories.keys()
            },
        }

        response = requests.post(url, json=data)
        response.raise_for_status()

        for category in unsafe_categories.keys():
            score = response.json()["attributeScores"][category]["summaryScore"][
                "value"
            ]
            if score > 0.7:
                unsafe_categories[category].append({"text": text, "score": score})

    return {"unsafe_text": unsafe_categories}


def check_visual_labels_for_unsafe_text(labels: List[str]) -> Dict[str, List[dict]]:
    """Check generated visual labels for unsafe text using Perspective API."""
    return check_text_safety(labels)
