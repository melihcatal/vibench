import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config
from speech_models import StreamingRecognitionResult

def setup_partial_and_final_event_handlers(recognizer, result_queue):
    """
    Sets up event handlers for partial (recognizing) and final (recognized) speech recognition results.
    Results are put into the provided result_queue.
    """

    def recognizing_handler(e: speechsdk.SpeechRecognitionEventArgs):
        if e.result.text:
            result_queue.put(StreamingRecognitionResult(e.result.text, False).to_dict())

    def recognized_handler(e: speechsdk.SpeechRecognitionEventArgs):
        if e.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            result_queue.put(StreamingRecognitionResult(e.result.text, True).to_dict())
        elif e.result.reason == speechsdk.ResultReason.NoMatch:
            # print("NOMATCH: Speech could not be recognized.")
            pass
        elif e.result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = e.result.cancellation_details
            # print(f"CANCELED: Reason={cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                # print(f"CANCELED: ErrorDetails={cancellation_details.error_details}")
                result_queue.put(RuntimeError(f"Azure Speech Recognition Canceled: {cancellation_details.error_details}"))

    recognizer.recognizing.connect(recognizing_handler)
    recognizer.recognized.connect(recognized_handler)

def setup_session_stopped_handler(recognizer, result_queue):
    """
    Sets up event handler for session stopped events.
    """
    def session_stopped_handler(e: speechsdk.SessionEventArgs):
        # print("Session stopped event.")
        result_queue.put(None)

    recognizer.session_stopped.connect(session_stopped_handler)


# Example usage if this file were standalone, but it's meant to be imported
# from queue import Queue
# if __name__ == "__main__":
#     speech_config = get_speech_config()
#     audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
#     recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
#     
#     q = Queue()
#     setup_partial_and_final_event_handlers(recognizer, q)
#     setup_session_stopped_handler(recognizer, q)
# 
#     print("Speak into your microphone.")
#     recognizer.start_continuous_recognition_async().get()
# 
#     try:
#         while True:
#             event = q.get(timeout=60)
#             if event is None:
#                 break
#             if isinstance(event, Exception):
#                 raise event
#             print(f"Recognition event: {event}")
#     finally:
#         recognizer.stop_continuous_recognition_async().get()
#         print("Stopping continuous recognition.")
