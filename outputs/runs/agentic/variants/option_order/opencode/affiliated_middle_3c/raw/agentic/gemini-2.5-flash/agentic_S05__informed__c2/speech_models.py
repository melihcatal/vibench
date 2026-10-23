import dataclasses


@dataclasses.dataclass
class SpeechConfig:
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = False
    model: str = "default"


# Placeholder for response normalization if needed
def normalize_transcript_response(response):
    if not response.results:
        return ""
    return response.results[0].alternatives[0].transcript
