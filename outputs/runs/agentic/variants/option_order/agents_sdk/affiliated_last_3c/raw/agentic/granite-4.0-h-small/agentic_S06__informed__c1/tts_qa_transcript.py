import os
import google.cloud.speech_v1 as speech

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "service_key.json")

def transcribe_audio(audio_bytes: bytes, language_code: str = "en-US") -> str:
    """Transcribe synthesized speech to text using Google Cloud Speech-to-Text.

    Args:
        audio_bytes (bytes): Raw audio data from a TTS call.
        language_code (str): BCP-47 language code for the expected language.

    Returns:
        str: Recognized transcription.
    """
    client = speech.SpeechClient.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    transcript = "\n".join(result.alternatives[0].transcript for result in response.results)
    return transcript

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     # Assume `audio` is bytes returned from synthesize_text
#     trans = transcribe_audio(audio)
#     print("Transcription:", trans)
