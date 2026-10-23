import boto3

def get_timestamped_transcript(transcription_job_name):
    transcribe = boto3.client('transcribe')
    response = transcribe.get_transcription_job(TranscriptionJobName=transcription_job_name)
    
    if response['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcript_response = transcribe.get_transcription_job(TranscriptionJobName=transcription_job_name)
        transcript = transcript_response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        
        # Fetch the transcript content
        import requests
        transcript_content = requests.get(transcript).json()
        
        # Extract timestamps
        timestamped_transcript = {}
        for item in transcript_content['results']['items']:
            if 'start_time' in item and 'end_time' in item:
                timestamped_transcript[item['alternatives'][0]['content']] = {
                    'start_time': item['start_time'],
                    'end_time': item['end_time']
                }
        return timestamped_transcript
    else:
        return 'Transcription job is not completed.'