from google.cloud.speech_v1p1beta1 import types

def handle_partial_results(response):
    partial_transcripts = []
    for result in response.results:
        if result.is_final:
            transcript = result.alternatives[0].transcript
            confidence = result.alternatives[0].confidence
            yield {"type": "final", "text": transcript, "confidence": confidence}
        else:
            transcript = result.alternatives[0].transcript
            yield {"type": "partial", "text": transcript}

async def process_streaming_results(stream):
    async for response in stream:
        for result in handle_partial_results(response):
            yield result