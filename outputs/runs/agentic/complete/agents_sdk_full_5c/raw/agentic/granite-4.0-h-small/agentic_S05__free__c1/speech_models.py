from typing import List, Dict

# Provider: Google Cloud Speech-to-Text (hosted API: speech.googleapis.com)
# This helper module defines request/response wrappers and normalizes output.

# Define a simple wrapper for a recognition result.
class RecognitionResult:
    def __init__(self, response: dict):
        # Expect the raw API payload.
        self.raw = response
        self.is_final = response.get('results', [])[-1].get('is_final', False)
        self.transcript = ''.join(r.get('alternatives', [{}])[0].get('transcript', '')
                                  for r in response['results'])
        self.confidence = response['results'][-1]['alternatives'][0].get('confidence', 0.0)
        # If word_time_offsets enabled, parse them.
        self.word_offsets: List[Dict] = []
        if response['results'][-1].get('alternatives', [{}])[0].get('words', []):
            for word in response['results'][-1]['alternatives'][0]['words']:
                self.word_offsets.append({
                    'word': word['word'],
                    'start_time': word.get('start_time'),
                    'end_time': word.get('end_time'),
                })

    def __repr__(self):
        return f"<RecognitionResult is_final={self.is_final} text='{self.transcript}' confidence={self.confidence}>"

def normalize_streaming_response(resp_list: List[dict]) -> List[RecognitionResult]:
    """Convert raw list of API responses into standardized RecognitionResult objects."""
    return [RecognitionResult(r) for r in resp_list]

# Example helper to retrieve word alignment info if available.
def get_word_alignment(results: List[RecognitionResult]) -> List[List[Dict]]:
    """
    Returns a list of lists, each inner list containing word offset dicts for a final result.
    """
    return [result.word_offsets for result in results if result.is_final]

# Example usage (placeholder)
# def demo():
#     raw = [{'results': []}]  # dummy
#     results = normalize_streaming_response(raw)
#     for r in results:
#         print(r)
# demo()