from google.cloud import speech_v1p1beta1 as speech


def normalize_transcript(transcript):
    return transcript.lower().strip()
