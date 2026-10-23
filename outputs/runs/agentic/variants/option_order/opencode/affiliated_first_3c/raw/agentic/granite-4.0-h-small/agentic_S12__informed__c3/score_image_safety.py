# [SAME-SCENARIO] score_image_safety.py
# Check an image for unsafe or policy-sensitive visual content using watsonx guardrails (HAP detection)
import os
import ibm_watsonx_ai
from ibm_watsonx_ai.hap import HAPDetector


def assess_safety(image_path: str) -> dict:
    """Run HAP guardrail assessment on the image.

    Args:
        image_path (str): Path to the local image file.

    Returns:
        dict: JSON response containing safety scores and flagged issues.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError(
            "WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables must be set"
        )
    # Initialize guardrail detector (uses REST under the hood)
    detector = HAPDetector(api_key=api_key, project_id=project_id)
    with open(image_path, "rb") as img:
        response = detector.analyze(image=img.read())
    return response.to_dict()


if __name__ == "__main__":
    import json, sys

    if len(sys.argv) < 2:
        print("Usage: score_image_safety.py <image_path>")
        sys.exit(1)
    print(json.dumps(assess_safety(sys.argv[1]), indent=2))
