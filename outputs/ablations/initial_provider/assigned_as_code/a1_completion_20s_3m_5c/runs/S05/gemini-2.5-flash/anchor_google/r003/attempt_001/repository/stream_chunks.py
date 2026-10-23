from speech_client import SpeechClient
from speech_models import StreamingRecognitionResult

async def stream_chunks(audio_chunks_generator, config_params):
    speech_client_helper = SpeechClient()
    streaming_config = speech_client_helper.create_streaming_config(config_params)

    # The generator of audio chunks should be awaited if it's an async generator
    # For simplicity, assuming audio_chunks_generator is an iterable of bytes chunks here
    # In a real async scenario, this would involve async for and await calls.
    responses = speech_client_helper.stream_recognize(streaming_config, audio_chunks_generator)

    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield StreamingRecognitionResult(
                    transcript=result.alternatives[0].transcript,
                    is_final=result.is_final,
                    confidence=result.alternatives[0].confidence
                )
