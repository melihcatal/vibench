import boto3

from speech_client import get_speech_client


def translate_transcript(job_id, config=None):
    client = get_speech_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response["TranscriptionJob"]
    transcript = job["Transcript"]
    items = transcript.get("Items", [])
    translate_client = boto3.client('translate', region_name=config.get('region'))
    translated_items = []
    for item in items:
        text = item["alternatives"][0]["transcript"]
        translation = translate_client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode='es')
        translated_items.append({
            "start_time": item["start_time"],
            "end_time": item["end_time"],
            "text": translation["TranslatedText"]
        })
    return {
        "job_id": job["TranscriptionJobName"],
        "status": job["TranscriptionJobStatus"],
        "translated_transcript": translated_items
    }