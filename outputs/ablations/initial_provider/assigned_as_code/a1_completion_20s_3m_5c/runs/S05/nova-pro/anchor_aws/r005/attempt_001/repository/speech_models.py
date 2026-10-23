from google.cloud import speech

def normalize_transcript(transcript):
    return transcript.strip().lower()

def format_response(response):
    if response.results:
        for res in response.results:
            if res.is_final:
                return res.alternatives[0].transcript
    return ''