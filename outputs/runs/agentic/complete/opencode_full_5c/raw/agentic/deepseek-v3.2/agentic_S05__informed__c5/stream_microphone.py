import asyncio
import pyaudio
from speech_client import get_speech_client


async def stream_microphone():
    """Stream microphone audio and yield interim transcripts."""
    client = get_speech_client()

    # Configure streaming recognition
    config = {
        "encoding": "LINEAR16",
        "sample_rate_hertz": 16000,
        "language_code": "en-US",
        "enable_automatic_punctuation": True,
        "interim_results": True,
    }

    # Create streaming config for Azure Speech
    speech_config = client.speech_config
    speech_config.speech_recognition_language = "en-US"
    speech_config.enable_dictation()
    speech_config.request_word_level_timestamps()

    # Create audio config for microphone
    audio_config = client.audio.AudioConfig(use_default_microphone=True)

    # Create recognizer
    recognizer = client.speech.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    print("Listening... Speak into your microphone.")

    # Start continuous recognition
    done = asyncio.Event()

    def recognized_callback(evt):
        if evt.result.reason == client.speech.ResultReason.RecognizedSpeech:
            print(f"Recognized: {evt.result.text}")
            yield evt.result.text
        elif evt.result.reason == client.speech.ResultReason.NoMatch:
            print("No speech could be recognized")

    def session_stopped_callback(evt):
        print("Session stopped.")
        done.set()

    recognizer.recognized.connect(recognized_callback)
    recognizer.session_stopped.connect(session_stopped_callback)

    # Start continuous recognition
    recognizer.start_continuous_recognition()

    try:
        await done.wait()
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        recognizer.stop_continuous_recognition()

    return


if __name__ == "__main__":
    asyncio.run(stream_microphone())
