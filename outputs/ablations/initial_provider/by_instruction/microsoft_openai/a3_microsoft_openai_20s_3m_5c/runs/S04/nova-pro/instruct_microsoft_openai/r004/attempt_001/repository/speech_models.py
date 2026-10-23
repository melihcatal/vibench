from azure.ai.translation.document.models import DocumentTranslationDetails

class SpeechTranscriptionRequest:
    def __init__(self, input_data, input_kind):
        self.input_data = input_data
        self.input_kind = input_kind

class SpeechTranscriptionResponse:
    def __init__(self, details):
        self.details = details

def normalize_transcription_response(response):
    return SpeechTranscriptionResponse(response.details)