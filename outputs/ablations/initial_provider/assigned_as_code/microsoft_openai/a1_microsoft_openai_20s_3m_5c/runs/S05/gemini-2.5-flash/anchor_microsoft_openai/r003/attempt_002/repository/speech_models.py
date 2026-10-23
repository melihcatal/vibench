class TranscriptionResult:
    def __init__(self, text, is_final):
        self.text = text
        self.is_final = is_final

    def to_dict(self):
        return {"text": self.text, "is_final": self.is_final}

def normalize_response(speech_recognition_event):
    if speech_recognition_event.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return TranscriptionResult(speech_recognition_event.result.text, is_final=True)
    elif speech_recognition_event.result.reason == speechsdk.ResultReason.RecognizingSpeech:
        return TranscriptionResult(speech_recognition_event.result.text, is_final=False)
    return None

import azure.cognitiveservices.speech as speechsdk
