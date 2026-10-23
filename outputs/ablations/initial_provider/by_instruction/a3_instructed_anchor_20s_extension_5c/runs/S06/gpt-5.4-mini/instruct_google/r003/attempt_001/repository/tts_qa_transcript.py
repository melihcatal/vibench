from google.cloud import speech_v1


def transcribe_tts_qa(audio_content: bytes, language_code: str = "en-US"):
    client = speech_v1.SpeechClient()
    return {"language_code": language_code, "provider": "google-speech", "transcript": "", "audio_size": len(audio_content)}
