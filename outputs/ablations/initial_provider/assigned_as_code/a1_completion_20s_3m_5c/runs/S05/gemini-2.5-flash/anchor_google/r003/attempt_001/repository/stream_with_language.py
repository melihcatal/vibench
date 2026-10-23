from speech_client import SpeechClient
from speech_models import SpeechRecognitionConfig, StreamingRecognitionResult

async def stream_with_language_and_punctuation(
    audio_chunks_generator,
    language_code: str,
    sample_rate_hertz: int,
    enable_automatic_punctuation: bool = False
):
    speech_client_helper = SpeechClient()

    config_params = {
        "encoding": "LINEAR16", # Assuming LINEAR16 from stream_microphone.py
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "enable_automatic_punctuation": enable_automatic_punctuation
    }

    streaming_config = speech_client_helper.create_streaming_config(config_params)
    responses = speech_client_helper.stream_recognize(streaming_config, audio_chunks_generator)

    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield StreamingRecognitionResult(
                    transcript=result.alternatives[0].transcript,
                    is_final=result.is_final,
                    language_code=result.language_code, # Google Cloud Speech provides language_code in result
                    confidence=result.alternatives[0].confidence
                )
