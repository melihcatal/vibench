from speech_client import transcribe_client
from speech_models import TranscriptionRequest


def submit_transcription(file_uri, job_name):
    request = TranscriptionRequest(file_uri, job_name)
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=request.job_name,
        LanguageCode=request.language_code,
        Media={"MediaFileUri": request.file_uri},
        MediaFormat="mp3",
        OutputBucketName="your-output-bucket",
    )
    return response
