from google.cloud import speech


def normalize_transcript(transcript):
    return transcript.lower()


def format_response(response):
    return {"text": response["text"], "is_final": response["is_final"]}