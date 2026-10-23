import time
import uuid
from speech_client import get_transcribe_client

def tts_qa_transcript(payload, config=None):
    config = config or {}
    client = get_transcribe_client(region_name=config.get("region"))
    audio_uri = payload["audio_uri"]
    language_code = payload.get("language_code", "en-US")
    job_name = f"tts-qa-transcript-{uuid.uuid4()}"

    client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_uri},
        MediaFormat='mp3', # Assuming mp3 from save_audio.py
        LanguageCode=language_code
    )

    max_attempts = 10
    for attempt in range(max_attempts):
        status_response = client.get_transcription_job(TranscriptionJobName=job_name)
        status = status_response["TranscriptionJob"]["TranscriptionJobStatus"]
        if status == "COMPLETED":
            transcript_file_uri = status_response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            # In a real scenario, you'd fetch and parse the transcript content from this URI.
            # For simplicity, we return the URI for now.
            return {"transcript": f"Transcription job completed. Transcript available at: {transcript_file_file_uri}"}
        elif status == "FAILED":
            raise Exception(f"Transcription job failed: {status_response}")
        time.sleep(5) # Wait 5 seconds before checking again

    raise Exception("Transcription job timed out")
