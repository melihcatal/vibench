from google.cloud import speech_v1p1beta1 as speech

def create_request(config, audio):
    return speech.RecognizeRequest(config=config, audio=audio)

def parse_response(response):
    for result in response.results:
        yield result.alternatives[0].transcript

def normalize_transcript(transcript):
    return transcript.lower().strip()