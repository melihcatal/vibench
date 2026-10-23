import os
import google.cloud.speech_v1 as speech

# Credentials are picked up from environment variable GOOGLE_APPLICATION_CREDENTIALS
client = speech.SpeechClient()


def transcribe_audio(audio_bytes: bytes, language_code: str = "en-US") -> str:
    """
    Transcribes raw audio bytes to plaintext using Google Cloud Speech‑to‑Text.

    Args:
        audio_bytes (bytes): Binary audio data (e.g., MP3, WAV).
        language_code (str): BCP-47 language tag (default "en-US").

    Returns:
        str: The transcribed text.
    """
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript
    return transcript


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     with open("sample.mp3", "rb") as f:
#         audio_data = f.read()
#     print(transcribe_audio(audio_data))
