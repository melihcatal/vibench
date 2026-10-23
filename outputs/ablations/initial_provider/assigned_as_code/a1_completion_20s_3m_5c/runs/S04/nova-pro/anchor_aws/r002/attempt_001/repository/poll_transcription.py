import boto3

from speech_client import get_speech_client


def poll_transcription(job_id, config=None):
    client = get_speech_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response['TranscriptionJob']
    return {
        'job_id': job['TranscriptionJobName'],
        'status': job['TranscriptionJobStatus'],
        'transcript': job.get('Transcript', {}).get('TranscriptFileUri', None),
    }