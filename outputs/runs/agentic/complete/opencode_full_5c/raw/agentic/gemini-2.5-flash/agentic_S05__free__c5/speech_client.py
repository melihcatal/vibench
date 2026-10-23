import os
import asyncio
from google.cloud import speech
from google.api_core.exceptions import GoogleAPIError


class SpeechClient:
    def __init__(self):
        self.client = speech.SpeechClient()

    async def stream_audio_to_text(self, audio_generator, config_params):
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding[config_params.encoding],
            sample_rate_hertz=config_params.sample_rate_hertz,
            language_code=config_params.language_code,
            enable_automatic_punctuation=config_params.enable_automatic_punctuation,
        )
        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=config_params.interim_results,
        )

        async def request_generator():
            async for chunk in audio_generator:
                yield speech.StreamingRecognizeRequest(audio_content=chunk)

        try:
            responses = self.client.streaming_recognize(
                config=streaming_config, requests=request_generator()
            )
            async for response in responses:
                yield response
        except GoogleAPIError as e:
            print(f"Google Cloud Speech-to-Text API Error: {e}")
            raise
