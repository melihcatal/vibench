import os
import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config


def transcribe_audio_from_file(audio_file_path: str) -> str:
    speech_config = get_speech_config()
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    print("Transcribing audio from file...")
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized."
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(
            f"Speech recognition canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}"
        )
    else:
        raise Exception(f"Speech recognition failed: {result.reason}")


def transcribe_audio_from_bytes(audio_bytes: bytes) -> str:
    speech_config = get_speech_config()
    # For transcribing from an in-memory byte stream, you typically need to use
    # AudioDataStream. This example assumes a simple file-based approach for brevity
    # or a temporary file if direct byte stream recognition is complex with default SDK usage.
    # For this example, we'll demonstrate a conceptual path. In a real scenario, you might write
    # the bytes to a temporary file or use a PushAudioInputStream/PullAudioInputStream.

    # Create a PushAudioInputStream
    stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=stream)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # Feed the audio bytes to the stream
    stream.write(audio_bytes)
    stream.close()

    print("Transcribing audio from bytes...")
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized."
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(
            f"Speech recognition canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}"
        )
    else:
        raise Exception(f"Speech recognition failed: {result.reason}")


if __name__ == "__main__":
    # Example usage (requires an audio file or sample bytes)
    # To run this, ensure you have an audio file or generate one.
    os.environ["AZURE_SPEECH_KEY"] = "YOUR_SPEECH_KEY"  # Replace with actual key
    os.environ["AZURE_SPEECH_REGION"] = (
        "YOUR_SPEECH_REGION"  # Replace with actual region
    )

    # # Example with a dummy audio file path (you'd need a real one)
    # try:
    #     # Assuming an audio file exists for testing
    #     # dummy_audio_file = "path/to/your/audio.wav"
    #     # if os.path.exists(dummy_audio_file):
    #     #     transcript = transcribe_audio_from_file(dummy_audio_file)
    #     #     print(f"File Transcript: {transcript}")
    #     # else:
    #     #     print(f"Warning: Audio file not found at {dummy_audio_file}. Skipping file transcription example.")
    #
    #     # Example with dummy audio bytes (needs actual audio data to work meaningfully)
    #     dummy_audio_bytes = b"\x00\x01\x02\x03\x04\x05" # Replace with actual audio bytes
    #     if dummy_audio_bytes:
    #         transcript_from_bytes = transcribe_audio_from_bytes(dummy_audio_bytes)
    #         print(f"Bytes Transcript: {transcript_from_bytes}")
    #
    # except Exception as e:
    #     print(f"Transcription error: {e}")
    pass
