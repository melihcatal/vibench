from googleapiclient import discovery
import os

def moderate_vendor_notes(text_content: str) -> dict:
    """
    Moderates vendor notes or memo fields using Google Cloud Perspective API.
    """
    # Build the Perspective API client
    # Ensure GOOGLE_API_KEY is set in your environment for authentication
    API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': { 'text': text_content },
        'requestedAttributes': { 'TOXICITY': {}, 'FLIRTATION': {}, 'SEXUALLY_EXPLICIT': {}}
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        return response
    except Exception as e:
        return {"error": f"Error moderating text with Perspective API: {e}"}
