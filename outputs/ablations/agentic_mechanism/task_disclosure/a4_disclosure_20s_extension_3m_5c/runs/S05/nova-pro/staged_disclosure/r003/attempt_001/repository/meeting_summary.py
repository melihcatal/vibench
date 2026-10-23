import boto3

transcribe = boto3.client('transcribe')

def summarize_transcript(transcript):
    response = transcribe.start_transcription_job(
        TranscriptionJobName='meeting_summary',
        LanguageCode='en-US',
        Media={'MediaFileUri': transcript},
        OutputBucketName='transcribe-output',
        Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 10}
    )
    return response['TranscriptionJob']['TranscriptionJobName']

if __name__ == '__main__':
    transcript_uri = 's3://my-bucket/my-transcript.mp3'
    job_name = summarize_transcript(transcript_uri)
    print(f'Transcription job started with name: {job_name}')
