import speech_recognition as sr
import speech_client


def transcribe_qa_audio(audio_bytes: bytes) -> str:
    """Transcribe synthesized QA samples to text using Google Cloud Speech-to-Text.

    Args:
        audio_bytes (bytes): Audio data to transcribe.

    Returns:
        str: Recognized transcript.
    """
    recognizer = sr.Recognizer()
    # Use provided audio bytes as file-like object
    with sr.AudioFile(bytesio.BytesIO(audio_bytes)) as audio_file:
        audio = recognizer.record(audio_file)
    try:
        transcript = recognizer.recognize_google_cloud(audio)
    except sr.UnknownValueError:
        transcript = ""
    except sr.RequestError as e:
        transcript = f"Recognition error: {e}"
    return transcript
