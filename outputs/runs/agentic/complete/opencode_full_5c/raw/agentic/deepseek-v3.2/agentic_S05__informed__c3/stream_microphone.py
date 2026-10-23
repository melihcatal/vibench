import asyncio
import pyaudio
import wave
from azure.cognitiveservices.speech import (
    SpeechConfig,
    AudioConfig,
    SpeechRecognizer,
    ResultReason,
)
from azure.cognitiveservices.speech.audio import PushAudioInputStream
import threading
import queue


class MicrophoneStream:
    def __init__(self, rate=16000, chunk=1024):
        self.rate = rate
        self.chunk = chunk
        self._audio_queue = queue.Queue()
        self._stop_event = threading.Event()

    def start(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self._fill_buffer,
        )

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._audio_queue.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self._stop_event.is_set():
            chunk = self._audio_queue.get()
            if chunk is None:
                return
            yield chunk

    def stop(self):
        self._stop_event.set()
        if hasattr(self, "_audio_stream"):
            self._audio_stream.stop_stream()
            self._audio_stream.close()
        if hasattr(self, "_audio_interface"):
            self._audio_interface.terminate()


async def stream_microphone():
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set"
        )

    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language = "en-US"
    speech_config.enable_dictation()

    stream = MicrophoneStream()
    stream.start()

    push_stream = PushAudioInputStream()
    audio_config = AudioConfig(stream=push_stream)

    recognizer = SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    def recognized_callback(evt):
        if evt.result.reason == ResultReason.RecognizedSpeech:
            yield evt.result.text
        elif evt.result.reason == ResultReason.NoMatch:
            pass

    recognizer.recognized.connect(recognized_callback)

    def recognizing_callback(evt):
        if evt.result.reason == ResultReason.RecognizingSpeech:
            yield evt.result.text

    recognizer.recognizing.connect(recognizing_callback)

    recognizer.start_continuous_recognition()

    try:
        for audio_chunk in stream.generator():
            push_stream.write(audio_chunk)
            await asyncio.sleep(0)
    finally:
        recognizer.stop_continuous_recognition()
        stream.stop()
        push_stream.close()


if __name__ == "__main__":
    import os

    async def main():
        async for transcript in stream_microphone():
            if transcript:
                print(f"Transcript: {transcript}")

    asyncio.run(main())
