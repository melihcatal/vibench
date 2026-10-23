import os
from google.cloud import speech


def handle_streaming_transcripts(responses):
    for response in responses:
        for result in response.results:
            if result.is_final:
                yield {"type": "final", "transcript": result.alternatives[0].transcript}
            else:
                yield {
                    "type": "partial",
                    "transcript": result.alternatives[0].transcript,
                }
