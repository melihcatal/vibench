import boto3

from speech_client import get_transcribe_client


def transcript_embedding(job_id, config=None):
    client = get_transcribe_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response["TranscriptionJob"]
    if job["TranscriptionJobStatus"]!= "COMPLETED":
        raise ValueError("Transcription job is not completed")
    transcript_uri = job["Transcript"]["TranscriptFileUri"]
    comprehend = boto3.client('comprehend', region_name=config.get('region'))
    with open(transcript_uri, 'r') as f:
        transcript_text = f.read()
    response = comprehend.detect_dominant_language(Text=transcript_text)
    language_code = response['Languages'][0]['LanguageCode']
    response = comprehend.detect_sentiment(Text=transcript_text, LanguageCode=language_code)
    sentiment = response['Sentiment']
    return sentiment
