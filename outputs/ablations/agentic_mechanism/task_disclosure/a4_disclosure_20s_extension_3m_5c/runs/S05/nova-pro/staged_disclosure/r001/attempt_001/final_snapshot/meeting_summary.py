import boto3

transcribe = boto3.client('transcribe')

def summarize_transcript(transcript):
    response = transcribe.start_transcription_job(
        TranscriptionJobName='meeting-summary',
        LanguageCode='en-US',
        Media={'MediaFileUri': transcript},
        OutputBucketName='transcribe-output'
    )
    return response['TranscriptionJob']['TranscriptionJobName']

if __name__ == '__main__':\n    transcript_uri = 's3://your-bucket/your-transcript.mp3'
    job_name = summarize_transcript(transcript_uri)
    print(f'Transcription job started: {job_name}')
