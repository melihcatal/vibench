import boto3

from speech_client import get_transcribe_client


def translate_transcript(job_id, config=None):
    client = get_transcribe_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response["TranscriptionJob"]
    if job["TranscriptionJobStatus"]!= "COMPLETED":
        raise ValueError("Transcription job is not completed")
    transcript_uri = job["Transcript"]["TranscriptFileUri"]
    translate = boto3.client('translate', region_name=config.get('region'))
    with open(transcript_uri, 'r') as f:
        transcript_text = f.read()
    response = translate.translate_text(
        Text=transcript_text,
        SourceLanguageCode=job['LanguageCode'],
        TargetLanguageCode='en'
    )
    return response['TranslatedText']
