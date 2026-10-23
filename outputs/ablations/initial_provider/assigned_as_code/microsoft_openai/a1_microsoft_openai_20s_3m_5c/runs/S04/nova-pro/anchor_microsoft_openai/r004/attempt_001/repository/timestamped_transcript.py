import boto3


def timestamped_transcript(job_id, config=None):
    config = config or {}
    transcribe_client = boto3.client('transcribe', region_name=config['region'], aws_access_key_id=config.get('api_key') or os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=config.get('secret_key') or os.environ['AWS_SECRET_ACCESS_KEY'])
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_id)
    transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    with open('transcript.json', 'w') as f:
        f.write(transcript_uri)
    return {'transcript_uri': transcript_uri}