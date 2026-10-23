from google.cloud import speech_v1p1beta1 as speech

def normalize_transcript(transcript):
    return transcript.strip().capitalize()

def extract_transcript(result):
    return result.alternatives[0].transcript