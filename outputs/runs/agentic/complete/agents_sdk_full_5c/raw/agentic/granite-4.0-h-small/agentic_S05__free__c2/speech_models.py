import json

# Example normalization helpers

def parse_recognition_response(response_json):
    """Extracts transcript data from provider response."""
    data = json.loads(response_json)
    transcripts = []
    for result in data.get('results', []):
        alternatives = result.get('alternatives', [])
        if alternatives:
            transcripts.append(alternatives[0].get('transcript', ''))
    return transcripts


def normalize_text(text):
    """Simple whitespace and punctuation cleanup."""
    return ' '.join(text.split())