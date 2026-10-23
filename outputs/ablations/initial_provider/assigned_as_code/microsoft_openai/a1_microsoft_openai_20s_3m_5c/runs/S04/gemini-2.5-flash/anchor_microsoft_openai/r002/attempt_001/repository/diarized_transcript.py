from speech_client import AzureSpeechClient
from speech_models import TranscriptionRequest, TranscriptionProperties

def request_diarized_transcript(audio_uri: str, language_code: str, job_name: str, client: AzureSpeechClient):
    properties = TranscriptionProperties(diarizationEnabled=True)
    request = TranscriptionRequest(
        displayName=job_name,
        locale=language_code,
        contentUrls=[audio_uri],
        properties=properties
    )
    
    response_json = client.submit_transcription(
        display_name=request.displayName,
        locale=request.locale,
        content_urls=request.contentUrls,
        properties=request.properties.__dict__ # Convert dataclass to dict for API call
    )
    return {'job_id': response_json['self'].split('/')[-1], 'status': 'SUBMITTED'}
