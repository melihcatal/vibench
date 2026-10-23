import os
from typing import List, Dict, Any
import requests
from vision_client import get_openai_api_key


def check_labels_for_unsafe_text(labels: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Check generated visual labels for unsafe text using OpenAI Moderation API.

    Args:
        labels: List of label dictionaries containing descriptions

    Returns:
        Dictionary containing moderation results and flagged items
    """
    api_key = get_openai_api_key()

    label_texts = [label.get("description", "") for label in labels]
    combined_text = " ".join(label_texts)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {"input": combined_text}

    response = requests.post(
        "https://api.openai.com/v1/moderations", headers=headers, json=payload
    )
    response.raise_for_status()

    result = response.json()

    moderation_result = result.get("results", [{}])[0]

    flagged_labels = []
    for i, label in enumerate(labels):
        label_text = label.get("description", "")
        if any(
            keyword in label_text.lower()
            for keyword in ["violent", "explicit", "adult", "hate"]
        ):
            flagged_labels.append(
                {"label": label_text, "reason": "keyword_match", "index": i}
            )

    return {
        "flagged": moderation_result.get("flagged", False),
        "categories": moderation_result.get("categories", {}),
        "category_scores": moderation_result.get("category_scores", {}),
        "flagged_labels": flagged_labels,
        "total_labels_checked": len(labels),
        "provider": "openai-moderation",
        "model": "text-moderation-latest",
    }
