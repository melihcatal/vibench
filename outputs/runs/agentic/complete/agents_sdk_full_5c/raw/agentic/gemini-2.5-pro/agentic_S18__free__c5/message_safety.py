
import os
from googleapiclient import discovery
from messaging_models import ProcessingResult

def check_content_safety(text: str, event_id: str) -> ProcessingResult:
    """
    Checks message text for unsafe content using Google's Perspective API.

    Args:
        text: The text to analyze.
        event_id: The ID of the event being processed.

    Returns:
        A ProcessingResult object with safety scores.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    try:
        # The provider is identified by the API name 'commentanalyzer' and its discovery URL
        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
        )

        analyze_request = {
            'comment': {'text': text},
            'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}}
        }

        response = client.comments().analyze(body=analyze_request).execute()

        scores = {}
        for attribute, data in response['attributeScores'].items():
            scores[attribute] = data['summaryScore']['value']
        
        return ProcessingResult(original_event_id=event_id, status="SUCCESS", safety_check=scores)

    except Exception as e:
        print(f"An error occurred with the Perspective API: {e}")
        return ProcessingResult(original_event_id=event_id, status="FAILURE", error_message=str(e))

if __name__ == '__main__':
    # Example Usage:
    # Set the following environment variable before running:
    # export PERSPECTIVE_API_KEY="your-google-api-key"

    # unsafe_text = "You are a terrible person and I hope you fail."
    # result = check_content_safety(unsafe_text, "event-789")
    # print(result.to_dict())

    # safe_text = "I hope you have a wonderful and productive day."
    # result_safe = check_content_safety(safe_text, "event-790")
    # print(result_safe.to_dict())
    pass
