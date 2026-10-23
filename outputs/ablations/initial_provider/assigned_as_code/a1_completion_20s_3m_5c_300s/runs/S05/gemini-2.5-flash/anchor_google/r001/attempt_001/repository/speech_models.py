class SpeechRecognitionRequest:
    def __init__(self, audio_chunks, sample_rate_hz, language_code, enable_automatic_punctuation=False):
        self.audio_chunks = audio_chunks
        self.sample_rate_hz = sample_rate_hz
        self.language_code = language_code
        self.enable_automatic_punctuation = enable_automatic_punctuation

class SpeechRecognitionResult:
    def __init__(self, transcript, is_final):
        self.transcript = transcript
        self.is_final = is_final

def normalize_response(response):
    # Placeholder for response normalization if needed
    return response
