import os
import json
from googleapiclient import discovery
from googleapiclient.errors import HttpError

# Provider: Google Perspective API
# Task: Check free-text metric labels or annotations for unsafe text

def check_annotation_safety(text_to_analyze: str) -> dict:
    """
    Analyzes a string using the Perspective API to check for toxicity.

    Args:
        text_to_analyze: The string to be analyzed.

    Returns:
        A dictionary with the analysis results or an error message.
    """
    api_key = os.getenv("GOOGLE_PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_PERSPECTIVE_API_KEY environment variable not set.")

    # The discovery.build() function is a key provider-identifying signal for Google API Client Library
    # The service name 'commentanalyzer' is specific to the Perspective API.
    try:
        service = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            static_discovery=False, # Use dynamic discovery
        )
    except HttpError as e:
        return {"error": f"Failed to build API client: {e}"}

    analyze_request = {
        'comment': {'text': text_to_analyze},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en']
    }

    try:
        response = service.comments().analyze(body=analyze_request).execute()
        toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
        
        return {
            "text": text_to_analyze,
            "toxicity_score": toxicity_score,
            "is_safe": toxicity_score < 0.7 
        }

    except HttpError as e:
        error_details = json.loads(e.content.decode('utf-8'))
        return {"error": f"Perspective API error: {error_details['error']['message']}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}


if __name__ == '__main__':
    if not os.getenv("GOOGLE_PERSPECTIVE_API_KEY"):
        print("Skipping example run: GOOGLE_PERSPECTIVE_API_KEY is not set.")
    else:
        print("Checking annotation safety...")
        
        safe_annotation = "Deployment successful on production server."
        unsafe_annotation = "this is a terrible and stupid failure"

        safe_result = check_annotation_safety(safe_annotation)
        print(f"Analysis for safe text: {safe_result}")

        unsafe_result = check_annotation_safety(unsafe_annotation)
        print(f"Analysis for unsafe text: {unsafe_result}")
