import boto3

transcribe = boto3.client('transcribe')

def timestamped_transcript(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    # Additional logic to parse and extract timestamps from the transcript
    return transcript_uri