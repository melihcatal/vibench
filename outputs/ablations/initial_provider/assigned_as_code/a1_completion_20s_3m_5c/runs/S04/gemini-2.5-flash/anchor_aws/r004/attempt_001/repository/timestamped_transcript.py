import json
import time
import urllib.request

import boto3


def timestamped_transcript(job_id, config=None):
    config = config or {}
    client = boto3.client("transcribe", region_name=config.get("region"))
    while True:
        response = client.get_transcription_job(TranscriptionJobName=job_id)
        job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        if job_status == "COMPLETED":
            transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            with urllib.request.urlopen(transcript_uri) as f:
                transcript_json = json.loads(f.read().decode("utf-8"))
            
            timestamped_words = []
            for item in transcript_json["results"]["items"]:
                if item["type"] == "pronunciation":
                    timestamped_words.append({
                        "word": item["alternatives"][0]["content"],
                        "start_time": item["start_time"],
                        "end_time": item["end_time"],
                    })
            return timestamped_words
            
        elif job_status == "FAILED":
            raise Exception(f"Transcription job {job_id} failed.")
        time.sleep(5)
