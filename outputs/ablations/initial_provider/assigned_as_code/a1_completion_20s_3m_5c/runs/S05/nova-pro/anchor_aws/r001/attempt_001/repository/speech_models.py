class TranscriptionRequest:
    def __init__(self, language_code, sample_rate_hz, audio_chunks):
        self.language_code = language_code
        self.sample_rate_hz = sample_rate_hz
        self.audio_chunks = audio_chunks

class TranscriptionResponse:
    def __init__(self, text, is_final):
        self.text = text
        self.is_final = is_final

def normalize_transcription_response(response):
    return TranscriptionResponse(response['text'], response['is_final'])