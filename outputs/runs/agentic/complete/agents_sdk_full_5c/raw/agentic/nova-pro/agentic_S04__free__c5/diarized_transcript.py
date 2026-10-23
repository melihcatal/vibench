import boto3

transcribe = boto3.client('transcribe')

def diarized_transcript(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    # Additional logic to parse and diarize the transcript
    return transcript_uri