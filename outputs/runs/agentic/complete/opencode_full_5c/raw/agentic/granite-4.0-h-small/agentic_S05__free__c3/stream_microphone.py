import asyncio
from google.cloud import speech_v1p1beta1 as speech


class MicrophoneStream:
    def __init__(self, sample_rate_hertz=16000):
        self.sample_rate_hertz = sample_rate_hertz
        self.client = speech.SpeechClient()  # concrete GCP provider
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.sample_rate_hertz,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )
        self.recognizer = None
        self.stream = None

    async def start(self):
        # Create a streaming recognizer
        config = speech.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True,
        )
        requests = self._generate_requests()
        responses = self.client.streaming_recognize(config, requests)
        self.recognizer = self.client.streaming_recognize
        self.stream = responses
        async for response in responses:
            yield from self._handle_response(response)

    def _generate_requests(self):
        first_request = speech.StreamingRecognizeRequest(streaming_config=self.config)
        yield first_request
        while True:
            # Replace with actual microphone audio capture logic
            audio_chunk = self._get_next_audio_chunk()
            if not audio_chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=audio_chunk)

    def _get_next_audio_chunk(self):
        # Placeholder implementation – replace with real microphone capture
        yield b""

    async def _handle_response(self, response):
        for result in response.results:
            if not result.alternatives:
                continue
            transcript = result.alternatives[0].transcript
            is_final = result.is_final
            print(f"Transcript: {transcript} ('{'final' if is_final else 'interim'})")
