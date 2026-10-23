import os
from typing import Dict, Any

from observability_client import PerspectiveAPIClient

def check_metric_annotation_safety(text: str) -> Dict[str, Any]:
    """
    Checks free-text metric labels or annotations for unsafe text using Google Cloud's Perspective API.

    Args:
        text: The free-text annotation or label to check.

    Returns:
        A dictionary containing safety analysis results, including scores for various attributes and an overall safety flag.
    """
    # Google Cloud credentials must be configured (e.g., via GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or gcloud auth application-default login)

    client = PerspectiveAPIClient()
    safety_report = client.check_annotation_safety(text)
    return safety_report

if __name__ == '__main__':
    # Example usage
    print("Checking annotation safety...")

    safe_text = "This is a normal and good metric annotation."
    unsafe_text_1 = "This annotation contains hateful and toxic language!"
    unsafe_text_2 = "You are an idiot and should be fired!"

    print(f"\nAnalyzing: '{safe_text}'")
    try:
        report1 = check_metric_annotation_safety(safe_text)
        print(report1)
    except Exception as e:
        print(f"Error analyzing safe text: {e}")

    print(f"\nAnalyzing: '{unsafe_text_1}'")
    try:
        report2 = check_metric_annotation_safety(unsafe_text_1)
        print(report2)
    except Exception as e:
        print(f"Error analyzing unsafe text 1: {e}")

    print(f"\nAnalyzing: '{unsafe_text_2}'")
    try:
        report3 = check_metric_annotation_safety(unsafe_text_2)
        print(report3)
    except Exception as e:
        print(f"Error analyzing unsafe text 2: {e}")
