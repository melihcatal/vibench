
import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_text_for_toxicity(text: str, api_key: str) -> float | None:
    """
    Uses the Google Perspective API to check text for toxicity.

    Args:
        text: The text string to analyze.
        api_key: Your Google Cloud API key for the Perspective API.

    Returns:
        The toxicity score (0.0 to 1.0), or None on failure.
    """
    try:
        # Note: discovery.build is not thread-safe
        # For multi-threaded applications, create a new client per thread.
        service = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
        )

        analyze_request = {
            'comment': {'text': text},
            'requestedAttributes': {'TOXICITY': {}}
        }

        response = service.comments().analyze(body=analyze_request).execute()
        
        toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
        return toxicity_score

    except HttpError as e:
        print(f"An HTTP error occurred with Perspective API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == '__main__':
    # Example usage:
    PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")

    if not PERSPECTIVE_API_KEY:
        print("PERSPECTIVE_API_KEY environment variable is not set.")
    else:
        # This label is safe
        safe_label = "Production database credentials for the billing service."
        safe_score = check_text_for_toxicity(safe_label, PERSPECTIVE_API_KEY)
        if safe_score is not None:
            print(f"'{safe_label}' -> Toxicity score: {safe_score:.4f}")
            if safe_score > 0.7:
                 print("  -> Unsafe label detected!")

        # This label contains problematic language
        unsafe_label = "This is a stupid password for the dumbest service."
        unsafe_score = check_text_for_toxicity(unsafe_label, PERSPECTIVE_API_KEY)
        if unsafe_score is not None:
            print(f"'{unsafe_label}' -> Toxicity score: {unsafe_score:.4f}")
            if unsafe_score > 0.7:
                 print("  -> Unsafe label detected!")
