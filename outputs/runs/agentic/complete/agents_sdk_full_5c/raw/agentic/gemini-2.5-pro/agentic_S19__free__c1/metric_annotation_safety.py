
import os
import json
from googleapiclient import discovery
from googleapiclient.errors import HttpError


def check_annotation_safety(text: str) -> dict:
    """
    Checks free-text annotations for unsafe content using the Perspective API.

    Args:
        text: The annotation text to analyze.

    Returns:
        A dictionary with toxicity analysis results.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # The client is created dynamically based on the discovery document.
    # See: https://github.com/googleapis/google-api-python-client
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}}
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        
        scores = {}
        for attr, value in response['attributeScores'].items():
            scores[attr] = value['summaryScore']['value']
        
        return {
            "text": text,
            "scores": scores,
            "safe": scores.get("TOXICITY", 1.0) < 0.7
        }

    except HttpError as e:
        print(f"Perspective API error: {e}")
        error_content = json.loads(e.content)
        return {
            "text": text,
            "error": error_content.get("error", {}).get("message", "Unknown error")
        }


if __name__ == '__main__':
    safe_annotation = "Deployment completed successfully. CPU usage is stable."
    unsafe_annotation = "This is a stupid and terrible alert configuration."

    print("--- Checking Safe Annotation ---")
    result_safe = check_annotation_safety(safe_annotation)
    print(json.dumps(result_safe, indent=2))

    print("\n--- Checking Unsafe Annotation ---")
    result_unsafe = check_annotation_safety(unsafe_annotation)
    print(json.dumps(result_unsafe, indent=2))
