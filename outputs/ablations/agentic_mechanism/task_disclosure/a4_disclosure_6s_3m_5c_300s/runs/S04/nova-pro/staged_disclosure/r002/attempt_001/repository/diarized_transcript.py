import boto3

transcribe = boto3.client('transcribe', region_name='us-west-2')

def start_transcription_job(job_name, media_file_uri):
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': media_file_uri},
        LanguageCode='en-US',
        MediaFormat='mp4',
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 10
        }
    )
    return response

if __name__ == '__main__':
    job_name = 'meeting_transcription'
    media_file_uri = 's3://your-bucket/your-media-file.mp4'
    response = start_transcription_job(job_name, media_file_uri)
    print(response)