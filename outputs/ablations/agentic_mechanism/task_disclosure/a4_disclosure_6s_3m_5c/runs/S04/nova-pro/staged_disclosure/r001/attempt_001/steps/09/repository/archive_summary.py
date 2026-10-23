import boto3

def summarize_transcription_results(transcription_job_name):
    transcribe = boto3.client('transcribe')
    response = transcribe.get_transcription_job(TranscriptionJobName=transcription_job_name)
    if response['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        print(f'Transcription job {transcription_job_name} completed. Transcript URI: {transcript_uri}')
    else:
        print(f'Transcription job {transcription_job_name} is not completed.')