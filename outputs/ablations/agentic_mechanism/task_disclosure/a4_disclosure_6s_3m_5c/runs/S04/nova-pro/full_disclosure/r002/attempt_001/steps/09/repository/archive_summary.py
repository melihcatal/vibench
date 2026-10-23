import boto3

def summarize_transcription_results(transcription_job_name):
    transcribe_client = boto3.client('transcribe')
    response = transcribe_client.get_transcription_job(TranscriptionJobName=transcription_job_name)
    transcription_status = response['TranscriptionJob']['TranscriptionJobStatus']
    if transcription_status == 'COMPLETED':
        transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        # Further processing to summarize the transcript can be added here
        return f'Transcription job {transcription_job_name} completed. Transcript URI: {transcript_uri}'
    else:
        return f'Transcription job {transcription_job_name} is not completed. Status: {transcription_status}'