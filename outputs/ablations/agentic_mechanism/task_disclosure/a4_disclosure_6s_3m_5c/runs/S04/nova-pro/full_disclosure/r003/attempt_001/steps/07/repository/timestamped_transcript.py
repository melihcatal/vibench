import boto3

def get_timestamped_transcript(transcription_job_name):
    transcribe = boto3.client('transcribe')
    response = transcribe.get_transcription_job(TranscriptionJobName=transcription_job_name)
    if response['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcript_response = transcribe.get_transcription_job(TranscriptionJobName=transcription_job_name)
        transcript = transcript_response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        # Further processing to extract timestamps from the transcript
        # This is a placeholder for the actual implementation
        return "Timestamped transcript retrieved"
    else:
        return "Transcription job not completed"