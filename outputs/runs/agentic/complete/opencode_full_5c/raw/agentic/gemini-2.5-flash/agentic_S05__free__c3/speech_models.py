import collections


class ResponseParser:
    """Helper for parsing Google Cloud Speech-to-Text streaming responses."""

    def __init__(self):
        self.buff = collections.deque()

    def parse(self, responses):
        """Parses streaming responses and yields interim and final transcripts."""
        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript

            if result.is_final:
                yield {"type": "final", "transcript": transcript}
                self.buff.clear()
            else:
                self.buff.append(transcript)
                # Just return the last interim transcript for simplicity
                yield {"type": "interim", "transcript": transcript}
