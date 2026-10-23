import json
import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# IBM Watson Speech to Text setup
WATSON_SPEECH_TO_TEXT_APIKEY = os.environ.get("WATSON_SPEECH_TO_TEXT_APIKEY")
WATSON_SPEECH_TO_TEXT_URL = os.environ.get("WATSON_SPEECH_TO_TEXT_URL")

def stream_with_language_and_punctuation():
    authenticator = IAMAuthenticator(WATSON_SPEECH_TO_TEXT_APIKEY)
    speech_to_text = SpeechToTextV1(
        authenticator=authenticator
    )
    speech_to_text.set_service_url(WATSON_SPEECH_TO_TEXT_URL)

    # In a real scenario, you would stream audio from a source (e.g., microphone)
    # For this example, we'll simulate an audio stream.
    # Replace this with your actual audio input handling.
    def get_audio_stream():
        # This is a dummy audio stream for demonstration purposes.
        # In a real application, you would read audio bytes from a microphone or file.
        yield b""

    print("Starting streaming recognition with language and punctuation...")

    try:
        # Start a websocket connection to the Watson Speech to Text service
        # and send audio data.
        # The 'result_callback' will handle the transcription results.
        response = speech_to_text.recognize_using_websocket(
            audio=get_audio_stream(),
            content_type='audio/l16; rate=16000',
            interim_results=True,
            model='en-US_BroadbandModel',
            speaker_labels=True,
            timestamps=True,
            word_alternatives_threshold=0.9,
            inactivity_timeout=5,
            processing_metrics=True,
            recognize_callback=MyRecognitionListener()
        )

    except Exception as e:
        print(f"Error during Watson Speech to Text streaming: {e}")

class MyRecognitionListener(object):
    def on_data(self, data):
        # Handle interim and final results
        if "results" in data:
            for result in data["results"]:
                if "alternatives" in result and result["alternatives"]:
                    transcript = result["alternatives"][0]["transcript"]
                    if result["final"]:
                        print(f"Final Transcript: {transcript}")
                    else:
                        print(f"Partial Transcript: {transcript}")

    def on_error(self, error):
        print(f"Error received from Watson Speech to Text: {error}")

    def on_close(self):
        print("Watson Speech to Text connection closed.")

