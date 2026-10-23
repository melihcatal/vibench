import azure.cognitiveservices.speech as speechsdk
import os

def handle_partial_and_final_results(speech_recognizer: speechsdk.SpeechRecognizer):
    def recognizing_handler(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
            print(f"PARTIAL: {evt.result.text}")

    def recognized_handler(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"FINAL: {evt.result.text}")
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print(f"NOMATCH: Speech could not be recognized.")
        
    speech_recognizer.recognizing.connect(recognizing_handler)
    speech_recognizer.recognized.connect(recognized_handler)
