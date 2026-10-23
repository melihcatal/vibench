from deepgram import LiveResult
from speech_models import extract_transcript

class PartialResultsHandler:
    def __init__(self, on_partial=None, on_final=None):
        self.on_partial = on_partial
        self.on_final = on_final

    def handle_transcript(self, result: LiveResult):
        text, is_final = extract_transcript(result.__dict__)
        if text:
            if is_final and self.on_final:
                self.on_final(text)
            elif not is_final and self.on_partial:
                self.on_partial(text)
            yield text  # for generator use if needed

# Usage example in other files:
# handler = PartialResultsHandler(on_partial=print_partial, on_final=print_final)
# live.registerHandler(LiveTranscriptionEvents.Transcript, handler.handle_transcript)