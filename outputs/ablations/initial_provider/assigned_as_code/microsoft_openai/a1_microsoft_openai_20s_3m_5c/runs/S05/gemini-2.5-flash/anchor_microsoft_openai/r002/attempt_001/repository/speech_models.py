import azure.cognitiveservices.speech as speechsdk
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class SpeechRecognitionConfig:
    language_code: str
    sample_rate_hz: int = 16000
    
@dataclass
class SpeechRecognitionResult:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    reason: Optional[speechsdk.ResultReason] = None

def normalize_azure_result(azure_speech_event) -> SpeechRecognitionResult:
    if isinstance(azure_speech_event, speechsdk.SpeechRecognitionEventArgs):
        return SpeechRecognitionResult(
            text=azure_speech_event.result.text,
            is_final=azure_speech_event.result.reason == speechsdk.ResultReason.RecognizedSpeech,
            confidence=azure_speech_event.result.confidence if hasattr(azure_speech_event.result, 'confidence') else None,
            reason=azure_speech_event.result.reason
        )
    elif isinstance(azure_speech_event, speechsdk.RecognitionEventArgs):
        return SpeechRecognitionResult(
            text=azure_speech_event.result.text,
            is_final=azure_speech_event.result.reason == speechsdk.ResultReason.RecognizedSpeech,
            confidence=None, # Azure SpeechRecognitionEventArgs has confidence, RecognitionEventArgs does not always.
            reason=azure_speech_event.result.reason
        )
    else:
        raise TypeError(f"Unexpected event type: {type(azure_speech_event)}")
