# archive_summary.py
import os
import json
import boto3
from datetime import datetime
from typing import List
from speech_models import SpeechModels

# Example: python archive_summary.py <job_name> <output_bucket>
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: archive_summary.py <job_name> <output_bucket>", file=sys.stderr)
        sys.exit(1)
    job_name = sys.argv[1]
    output_bucket = sys.argv[2]

    # --- Fetch completed transcript (or use stored result) ---
    client = boto3.client('transcribe', region_name='us-east-1')
    job = client.get_transcription_job(TranscriptionJobName=job_name)
    transcript_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
    # Retrieve the transcript (assumes S3)
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=os.getenv('AWS_S3_BUCKET'), Key=transcript_uri.split('/')[-1])
    transcript_text = obj['Body'].read().decode()

    # --- Simple summarization using a hosted model (IBM watsonx.ai) ---
    from ibm_watson import NaturalLanguageUnderstandingV2
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

    auth = IAMAuthenticator(os.getenv('WATSON_NLU_APIKEY'))
    nlu = NaturalLanguageUnderstandingV2(version='2023-08-01', authenticator=auth)
    nlu.set_service_url(os.getenv('WATSON_NLU_ENDPOINT'))

    summary = nlu.summarize(
        text=transcript_text,
        language='en',
        return_analyzes='abstract'
    ).get_result()

    abstract = summary.get('summarizations', [{}])[0].get('abstract')
    if not abstract:
        abstract = "[Summary could not be generated]"

    # --- Store summary in S3 ---
    summary_json = {
        "job_name": job_name,
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "summary": abstract[0] if isinstance(abstract, list) else abstract,
        "original_uri": transcript_uri
    }
    s3.put_object(
        Bucket=output_bucket,
        Key=f'summaries/{job_name}.json',
        Body=json.dumps(summary_json).encode()
    )

    print(json.dumps(summary_json, indent=2))
