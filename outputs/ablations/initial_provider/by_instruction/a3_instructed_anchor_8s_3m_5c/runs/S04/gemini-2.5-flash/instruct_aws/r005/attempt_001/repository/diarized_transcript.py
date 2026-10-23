import boto3
from speech_client import get_transcribe_client
from speech_models import TranscriptionJobRequest

def submit_diarized_transcription_job(job_request: TranscriptionJobRequest) -> dict:
    transcribe_client = get_transcribe_client()
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_request.job_name,
        MediaFormat=job_request.media_format,
        Media={'MediaFileUri': job_request.audio_file_uri},
        LanguageCode=job_request.language_code,
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 10  # Adjust as needed, max 10 for standard diarization
        }
    )
    return response['TranscriptionJob']

if __name__ == '__main__':
    example_request = TranscriptionJobRequest(
        job_name="my-diarized-transcription-job-1",
        audio_file_uri="s3://your-s3-bucket/your-meeting-audio.wav",
        media_format="wav",
        language_code="en-US"
    )
    try:
        job_info = submit_diarized_transcription_job(example_request)
        print(f"Diarized transcription job submitted: {job_info['TranscriptionJobStatus']} - {job_info['TranscriptionJobName']}")
        print(f"Job ARN: {job_info['TranscriptionJobArn']}")
    except Exception as e:
        print(f"Error submitting diarized transcription job: {e}")
