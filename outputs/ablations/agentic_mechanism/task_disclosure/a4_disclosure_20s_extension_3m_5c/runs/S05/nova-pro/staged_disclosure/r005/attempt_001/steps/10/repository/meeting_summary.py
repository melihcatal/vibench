import boto3

transcribe = boto3.client('transcribe')

def summarize_transcript(transcript):
    response = transcribe.start_transcription_job(
        TranscriptionJobName='MeetingSummary',
        LanguageCode='en-US',
        Media={'MediaFileUri': transcript},
        OutputBucketName='meeting-summaries'
    )
    return response['TranscriptionJob']['TranscriptionJobName']

if __name__ == '__main__':\n    transcript_chunk = 'path_to_transcript_chunk'
    job_name = summarize_transcript(transcript_chunk)
    print(f'Transcription job {job_name} started.')