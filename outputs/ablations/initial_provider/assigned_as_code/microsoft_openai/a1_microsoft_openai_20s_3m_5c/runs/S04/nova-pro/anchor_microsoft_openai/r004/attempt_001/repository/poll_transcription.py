import boto3


def poll_transcription(job_id, config=None):
    config = config or {}
    transcribe_client = boto3.client('transcribe', region_name=config['region'], aws_access_key_id=config.get('api_key') or os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=config.get('secret_key') or os.environ['AWS_SECRET_ACCESS_KEY'])
    while True:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_id)
        job_status = response['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            break
    return {'status': job_status, 'transcript': response['TranscriptionJob']['Transcript']['TranscriptFileUri'] if job_status == 'COMPLETED' else None}