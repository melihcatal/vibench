from google.cloud import speech
from speech_models import SpeechResult

def handle_partial_results(responses):
    for response in responses:
        for result in response.results:
            transcript = result.alternatives[0].transcript
            is_final = result.is_final
            if is_final:
                print(f"FINAL TRANSCRIPT: {transcript}")
            else:
                print(f"INTERIM TRANSCRIPT: {transcript}")
            yield SpeechResult(transcript, is_final)
