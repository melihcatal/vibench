import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config
from speech_models import TranscriptResult, normalize_transcript

class PartialResultsHandler:
    def __init__(self):
        self.latest_partial_result = ""
        self.final_results = []

    def handle_intermediate_result(self, evt: speechsdk.SpeechRecognitionEventArgs):
        self.latest_partial_result = evt.result.text
        # print(f"Partial: {self.latest_partial_result}") # For debugging
        # Yield or process the partial result as needed
        yield TranscriptResult(text=normalize_transcript(self.latest_partial_result), is_partial=True)

    def handle_final_result(self, evt: speechsdk.SpeechRecognitionEventArgs):
        final_text = evt.result.text
        self.final_results.append(final_text)
        self.latest_partial_result = ""
        print(f"Final: {final_text}")
        # Yield or process the final result as needed
        yield TranscriptResult(text=normalize_transcript(final_text), is_partial=False)

    def setup_recognizer_callbacks(self, recognizer: speechsdk.SpeechRecognizer):
        recognizer.recognizing.connect(lambda evt: list(self.handle_intermediate_result(evt))) # Use list to consume generator
        recognizer.recognized.connect(lambda evt: list(self.handle_final_result(evt))) # Use list to consume generator

# Example usage (can be integrated into stream_microphone.py or stream_chunks.py)
async def demonstrate_partial_results(recognizer: speechsdk.SpeechRecognizer):
    handler = PartialResultsHandler()
    handler.setup_recognizer_callbacks(recognizer)
    print("Recognizer callbacks for partial results set up.")
