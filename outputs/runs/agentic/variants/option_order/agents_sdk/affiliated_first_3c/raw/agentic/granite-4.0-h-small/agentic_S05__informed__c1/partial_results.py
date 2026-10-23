import json
class PartialResultsHandler:
    def __init__(self):
        self.partial_transcripts = []

    def handle(self, event):
        """Expect event to be the JSON payload from the streaming recognizer
        (Google, Watson, etc.). This method extracts interim and final
        transcript fragments and stores them."""
        try:
            data = json.loads(event)
        except json.JSONDecodeError:
            return
        results = data.get('results')
        if not results:
            return
        for r in results:
            alts = r.get('alternatives')
            if not alts:
                continue
            txt = alts[0].get('transcript','')
            final = r.get('final', False)
            self.partial_transcripts.append({'text': txt, 'final': final})

    def get_transcript(self):
        """Return the best-effort assembled transcript (interleaved order)."""
        assembled = []
        for frag in self.partial_transcripts:
            if frag['final']:
                assembled.append(frag['text'])
        return ''.join(assembled)

if __name__ == '__main__':
    handler = PartialResultsHandler()
    # Simulate receiving a JSON event; replace with real stream handling
    sample_event = json.dumps({
        'results': [
            {'alternatives': [{'transcript': 'Hello'}, {'transcript': 'World'}], 'final': False},
            {'alternatives': [{'transcript': ' from AI.'}], 'final': True}
        ]
    })
    handler.handle(sample_event)
    print('Combined transcript:', handler.get_transcript())
