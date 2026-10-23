import azure.cognitiveservices.speech as speechsdk
import asyncio
import queue
import threading
import os


class AudioChunkStreamer:
    def __init__(self):
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION")
        if not self.speech_key or not self.speech_region:
            raise ValueError(
                "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set"
            )

        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.speech_region
        )
        self.push_stream = speechsdk.audio.PushAudioInputStream()
        self.audio_config = speechsdk.audio.AudioConfig(stream=self.push_stream)
        self.recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=self.audio_config
        )

        self.chunk_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.is_streaming = False

    def _recognizing_callback(self, evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
            transcript = evt.result.text
            self.result_queue.put({"type": "interim", "text": transcript})

    def _recognized_callback(self, evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            transcript = evt.result.text
            self.result_queue.put({"type": "final", "text": transcript})

    async def _audio_source(self):
        while self.is_streaming:
            try:
                chunk = await asyncio.get_event_loop().run_in_executor(
                    None, self.chunk_queue.get, True, 0.1
                )
                if chunk:
                    self.push_stream.write(chunk)
            except queue.Empty:
                continue

    def start_streaming(self):
        self.is_streaming = True

        self.recognizer.recognizing.connect(self._recognizing_callback)
        self.recognizer.recognized.connect(self._recognized_callback)

        self.recognizer.start_continuous_recognition_async()

        self.audio_thread = threading.Thread(
            target=lambda: asyncio.run(self._audio_source())
        )
        self.audio_thread.daemon = True
        self.audio_thread.start()

    def stop_streaming(self):
        self.is_streaming = False
        self.recognizer.stop_continuous_recognition_async()
        if self.audio_thread:
            self.audio_thread.join(timeout=1)

    def add_audio_chunk(self, chunk):
        self.chunk_queue.put(chunk)

    def get_transcripts(self):
        while True:
            try:
                yield self.result_queue.get(timeout=0.1)
            except queue.Empty:
                if not self.is_streaming:
                    break
                continue

    async def stream_from_async_source(self, async_audio_source):
        self.start_streaming()
        try:
            async for chunk in async_audio_source:
                self.add_audio_chunk(chunk)
                for transcript in self.get_transcripts():
                    yield transcript
        finally:
            self.stop_streaming()
