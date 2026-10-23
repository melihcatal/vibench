import requests
from speech_models import normalize_transcript, SpeechRecognitionResult

# Perspective API example (rest)
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def check_safety(text: str) -> dict:
    """Uses Perspective API to detect unsafe content in live transcript.
    Args:
        text (str): transcript chunk to evaluate
    Returns:
        dict: API response containing scores
    """
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "SPAM": {}},
    }
    headers = {
        "content-type": "application/json",
        "x-goog-api-key": PERSPECTIVE_API_KEY,
    }
    resp = requests.post(PERSPECTIVE_API_URL, json=payload, headers=headers)
    return resp.json()


# Sample usage in streaming flow (placeholder)
# async for chunk in stream_microphone():
#     result = json.loads(chunk)
#     safety = check_safety(normalize_transcript(result))
#     if safety['attributeScores']['TOXICITY']['summaryScore']['value'] > 0.8:
#         print('WARNING: Unsafe content detected')
