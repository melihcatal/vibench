from typing import Dict, List

class SpeechRecognitionResult:
    def __init__(self, response: Dict):
        self.response = response
        self.is_final = response.get('results', [])[-1].get('is_final', False)
        self.transcript = ''.join(r.get('alternatives', [{}])[0].get('transcript', '')
                                  for r in response['results'])
        self.confidence = response['results'][-1]['alternatives'][0].get('confidence', 0.0)

    def __repr__(self):
        return f"<SpeechRecognitionResult is_final={self.is_final} transcript='{self.transcript[:30]}...' confidence={self.confidence:.2f}>"

def handle_partial_results(recognizer, event_handler):
    """
    Subscribes to streaming recognizer events and dispatches interim and final outputs.

    Args:
        recognizer: streaming recognizer client with an 'on_partial_result' callback.
        event_handler: callable(transcript: str, is_final: bool, confidence: float)
    """
    def on_result(result_event):
        data = result_event.result
        # In many SDKs the event contains interim results and a final flag.
        is_final = data.get('is_final')
        transcript = data.get('transcript', '')
        confidence = data.get('confidence', 0.0)
        event_handler(transcript, is_final, confidence)

    recognizer.on_partial_result = on_result

# Example usage stub demonstrating how a caller would register a handler.
# def my_handler(txt, final, conf):
#     print(f"{txt} ({'FINAL' if final else 'INTERIM'}, conf={conf})")
# recognizer = build_recognizer()   # uses a concrete provider SDK
# handle_partial_results(recognizer, my_handler)
# recognizer.start()