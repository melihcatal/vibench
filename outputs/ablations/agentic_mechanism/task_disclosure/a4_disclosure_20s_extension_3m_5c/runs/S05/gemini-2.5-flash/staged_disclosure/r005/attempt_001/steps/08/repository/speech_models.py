
class StreamingSpeechRecognitionRequest:
    def __init__(self, audio_chunk: bytes, sample_rate_hertz: int, language_code: str):
        self.audio_chunk = audio_chunk
        self.sample_rate_hertz = sample_rate_hertz
        self.language_code = language_code

class StreamingSpeechRecognitionResponse:
    def __init__(self, transcript: str, is_final: bool):
        self.transcript = transcript
        self.is_final = is_final

def normalize_transcript(transcript: str) -> str:
    """
    Normalizes the transcript by performing basic cleaning.
    """
    return transcript.strip().lower()

def create_streaming_request(audio_data: bytes, sample_rate: int, lang_code: str) -> StreamingSpeechRecognitionRequest:
    """
    Helper to create a StreamingSpeechRecognitionRequest object.
    """
    return StreamingSpeechRecognitionRequest(audio_data, sample_rate, lang_code)

def parse_streaming_response(response_data) -> StreamingSpeechRecognitionResponse:
    """
    Helper to parse raw response data into StreamingSpeechRecognitionResponse.
    (This would be expanded to handle actual API responses from a speech-to-text service)
    """
    # Placeholder for actual parsing logic
    transcript = response_data.get("transcript", "")
    is_final = response_data.get("is_final", False)
    return StreamingSpeechRecognitionResponse(transcript, is_final)
