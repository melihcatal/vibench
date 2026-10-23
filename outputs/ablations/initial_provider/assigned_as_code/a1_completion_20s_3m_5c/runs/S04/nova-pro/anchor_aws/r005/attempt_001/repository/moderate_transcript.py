import boto3

from speech_client import get_speech_client


def moderate_transcript(job_id, config=None):
    client = get_speech_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response["TranscriptionJob"]
    transcript = job["Transcript"]
    items = transcript.get("Items", [])
    comprehend_client = boto3.client('comprehend', region_name=config.get('region'))
    moderated_items = []
    for item in items:
        text = item["alternatives"][0]["transcript"]
        moderation = comprehend_client.detect_sentiment(Text=text, LanguageCode='en')
        if moderation["Sentiment"]!= 'NEGATIVE':
            moderated_items.append({
                "start_time": item["start_time"],
                "end_time": item["end_time"],
                "text": text
            })
    return {
        "job_id": job["TranscriptionJobName"],
        "status": job["TranscriptionJobStatus"],
        "moderated_transcript": moderated_items
    }