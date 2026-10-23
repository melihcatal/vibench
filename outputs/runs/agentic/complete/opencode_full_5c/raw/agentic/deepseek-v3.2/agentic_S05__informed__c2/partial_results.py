import azure.cognitiveservices.speech as speechsdk
import queue
import threading
import os


class PartialResultsHandler:
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

        self.partial_results = []
        self.final_results = []
        self.result_queue = queue.Queue()
        self.is_processing = False

    def _recognizing_callback(self, evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
            transcript = evt.result.text
            self.partial_results.append(transcript)
            self.result_queue.put(
                {
                    "type": "partial",
                    "text": transcript,
                    "result_id": evt.result.result_id,
                    "offset": evt.result.offset,
                }
            )

    def _recognized_callback(self, evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            transcript = evt.result.text
            self.final_results.append(transcript)
            self.result_queue.put(
                {
                    "type": "final",
                    "text": transcript,
                    "result_id": evt.result.result_id,
                    "offset": evt.result.offset,
                    "duration": evt.result.duration.total_seconds()
                    if evt.result.duration
                    else None,
                }
            )

    def _canceled_callback(self, evt):
        if evt.result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = evt.result.cancellation_details
            self.result_queue.put(
                {
                    "type": "error",
                    "reason": cancellation_details.reason.name,
                    "error_details": cancellation_details.error_details,
                }
            )

    def start_recognition(self):
        self.is_processing = True

        self.recognizer.recognizing.connect(self._recognizing_callback)
        self.recognizer.recognized.connect(self._recognized_callback)
        self.recognizer.canceled.connect(self._canceled_callback)

        self.recognizer.start_continuous_recognition_async()

        def monitor_results():
            while self.is_processing:
                threading.Event().wait(0.1)

        monitor_thread = threading.Thread(target=monitor_results)
        monitor_thread.daemon = True
        monitor_thread.start()

    def stop_recognition(self):
        self.is_processing = False
        self.recognizer.stop_continuous_recognition_async()

    def get_results(self):
        while True:
            try:
                yield self.result_queue.get(timeout=0.1)
            except queue.Empty:
                if not self.is_processing:
                    break
                continue

    def handle_streaming_events(self):
        self.start_recognition()
        try:
            for result in self.get_results():
                yield result
        finally:
            self.stop_recognition()

    def get_latest_partial(self):
        return self.partial_results[-1] if self.partial_results else ""

    def get_all_finals(self):
        return self.final_results.copy()

    def clear_results(self):
        self.partial_results.clear()
        self.final_results.clear()
        while not self.result_queue.empty():
            try:
                self.result_queue.get_nowait()
            except queue.Empty:
                break
