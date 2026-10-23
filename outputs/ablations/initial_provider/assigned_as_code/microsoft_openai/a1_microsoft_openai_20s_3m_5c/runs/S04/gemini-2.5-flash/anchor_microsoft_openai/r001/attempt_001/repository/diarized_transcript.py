from speech_client import AzureSpeechClient
from speech_models import TranscriptionPayload, TranscriptionConfig, TranscriptionJob

def diarized_transcript(payload: TranscriptionPayload, config: TranscriptionConfig = None):
    config = config or TranscriptionConfig()
    client = AzureSpeechClient(config)

    properties = {
        "diarizationEnabled": True,
    }

    response_json = client.submit_transcription_job(
        display_name=payload.display_name,
        locale=payload.language_code,
        content_urls=[payload.audio_uri],
        properties=properties
    )

    job_id = response_json['self']
    status = response_json['status']
    return TranscriptionJob(job_id=job_id, status=status)
