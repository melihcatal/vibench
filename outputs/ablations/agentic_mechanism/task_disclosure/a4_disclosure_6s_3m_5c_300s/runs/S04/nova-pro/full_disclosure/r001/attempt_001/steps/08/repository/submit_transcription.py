import boto3

def submit_transcription_job(audio_file_uri, job_name, language_code):
    transcribe = boto3.client('transcribe')
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_file_uri},
        MediaFormat='mp3',
        LanguageCode=language_code
    )
    return response

if __name__ == '__main__':
    audio_file_uri = 's3://your-bucket/your-audio-file.mp3'
    job_name = 'your-transcription-job-name'
    language_code = 'en-US'
    response = submit_transcription_job(audio_file_uri, job_name, language_code)
    print(response)