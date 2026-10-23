from safety_client import get_comprehend_client
from safety_models import SafetyRequest, SafetyResponse, normalize_response

def reviewer_brief_audio(text):
    client = get_comprehend_client()
    request = SafetyRequest(text)
    response = client.start_speech_synthesis_task(OutputFormat='mp3', VoiceId='Joanna', Text=request.text)
    return response['SynthesisTask']['OutputUri']