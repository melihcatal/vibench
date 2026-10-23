import os
import asyncio
import pyaudio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig


class MicrophoneStreamCallback(RecognizeCallback):
    def __init__(self, yield_interim=True):
        super().__init__()
        self.yield_interim = yield_interim
        self.transcript_buffer = []
        self.final_transcript = None
        self.lock = asyncio.Lock()

    def on_transcription(self, transcript):
        if self.yield_interim:
            self.transcript_buffer.extend(transcript)

    def on_connected(self):
        pass

    def on_error(self, error):
        print(f"Error: {error}")

    def on_inactivity_timeout(self, error):
        print(f"Inactivity timeout: {error}")

    def on_transcription_complete(self):
        self.final_transcript = " ".join(self.transcript_buffer)
        self.transcript_buffer = []

    async def get_interim_transcript(self):
        async with self.lock:
            if self.transcript_buffer:
                return " ".join(self.transcript_buffer)
            return ""

    async def get_final_transcript(self):
        async with self.lock:
            if self.final_transcript:
                transcript = self.final_transcript
                self.final_transcript = None
                return transcript
            return None


async def stream_microphone():
    authenticator = IAMAuthenticator(os.getenv("IBM_STT_APIKEY"))
    speech_client = SpeechToTextV1(authenticator=authenticator)
    speech_client.set_service_url(os.getenv("IBM_STT_URL"))

    config = StreamingRecognitionConfig(
        model="en-US_Multimedia",
        interim_results=True,
        content_type="audio/l16; rate=44100",
    )

    callback = MicrophoneStreamCallback(yield_interim=True)
    audio_source = AudioSource()

    def audio_callback(in_data, frame_count, time_info, status):
        audio_source.send(in_data)
        return (in_data, pyaudio.paContinue)

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
        stream_callback=audio_callback,
    )

    stream.start_stream()
    speech_client.recognize_using_websocket(
        audio=audio_source,
        content_type=config.content_type,
        recognize_callback=callback,
        model=config.model,
        interim_results=config.interim_results,
    )

    try:
        while True:
            interim = await callback.get_interim_transcript()
            if interim:
                yield {"type": "interim", "text": interim}
            final = await callback.get_final_transcript()
            if final:
                yield {"type": "final", "text": final}
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        audio_source.completed()
