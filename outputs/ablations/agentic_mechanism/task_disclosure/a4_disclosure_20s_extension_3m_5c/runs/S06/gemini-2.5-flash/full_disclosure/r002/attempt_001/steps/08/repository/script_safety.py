import os
from googleapiclient import discovery
from googleapiclient import errors

def check_narration_script_safety(script_text: str, threshold: float = 0.7) -> dict:
    """
    Checks narration scripts for unsafe content using Google Cloud's Perspective API.

    Args:
        script_text: The narration script content to check.
        threshold: The confidence threshold (0.0 to 1.0) for flagging content as unsafe.
                   If any attribute's score exceeds this threshold, it's considered unsafe.

    Returns:
        A dictionary containing the safety analysis results, including a 'is_unsafe' boolean
        and the detailed attribute scores.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Provider-identifying signal: using googleapiclient to build the Perspective API service
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        cache_discovery=False
    )

    analyze_request = {
        'comment': {'text': script_text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'THREAT': {},
            'SEXUALLY_EXPLICIT': {},
            'PROFANITY': {}
        }
    }

    response = {'is_unsafe': False, 'scores': {}}

    try:
        api_response = client.comments().analyze(body=analyze_request).execute()

        for attribute, value in api_response['attributeScores'].items():
            score = value['summaryScore']['value']
            response['scores'][attribute] = score
            if score > threshold:
                response['is_unsafe'] = True

    except errors.HttpError as e:
        print(f"Error calling Perspective API: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return response
