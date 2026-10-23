import os
import json
from speech_client import SpeechClient
from speech_models import TranscriptionResult

# Provider-specific: Perspective API for toxic content moderation
PERSPECTIVE_API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

client = SpeechClient(base_url=PERSPECTIVE_API_URL, api_key=PERSPECTIVE_API_KEY, provider='perspective')

def moderate_transcript(transcript_text: str, attributes: list = ['TOXICITY']) -> Dict:
    """Moderate a transcript using Perspective API.

    Args:
        transcript_text (str): Raw text of the transcript.
        attributes (list): List of attribute names to analyze (e.g., ['TOXICITY']).
    Returns:
        dict: Scores for each requested attribute.
    """
    payload = {
        'comment': {'text': transcript_text},
        'languages': ['en'],
        'requestedAttributes': {attr: {} for attr in attributes}
    }
    response = client.post('/comments:analyze', json=payload, params={'key': PERSPECTIVE_API_KEY})
    return response.get('attributeScores', {})

if __name__ == '__main__':
    # Example usage (replace with real transcript)
    transcript = 'This is a test comment that should be evaluated for toxicity.'
    scores = moderate_transcript(transcript)
    print('Moderation scores:', scores)
