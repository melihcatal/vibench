import asyncio
import azure.cognitiveservices.speech as azurespeech
from typing import AsyncGenerator

from speech_client import get_azure_speech_recognizer
from speech_models import TranscriptResult

async def handle_azure_speech_events(
    language: str = "en-US"
) -> AsyncGenerator[TranscriptResult, None]:
    """
    Initializes an Azure SpeechRecognizer and handles its partial and final
    streaming recognition events, yielding TranscriptResult objects.
    """
    speech_recognizer = get_azure_speech_recognizer(language) # Azure Speech SDK is a provider-identifying signal

    # Event handler for recognizing (partial) results
    def recognized_cb(evt: azurespeech.SpeechRecognitionEventArgs):
        if evt.result.reason == azurespeech.ResultReason.RecognizingSpeech:
            asyncio.create_task(yield_transcript_result(evt.result.text, True))
        elif evt.result.reason == azurespeech.ResultReason.RecognizedSpeech:
            asyncio.create_task(yield_transcript_result(evt.result.text, False, evt.result.confidence))

    # Event handler for session stopped
    def session_stopped_cb(evt: azurespeech.SessionEventArgs):
        print(f"Session stopped: {evt}")
        # Signal the end of the stream if necessary

    # Helper to yield from an async generator within a sync callback
    # This is a common pattern for bridging sync event handlers with async generators.
    _transcript_queue = asyncio.Queue()

    async def yield_transcript_result(text: str, is_partial: bool, confidence: float = None):
        await _transcript_queue.put(TranscriptResult(text=text, is_partial=is_partial, confidence=confidence))

    speech_recognizer.recognizing.connect(recognized_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_stopped.connect(session_stopped_cb)
    speech_recognizer.canceled.connect(session_stopped_cb) # Canceled also signals a stop

    print("Starting Azure Speech Recognition...")
    # Note: In a real application, you'd start continuous recognition
    # and manage the lifecycle. For this example, we demonstrate the event handling.
    speech_recognizer.start_continuous_recognition_async().get()

    try:
        while True:
            # This loop will run indefinitely, yielding results as they come in.
            # In a production scenario, you would have a mechanism to stop this loop.
            transcript_result = await _transcript_queue.get()
            yield transcript_result
    except asyncio.CancelledError:
        print("Azure Speech Recognition task cancelled.")
    finally:
        speech_recognizer.stop_continuous_recognition_async().get()
        print("Azure Speech Recognition stopped.")

if __name__ == "__main__":
    async def main():
        print("Starting Azure Speech event handler...")
        async for transcript_result in handle_azure_speech_events():
            status = "(Partial)" if transcript_result.is_partial else "(Final)"
            print(f"Azure Transcript {status}: {transcript_result.text}")
    asyncio.run(main())
