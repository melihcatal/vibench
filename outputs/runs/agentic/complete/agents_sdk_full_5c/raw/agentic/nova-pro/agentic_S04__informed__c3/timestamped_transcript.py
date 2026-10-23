import boto3

transcribe_client = boto3.client('transcribe')

def get_timestamped_transcript(job_name):
    status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    with urllib.request.urlopen(transcript_uri) as response:
        transcript_content = response.read().decode('utf-8')
    transcript_data = json.loads(transcript_content)
    return transcript_data['results']['items']