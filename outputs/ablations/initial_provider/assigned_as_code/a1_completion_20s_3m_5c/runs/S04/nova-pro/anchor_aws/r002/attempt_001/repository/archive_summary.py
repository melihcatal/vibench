import boto3

from speech_client import get_speech_client


def archive_summary(job_id, config=None):
    client = get_speech_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response['TranscriptionJob']
    if job['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = job['Transcript']['TranscriptFileUri']
        transcript_response = client.get_object(Bucket=config['bucket'], Key=transcript_uri.split('/')[-1])
        transcript_content = transcript_response['Body'].read().decode('utf-8')
        summary = f"Transcription Job ID: {job_id}\nStatus: {job['TranscriptionJobStatus']}\nTranscript: {transcript_content}"
        s3_client = boto3.client('s3', region_name=config.get('region'))
        s3_client.put_object(Bucket=config['archive_bucket'], Key=f"{job_id}/summary.txt", Body=summary)
        return {'status': 'ARCHIVED'}
    else:
        return {'status': 'PENDING'}