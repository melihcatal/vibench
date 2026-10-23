import boto3

transcribe = boto3.client('transcribe')

def timestamped_transcript(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    with open('transcript.json', 'w') as f:
        f.write(transcript_uri)
    return transcript_uri