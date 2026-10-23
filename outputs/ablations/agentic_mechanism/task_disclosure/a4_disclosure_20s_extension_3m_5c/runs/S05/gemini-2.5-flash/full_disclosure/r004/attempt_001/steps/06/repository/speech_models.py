import dataclasses
from typing import List, Optional

# Provider-specific signal for Google Cloud Speech-to-Text
# This import is not directly used in the classes below, but serves as a provider-identifying signal.
# In a real integration, the client from this SDK would be used to make API calls.
from google.cloud import speech_v1p1beta1

@dataclasses.dataclass
class StreamingRecognitionConfig:
    """
    Configuration for streaming speech recognition.
    Corresponds to google.cloud.speech_v1p1beta1.StreamingRecognitionConfig.
    """
    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = False
    enable_word_time_offsets: bool = False
    model: str = "default"
    profanity_filter: bool = False
    # Add other relevant configuration parameters as needed

@dataclasses.dataclass
class RecognitionAudio:
    """
    Audio content for recognition.
    Corresponds to google.cloud.speech_v1p1beta1.RecognitionAudio.
    """
    content: Optional[bytes] = None
    uri: Optional[str] = None

@dataclasses.dataclass
class StreamingRecognizeRequest:
    """
    Request for streaming speech recognition.
    Corresponds to google.cloud.speech_v1p1beta1.StreamingRecognizeRequest.
    """
    streaming_config: Optional[StreamingRecognitionConfig] = None
    audio_content: Optional[bytes] = None

@dataclasses.dataclass
class SpeechRecognitionAlternative:
    """
    A transcript alternative for a portion of the audio.
    Corresponds to google.cloud.speech_v1p1beta1.SpeechRecognitionAlternative.
    """
    transcript: str
    confidence: float
    # Add word info if enable_word_time_offsets is true

@dataclasses.dataclass
class StreamingRecognitionResult:
    """
    A single result corresponding to a portion of the audio.
    Corresponds to google.cloud.speech_v1p1beta1.StreamingRecognitionResult.
    """
    alternatives: List[SpeechRecognitionAlternative]
    is_final: bool
    stability: float

@dataclasses.dataclass
class StreamingRecognizeResponse:
    """
    Response from streaming speech recognition.
    Corresponds to google.cloud.speech_v1p1beta1.StreamingRecognizeResponse.
    """
    results: List[StreamingRecognitionResult]
    end_of_single_utterance: bool = False

def normalize_transcript(response: StreamingRecognizeResponse) -> str:
    """
    Normalizes the transcript from a StreamingRecognizeResponse.
    This is a placeholder for actual normalization logic.
    """
    if response and response.results:
        # Assuming we take the first alternative of the first result for simplicity
        # Real-world normalization might involve more complex logic,
        # such as combining multiple alternatives, handling punctuation, etc.
        final_transcripts = [
            result.alternatives[0].transcript
            for result in response.results
            if result.is_final and result.alternatives
        ]
        if final_transcripts:
            return " ".join(final_transcripts)
    return ""
