import boto3

def summarize_transcription_results(transcription_job_name):
    transcribe = boto3.client('transcribe')
    response = transcribe.get_transcription_job(TranscriptionJobName=transcription_job_name)
    if response['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        # Further processing to summarize the transcript can be added here
        return 'Transcription job completed and transcript is available at: ' + transcript_uri
    else:
        return 'Transcription job is not completed yet.'