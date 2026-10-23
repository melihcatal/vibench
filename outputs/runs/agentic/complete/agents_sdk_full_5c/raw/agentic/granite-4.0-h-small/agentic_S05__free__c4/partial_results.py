from google.cloud.speech_v1p1beta1.types import StreamingRecognizeResult, SpeechRecognitionResult

def handle_partial_results(result_iter):
    """
    Generator that yields text as soon as intermediate results are available.
    Emits a tuple (transcript, is_final).
    """
    for response in result_iter:
        if not response.results:
            continue
        # The first alternative is usually the best guess
        best_alternative = response.results[0].alternatives[0]
        yield best_alternative.transcript, response.results[0].is_final

async def process_live_transcript(recognize_stream):
    """
    Consumes a StreamingRecognize streaming iterator and prints each partial/final chunk.
    """
    async for res in recognize_stream:
        for transcript, is_final in handle_partial_results(iter([res])):
            print(f"{'INTERIM' if not is_final else 'FINAL'}: {transcript}")

# Example integration (to be used together with stream_microphone or stream_chunks):
# result_stream = client.streaming_recognize(...)
# await process_live_transcript(result_stream)
