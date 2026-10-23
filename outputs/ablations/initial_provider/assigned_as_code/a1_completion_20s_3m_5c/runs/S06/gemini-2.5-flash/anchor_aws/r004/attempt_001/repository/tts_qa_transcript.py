import time
from speech_client import get_transcribe_client


def tts_qa_transcript(job_name, audio_file_uri, language_code="en-US", config=None):
    config = config or {}
    client = get_transcribe_client(region_name=config.get("region"))
    
    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_file_uri},
        MediaFormat='mp3',  # Assuming mp3 for synthesized audio
        LanguageCode=language_code
    )

    # In a real scenario, you'd poll the job status or use notifications
    # For this example, we'll return the job name and assume it will complete asynchronously
    return {"transcription_job_name": response["TranscriptionJob"]["TranscriptionJobName"],
            "job_status": response["TranscriptionJob"]["TranscriptionJobStatus"]}
