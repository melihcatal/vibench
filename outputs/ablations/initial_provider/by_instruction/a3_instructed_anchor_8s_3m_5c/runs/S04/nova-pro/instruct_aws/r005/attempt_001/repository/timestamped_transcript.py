import boto3

def get_timestamps(job_name):
    client = boto3.client('transcribe')
    
    status = client.get_transcription_job(TranscriptionJobName=job_name)
    transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    
    transcript = client.get_object(Bucket='your-bucket', Key=transcript_uri.split('/')[-1])['Body'].read().decode('utf-8')
    
    import json
    transcript_data = json.loads(transcript)
    
    return transcript_data['results']['items']