# No specific models or complex normalization needed for simple Google Cloud Speech-to-Text SDK usage.
# Placeholder for future complex request/response shaping or normalization if required.


class SpeechRecognitionRequest:
    def __init__(self, audio_content: bytes, language_code: str = "en-US"):
        self.audio_content = audio_content
        self.language_code = language_code


class SpeechRecognitionResult:
    def __init__(self, transcript: str, is_final: bool):
        self.transcript = transcript
        self.is_final = is_final


def normalize_google_speech_response(response):
    if not response.results:
        return None
    result = response.results[0]
    if not result.alternatives:
        return None
    return SpeechRecognitionResult(
        transcript=result.alternatives[0].transcript, is_final=result.is_final
    )
