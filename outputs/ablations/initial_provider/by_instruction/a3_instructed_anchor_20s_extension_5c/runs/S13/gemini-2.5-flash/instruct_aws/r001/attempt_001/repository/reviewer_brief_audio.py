from safety_client import GoogleCloudClient
from safety_models import ReviewerBriefAudioRequest, ReviewerBriefAudioResponse

def generate_reviewer_brief_audio(request: ReviewerBriefAudioRequest) -> ReviewerBriefAudioResponse:
    client = GoogleCloudClient()
    audio_content = client.synthesize_speech(request.text)
    return ReviewerBriefAudioResponse(audio_content=audio_content)
