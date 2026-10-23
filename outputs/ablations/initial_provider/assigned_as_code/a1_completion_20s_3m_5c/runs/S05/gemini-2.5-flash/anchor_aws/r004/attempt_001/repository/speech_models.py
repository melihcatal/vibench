class TranscriptResult:
    def __init__(self, text, is_final):
        self.text = text
        self.is_final = is_final

def normalize_transcribe_output(transcribe_event):
    results = []
    for result in transcribe_event.transcript.results:
        if result.alternatives:
            results.append(TranscriptResult(result.alternatives[0].transcript, not result.is_partial))
    return results
