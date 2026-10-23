import boto3

transcribe = boto3.client('transcribe')

def request_diarization(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    transcript = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    # Additional logic to process transcript for diarization
    return transcript