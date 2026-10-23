import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError


def check_annotation_safety(text: str) -> dict:
    """
    Checks free-text metric labels or annotations for unsafe text using the Perspective API.

    Args:
        text: The annotation text to analyze.

    Returns:
        A dictionary with toxicity scores or an error message.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    try:
        # The specific API name is 'commentanalyzer'
        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            static_discovery=False,
        )

        analyze_request = {
            'comment': {'text': text},
            'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}},
            'languages': ['en']
        }

        response = client.comments().analyze(body=analyze_request).execute()

        scores = {}
        for attribute, data in response['attributeScores'].items():
            scores[attribute] = data['summaryScore']['value']
            
        return scores

    except HttpError as e:
        return {"error": f"Perspective API error: {e}", "details": e.content.decode()}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

# Example Usage:
# if __name__ == '__main__':
#     if os.environ.get("PERSPECTIVE_API_KEY"):
#         safe_text = "Investigating CPU spike on web-prod-01"
#         unsafe_text = "This is a terrible, stupid alert that someone should fix."

#         print(f"Analyzing safe text: '{safe_text}'")
#         result_safe = check_annotation_safety(safe_text)
#         print(result_safe)

#         print(f"\nAnalyzing unsafe text: '{unsafe_text}'")
#         result_unsafe = check_annotation_safety(unsafe_text)
#         print(result_unsafe)
#     else:
#         print("PERSPECTIVE_API_KEY environment variable not set.")
#         print("This key is obtained from the Google Cloud Console for the Perspective API.")
