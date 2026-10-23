from speech_client import client
from speech_models import SpeechTranscriptionRequest

def submit_transcription(file_path):
    input_data = file_path
    input_kind = DocumentTranslationInputKind.URL
    request = SpeechTranscriptionRequest(input_data, input_kind)
    poller = client.begin_translate_document(request)
    return poller.result()