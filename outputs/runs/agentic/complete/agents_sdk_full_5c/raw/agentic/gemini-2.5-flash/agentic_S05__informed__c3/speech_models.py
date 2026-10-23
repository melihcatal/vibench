import json
import azure.cognitiveservices.speech as speechsdk

class SpeechRecognitionResult:
    def __init__(self, text: str, offset: int, duration: int, is_final: bool):
        self.text = text
        self.offset = offset
        self.duration = duration
        self.is_final = is_final

    def to_json(self):
        return json.dumps({
            "text": self.text,
            "offset": self.offset,
            "duration": self.duration,
            "is_final": self.is_final
        })

def normalize_azure_recognition_event(event: speechsdk.SpeechRecognitionEventArgs, is_final: bool = False):
    # event.result is a SpeechRecognitionResult object with attributes like text, offset, duration
    if event.result.reason == speechsdk.ResultReason.RecognizedSpeech or \
       event.result.reason == speechsdk.ResultReason.RecognizingSpeech:
        return SpeechRecognitionResult(
            text=event.result.text,
            offset=event.result.offset,
            duration=event.result.duration,
            is_final=is_final
        )
    return None
