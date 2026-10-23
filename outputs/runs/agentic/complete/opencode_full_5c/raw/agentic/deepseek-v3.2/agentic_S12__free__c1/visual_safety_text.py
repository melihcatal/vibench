import os
import requests
from typing import List, Dict, Any
from vision_client import get_openai_api_key
from vision_models import ImageLabel


def check_labels_for_unsafe_text(labels: List[ImageLabel]) -> Dict[str, Any]:
    """Check generated visual labels for unsafe text using OpenAI's moderation API."""
    api_key = get_openai_api_key()

    # Combine label descriptions into a single text for moderation
    label_texts = [label.description for label in labels]
    combined_text = " ".join(label_texts)

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {"input": combined_text, "model": "text-moderation-latest"}

    response = requests.post(
        "https://api.openai.com/v1/moderations", headers=headers, json=payload
    )
    response.raise_for_status()

    result = response.json()

    if "results" in result and len(result["results"]) > 0:
        moderation_result = result["results"][0]

        flagged_labels = []
        for label in labels:
            # Check if individual label text might be problematic
            label_payload = {
                "input": label.description,
                "model": "text-moderation-latest",
            }

            label_response = requests.post(
                "https://api.openai.com/v1/moderations",
                headers=headers,
                json=label_payload,
            )

            if label_response.status_code == 200:
                label_result = label_response.json()
                if (
                    label_result.get("results")
                    and len(label_result["results"]) > 0
                    and label_result["results"][0]["flagged"]
                ):
                    flagged_labels.append(
                        {
                            "label": label.description,
                            "score": label.score,
                            "moderation_result": label_result["results"][0],
                        }
                    )

        return {
            "overall_flagged": moderation_result["flagged"],
            "overall_categories": moderation_result["categories"],
            "overall_category_scores": moderation_result["category_scores"],
            "flagged_labels": flagged_labels,
        }

    return {
        "overall_flagged": False,
        "overall_categories": {},
        "overall_category_scores": {},
        "flagged_labels": [],
    }


if __name__ == "__main__":
    # Example usage
    sample_labels = [
        ImageLabel(description="dog", score=0.95),
        ImageLabel(description="park", score=0.87),
        ImageLabel(description="violence", score=0.45),
        ImageLabel(description="hate speech", score=0.32),
    ]

    safety_check = check_labels_for_unsafe_text(sample_labels)
    print(f"Overall flagged: {safety_check['overall_flagged']}")
    print(f"Flagged labels: {len(safety_check['flagged_labels'])}")

    for flagged in safety_check["flagged_labels"]:
        print(f"  - {flagged['label']}")
