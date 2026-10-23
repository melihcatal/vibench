import os
import time
import json
import requests
from typing import List, Dict
from speech_client import get_transcribe_client

def get_timestamped_transcript(job_name: str, poll_interval_seconds: int = 10) -> List[Dict]:
    transcribe_client = get_transcribe_client()

    while True:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = response['TranscriptionJob']['TranscriptionJobStatus']

        if job_status == 'COMPLETED':
            transcript_file_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            transcript_content = requests.get(transcript_file_uri).json()

            items = []
            for item in transcript_content['results']['items']:
                start_time = float(item.get('start_time', 0)) if 'start_time' in item else None
                end_time = float(item.get('end_time', 0)) if 'end_time' in item else None
                content = item['alternatives'][0]['content']
                item_type = item['type']
                speaker_label = item.get('speaker_label')

                items.append({
                    'type': item_type,
                    'content': content,
                    'start_time': start_time,
                    'end_time': end_time,
                    'speaker_label': speaker_label
                })
            return items
        elif job_status == 'FAILED':
            raise Exception(f"Transcription job {job_name} failed: {response['TranscriptionJob']['FailureReason']}")
        else:
            time.sleep(poll_interval_seconds)