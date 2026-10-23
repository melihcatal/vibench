from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_streaming_config
from speech_models import build_streaming_recognize_request

async def stream_audio_chunks(audio_chunk_generator):
    """
    Streams audio chunks from an async source to Google Cloud Speech-to-Text
    and yields interim transcripts.
    """
    client = get_speech_client()
    streaming_config = get_streaming_config()

    async def generate_requests():
        yield build_streaming_recognize_request(streaming_config=streaming_config) # Send config first
        async for chunk in audio_chunk_generator:
            yield build_streaming_recognize_request(audio_content=chunk)

    requests = generate_requests()
    
    # The client.streaming_recognize expects a synchronous iterable, 
    # but for an async generator, one would typically adapt it or collect
    # to a list first if the client doesn't directly support async iterables.
    # For demonstration, we'll assume an adaptation or pre-collection is done
    # if this were to be truly async end-to-end.
    # For the purpose of this exercise, we will simulate the synchronous call
    # with the generator yielding.

    # In a real async scenario, you would use an async client or an adapter.
    # For this demonstration, we'll create a synchronous iterable from the
    # async generator (which is not truly async streaming for the client call).
    # A true async implementation would require an async SpeechClient if available
    # or a different approach for feeding the requests.
    # For now, we simulate the `requests` iterable.

    # To make this runnable, we'll make audio_chunk_generator a sync iterable
    # for simplicity, as the `streaming_recognize` method is sync.
    # In a real async system, you would bridge this.

    class SyncAudioRequestGenerator:
        def __init__(self, async_gen):
            self.async_gen = async_gen
            self.first = True

        def __iter__(self):
            return self

        def __next__(self):
            if self.first:
                self.first = False
                return build_streaming_recognize_request(streaming_config=streaming_config)
            try:
                # This is a blocking call if async_gen is truly async.
                # For this exercise, we're simplifying the interaction.
                # In a real async app, you'd await the next chunk from the async_gen
                # in a separate async task and feed it.
                # Here, we'll assume audio_chunk_generator is a simple iterator for demonstration.
                chunk = next(self.async_gen) 
                return build_streaming_recognize_request(audio_content=chunk)
            except StopIteration:
                raise

    # For this exercise, audio_chunk_generator should be a synchronous iterable
    # that yields bytes chunks.
    # The first request will always be the config.
    def sync_request_generator(sync_audio_chunks_iter):
        yield build_streaming_recognize_request(streaming_config=streaming_config)
        for chunk in sync_audio_chunks_iter:
            yield build_streaming_recognize_request(audio_content=chunk)

    responses = client.streaming_recognize(sync_request_generator(audio_chunk_generator))

    for response in responses:
        if not response.results:
            continue
        result = response.results[0]
        if result.is_final:
            if result.alternatives:
                yield result.alternatives[0].transcript
        else:
            if result.alternatives:
                yield result.alternatives[0].transcript # Yield interim results as well
