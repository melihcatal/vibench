class PartialResult:
    def __init__(self, text, is_final):
        self.text = text
        self.is_final = is_final

def handle_partial_results(event):
    results = []
    for result in event.transcript.results:
        results.append(PartialResult(result.alternatives[0].transcript, not result.is_partial))
    return results