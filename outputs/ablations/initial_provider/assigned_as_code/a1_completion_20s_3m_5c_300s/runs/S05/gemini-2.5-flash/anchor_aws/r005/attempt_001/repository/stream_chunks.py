import asyncio
from google.cloud import speech
from speech_client import get_speech_client, get_streaming_config
from speech_models import StreamingRecognitionResult

async def stream_chunks(audio_chunks, language_code: str, sample_rate_hertz: int):
    client = get_speech_client()
    config = get_streaming_config(language_code, sample_rate_hertz, enable_automatic_punctuation=True)
    
    # A queue to hold audio chunks before sending to the API
    audio_queue = asyncio.Queue()

    # Generator for streaming audio requests
    async def request_generator():
        # Send the configuration first
        yield speech.StreamingRecognizeRequest(streaming_config=config)
        # Then send audio chunks as they arrive in the queue
        while True:
            chunk = await audio_queue.get()
            if chunk is None:  # Sentinel value to signal end of stream
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    # Populate the queue with incoming audio chunks
    async def populate_queue():
        for chunk in audio_chunks:
            await audio_queue.put(chunk)
        await audio_queue.put(None) # Signal the end of the audio stream

    queue_task = asyncio.create_task(populate_queue())

    # Start the streaming recognition call
    responses = client.streaming_recognize(request_generator())

    try:
        async for response in responses:
            if not response.results:
                continue

            result = StreamingRecognitionResult(response)
            yield result.to_dict()
    except Exception as e:
        print(f"Error during streaming recognition: {e}")
    finally:
        queue_task.cancel()
        await asyncio.gather(queue_task, return_exceptions=True)
