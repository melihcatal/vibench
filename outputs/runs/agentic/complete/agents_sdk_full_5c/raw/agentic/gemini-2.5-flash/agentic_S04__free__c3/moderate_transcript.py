from googleapiclient import discovery
import json
import os

def get_perspective_client():
    """Returns a Google API client for the Perspective API."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or authenticated via gcloud
    # API key can also be used, but service account is preferred for server-side
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        cache_discovery=False
    )

def moderate_text_segment(text: str, attributes_to_analyze: list = None) -> dict:
    """Moderates a single text segment using Google Cloud Perspective API.

    Args:
        text: The text content to analyze.
        attributes_to_analyze: A list of attributes to analyze (e.g., ['TOXICITY', 'FLIRTATION']).
                               Defaults to ['TOXICITY'].

    Returns:
        A dictionary containing the analysis results.
    """
    if attributes_to_analyze is None:
        attributes_to_analyze = ['TOXICITY']

    client = get_perspective_client()

    analyze_request = {
        'comment': { 'text': text },
        'requestedAttributes': { attr: {} for attr in attributes_to_analyze }
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

def moderate_transcript_segments(segments: list[str], attributes_to_analyze: list = None) -> list[dict]:
    """Moderates multiple transcript segments using Google Cloud Perspective API.

    Args:
        segments: A list of text segments to moderate.
        attributes_to_analyze: A list of attributes to analyze.

    Returns:
        A list of dictionaries, each containing the analysis results for a segment.
    """
    moderation_results = []
    for segment in segments:
        result = moderate_text_segment(segment, attributes_to_analyze)
        moderation_results.append(result)
    return moderation_results

# Example usage
# if __name__ == "__main__":
#     # sample_segments = [
#     #     "You are an amazing person.",
#     #     "You are stupid and I hate you.",
#     #     "Let's hang out later."
#     # ]
#     # 
#     # attributes = ['TOXICITY', 'INSULT', 'FLIRTATION']
#     # 
#     # results = moderate_transcript_segments(sample_segments, attributes)
#     # for i, res in enumerate(results):
#     #     print(f"Segment {i+1}: '{sample_segments[i]}'")
#     #     for attr, scores in res.get('attributeScores', {}).items():
#     #         print(f"  {attr}: {scores['summaryScore']['value']}")
#     pass
