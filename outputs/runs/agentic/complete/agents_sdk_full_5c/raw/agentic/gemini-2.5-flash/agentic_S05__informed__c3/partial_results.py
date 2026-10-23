import azure.cognitiveservices.speech as speechsdk
import os

def handle_streaming_events():
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.AudioConfig(use_ microphone=True)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    def recognizing_handler(evt):
        print(f"PARTIAL: {evt.result.text}")

    def recognized_handler(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"FINAL: {evt.result.text}")
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print(f"NOMATCH: Speech could not be recognized.")

    def canceled_handler(evt):
        print(f"CANCELED: Reason={evt.reason}")
        if evt.reason == speechsdk.ResultReason.CanceledWithError:
            print(f"CANCELED: ErrorDetails={evt.error_details}")

    speech_recognizer.recognizing.connect(recognizing_handler)
    speech_recognizer.recognized.connect(recognized_handler)
    speech_recognizer.canceled.connect(canceled_handler)

    print("Speak into your microphone to see partial and final results.")
    
    # Start recognition and wait for a single utterance
    # For continuous streaming, use start_continuous_recognition()
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognition successful for a single utterance.")
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print(f"No speech could be recognized in a single utterance: {result.no_match_details}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        print(f"Recognition canceled for a single utterance: {result.cancellation_details.reason}")
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {result.cancellation_details.error_details}")

if __name__ == "__main__":
    handle_streaming_events()
