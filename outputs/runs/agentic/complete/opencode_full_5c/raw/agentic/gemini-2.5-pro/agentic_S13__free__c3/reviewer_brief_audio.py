from safety_client import get_openai_client
from safety_models import ReviewerBriefAudioRequest, ReviewerBriefAudioResponse


def generate_reviewer_brief_audio(
    request: ReviewerBriefAudioRequest,
) -> ReviewerBriefAudioResponse:
    client = get_openai_client()
    response = client.audio.speech.create(
        model="tts-1", voice="alloy", input=request.brief_text
    )
    return ReviewerBriefAudioResponse(audio_content=response.content)
