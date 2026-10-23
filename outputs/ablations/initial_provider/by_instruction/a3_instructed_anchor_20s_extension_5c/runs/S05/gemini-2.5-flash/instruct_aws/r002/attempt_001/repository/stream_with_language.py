
import asyncio
import os
import azure.cognitiveservices.speech as speechsdk

# Azure Speech Service settings
AZURE_SPEECH_KEY = os.environ.get("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.environ.get("AZURE_SPEECH_REGION", "westus2")

async def stream_with_language(audio_chunks_source, language_code="en-US", enable_punctuation=True):
    """
    Starts a streaming recognizer with language and punctuation settings using Azure Speech Service.
    """
    if not AZURE_SPEECH_KEY:
        raise ValueError("AZURE_SPEECH_KEY environment variable not set.")

    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    speech_config.speech_recognition_language = language_code
    
    # Enable punctuation if required
    if enable_punctuation:
        speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption,
            "True Text"
        )

    # Create an audio config that streams from memory (or a simulated input)
    # For actual microphone, you'd use `AudioConfig(use_microphone=True)` or `PushAudioInputStream`
    # Here, we'll simulate a `PushAudioInputStream`
    push_stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=push_stream)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Event handlers
    transcript_queue = asyncio.Queue()

    def recognized_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            asyncio.create_task(transcript_queue.put(evt.result.text))
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            asyncio.create_task(transcript_queue.put("[No Match]"))

    def recognizing_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
            asyncio.create_task(transcript_queue.put(f"[Interim] {evt.result.text}"))

    def canceled_cb(evt):
        print(f"Cancellation: {evt.reason}")
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {evt.error_details}")
        asyncio.create_task(transcript_queue.put("[Canceled]"))

    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.canceled.connect(canceled_cb)

    speech_recognition_started = asyncio.Event()

    def session_started_cb(evt):
        speech_recognition_started.set()

    speech_recognizer.session_started.connect(session_started_cb)

    # Start continuous recognition
    speech_recognizer.start_continuous_recognition_async()

    # Wait for the session to start
    await speech_recognition_started.wait()

    # Feed audio chunks to the push stream
    audio_feed_task = asyncio.create_task(
        _feed_audio_to_azure_stream(audio_chunks_source, push_stream)
    )

    try:
        while True:
            transcript = await transcript_queue.get()
            if transcript == "[Canceled]":
                break
            yield transcript
    finally:
        speech_recognizer.stop_continuous_recognition_async().get()
        push_stream.close()
        audio_feed_task.cancel()
        await asyncio.gather(audio_feed_task, return_exceptions=True) # Ensure cancellation is propagated

async def _feed_audio_to_azure_stream(audio_chunks_source, push_stream):
    """Helper to feed audio chunks into Azure's PushAudioInputStream."""
    try:
        async for chunk in audio_chunks_source:
            push_stream.write(chunk)
    except asyncio.CancelledError:
        print("Audio feeding to Azure stream cancelled.")
    except Exception as e:
        print(f"Error feeding audio to Azure stream: {e}")
