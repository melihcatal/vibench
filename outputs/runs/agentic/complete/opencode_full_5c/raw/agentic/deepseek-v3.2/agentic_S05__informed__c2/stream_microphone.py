import azure.cognitiveservices.speech as speechsdk
import pyaudio
import threading
import queue
import time
import os


class MicrophoneStreamer:
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
        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=self.audio_config
        )

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

    def start_streaming(self):
        self.is_streaming = True

        self.recognizer.recognizing.connect(self._recognizing_callback)
        self.recognizer.recognized.connect(self._recognized_callback)

        self.recognizer.start_continuous_recognition_async()

        def monitor_stream():
            while self.is_streaming:
                time.sleep(0.1)

        monitor_thread = threading.Thread(target=monitor_stream)
        monitor_thread.daemon = True
        monitor_thread.start()

    def stop_streaming(self):
        self.is_streaming = False
        self.recognizer.stop_continuous_recognition_async()

    def get_transcripts(self):
        while True:
            try:
                yield self.result_queue.get(timeout=0.1)
            except queue.Empty:
                if not self.is_streaming:
                    break
                continue

    def stream_microphone(self):
        self.start_streaming()
        try:
            for transcript in self.get_transcripts():
                yield transcript
        finally:
            self.stop_streaming()
