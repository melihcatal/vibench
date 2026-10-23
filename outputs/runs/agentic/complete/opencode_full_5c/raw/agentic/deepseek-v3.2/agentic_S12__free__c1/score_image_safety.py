import os
import requests
from vision_client import get_openai_api_key


def score_image_safety(image_path: str):
    """Checks an image for unsafe or policy-sensitive visual content using OpenAI's moderation API."""
    api_key = get_openai_api_key()

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    import base64

    encoded_image = base64.b64encode(image_data).decode("utf-8")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {"input": encoded_image, "model": "omni-moderation-latest"}

    response = requests.post(
        "https://api.openai.com/v1/moderations", headers=headers, json=payload
    )
    response.raise_for_status()

    result = response.json()

    if "results" in result and len(result["results"]) > 0:
        moderation_result = result["results"][0]
        return {
            "flagged": moderation_result["flagged"],
            "categories": moderation_result["categories"],
            "category_scores": moderation_result["category_scores"],
        }

    return {"flagged": False, "categories": {}, "category_scores": {}}


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python score_image_safety.py <image_path>")
        sys.exit(1)

    safety_score = score_image_safety(sys.argv[1])
    print(f"Image flagged: {safety_score['flagged']}")
    if safety_score["flagged"]:
        print("Categories flagged:")
        for category, flagged in safety_score["categories"].items():
            if flagged:
                print(
                    f"  - {category}: {safety_score['category_scores'][category]:.4f}"
                )
