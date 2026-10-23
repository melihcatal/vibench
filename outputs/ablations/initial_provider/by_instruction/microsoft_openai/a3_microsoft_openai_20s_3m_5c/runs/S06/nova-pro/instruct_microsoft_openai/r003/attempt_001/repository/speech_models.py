from azure.cognitiveservices.speech import SpeechSynthesisOutputFormat

class SpeechRequest:
    def __init__(self, text: str, ssml: str = None):
        self.text = text
        self.ssml = ssml

class SpeechResponse:
    def __init__(self, audio_data: bytes):
        self.audio_data = audio_data

def normalize_response(response):
    return SpeechResponse(response.audio_data)