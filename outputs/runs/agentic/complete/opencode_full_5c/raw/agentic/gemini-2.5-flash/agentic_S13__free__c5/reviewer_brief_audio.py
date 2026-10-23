from safety_models import AudioBriefRequest, AudioBriefResponse
from safety_client import generate_audio_brief_with_gcp


def generate_reviewer_brief_audio(
    text: str, language_code: str = "en-US", voice_name: str = "en-US-Wavenet-D"
) -> AudioBriefResponse:
    request = AudioBriefRequest(
        text=text, language_code=language_code, voice_name=voice_name
    )
    response = generate_audio_brief_with_gcp(request)
    return response
