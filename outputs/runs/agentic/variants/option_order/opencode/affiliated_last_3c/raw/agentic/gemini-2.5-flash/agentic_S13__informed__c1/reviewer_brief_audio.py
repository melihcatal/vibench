from safety_client import GoogleTextToSpeechClient
from safety_models import AudioBriefResult


def generate_reviewer_brief_audio(
    brief_text: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-A"
) -> AudioBriefResult:
    client = GoogleTextToSpeechClient()
    audio_content = client.synthesize_speech(brief_text, language_code, voice_name)
    return AudioBriefResult(text=brief_text, audio_content=audio_content)
