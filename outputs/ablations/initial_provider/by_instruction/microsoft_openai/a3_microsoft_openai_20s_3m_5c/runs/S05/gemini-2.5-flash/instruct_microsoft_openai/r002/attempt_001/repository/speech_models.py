from dataclasses import dataclass
import azure.cognitiveservices.speech as speechsdk

@dataclass
class TranscriptEvent:
    type: str  # "recognizing" or "recognized"
    text: str

def normalize_speech_recognition_result(result: speechsdk.SpeechRecognitionResult) -> TranscriptEvent | None:
    if result.reason == speechsdk.ResultReason.RecognizingSpeech:
        return TranscriptEvent(type="recognizing", text=result.text)
    elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return TranscriptEvent(type="recognized", text=result.text)
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return TranscriptEvent(type="recognized", text="") # No match, return empty text for final
    return None
