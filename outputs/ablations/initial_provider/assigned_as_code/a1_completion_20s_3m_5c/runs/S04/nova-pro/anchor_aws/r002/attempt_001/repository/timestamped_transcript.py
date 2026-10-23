import boto3

from speech_client import get_speech_client


def timestamped_transcript(job_id, config=None):
    client = get_speech_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response['TranscriptionJob']
    if job['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = job['Transcript']['TranscriptFileUri']
        transcript_response = client.get_object(Bucket=config['bucket'], Key=transcript_uri.split('/')[-1])
        transcript_content = transcript_response['Body'].read().decode('utf-8')
        transcript_data = json.loads(transcript_content)
        items = transcript_data['results']['items']
        timestamps = {}
        for item in items:
            if 'start_time' in item and 'end_time' in item:
                timestamps[item['alternatives'][0]['content']] = {
                    'start_time': item['start_time'],
                    'end_time': item['end_time'],
                }
        return timestamps
    else:
        return {'status': 'PENDING'}